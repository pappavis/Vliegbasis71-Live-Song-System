"""TDD/unit tests for muscriptor_batch.py.

Run:
    python -m unittest -v test_muscriptor_batch.py

No real MuScriptor, ffmpeg, model download, GPU, network, or audio transcription
is required: external processes are replaced by test doubles.
"""

from __future__ import annotations

import configparser
import subprocess
import tempfile
import unittest
from pathlib import Path

from muscriptor_batch import (
    AppSettings,
    CommandBuilder,
    ConfigurationManager,
    ConversionJob,
    Converter,
    JobResolver,
)


class ConfigurationManagerTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.config_path = self.root / "muscriptor_batch.cfg"
        self.manager = ConfigurationManager(self.config_path)
        self.fallback = AppSettings(
            input_dir=self.root / "fallback-in",
            output_dir=self.root / "fallback-out",
            muscriptor_command="uvx muscriptor",
            ffmpeg_command="ffmpeg",
            default_format="midi",
        )

    def tearDown(self) -> None:
        self.temp.cleanup()

    def test_load_returns_fallback_when_cfg_does_not_exist(self) -> None:
        actual = self.manager.load(self.fallback)
        self.assertEqual(actual, self.fallback)

    def test_save_and_load_round_trip(self) -> None:
        expected = AppSettings(
            input_dir=self.root / "music in",
            output_dir=self.root / "music out",
            muscriptor_command="python -m muscriptor",
            ffmpeg_command="custom-ffmpeg",
            default_format="sheet",
        )

        self.manager.save(expected)
        actual = self.manager.load(self.fallback)

        self.assertEqual(actual, expected)

    def test_save_creates_settings_section(self) -> None:
        self.manager.save(self.fallback)
        parser = configparser.ConfigParser()
        parser.read(self.config_path, encoding="utf-8")

        self.assertTrue(parser.has_section("settings"))
        self.assertEqual(parser["settings"]["default_format"], "midi")


class CommandBuilderTests(unittest.TestCase):
    def test_build_midi_command(self) -> None:
        builder = CommandBuilder("uvx muscriptor", "ffmpeg", windows=False)

        command = builder.build_midi(
            Path("/music/My Song.mp3"),
            Path("/out/My Song.mid"),
        )

        self.assertEqual(
            command,
            [
                "uvx",
                "muscriptor",
                "transcribe",
                "/music/My Song.mp3",
                "-o",
                "/out/My Song.mid",
            ],
        )

    def test_build_sheet_command_uses_current_muscriptor_sheets_format(self) -> None:
        builder = CommandBuilder("uvx muscriptor", "ffmpeg", windows=False)

        command = builder.build_sheets(
            Path("/music/song.mp3"),
            Path("/out/song"),
        )

        self.assertEqual(
            command,
            [
                "uvx",
                "muscriptor",
                "transcribe",
                "/music/song.mp3",
                "--format",
                "sheets",
                "--output",
                "/out/song",
            ],
        )

    def test_build_wav_command_uses_pcm_16_bit(self) -> None:
        builder = CommandBuilder("uvx muscriptor", "ffmpeg", windows=False)

        command = builder.build_wav(
            Path("/music/song.mp3"),
            Path("/out/song.wav"),
        )

        self.assertEqual(
            command,
            [
                "ffmpeg",
                "-y",
                "-i",
                "/music/song.mp3",
                "-vn",
                "-c:a",
                "pcm_s16le",
                "/out/song.wav",
            ],
        )

    def test_command_with_arguments_is_split_without_shell(self) -> None:
        builder = CommandBuilder(
            "uvx --python 3.12 muscriptor",
            "ffmpeg",
            windows=False,
        )

        command = builder.build_midi(Path("a.mp3"), Path("a.mid"))

        self.assertEqual(
            command[:4],
            ["uvx", "--python", "3.12", "muscriptor"],
        )


class JobResolverTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.input_dir = Path(self.temp.name)
        (self.input_dir / "alpha.mp3").touch()
        (self.input_dir / "beta.mp3").touch()
        (self.input_dir / "ignore.wav").touch()
        self.resolver = JobResolver(self.input_dir)

    def tearDown(self) -> None:
        self.temp.cleanup()

    def test_without_explicit_files_finds_only_mp3_files(self) -> None:
        jobs = self.resolver.resolve(None, "midi", {})

        self.assertEqual(
            [job.source.name for job in jobs],
            ["alpha.mp3", "beta.mp3"],
        )
        self.assertTrue(all(job.output_format == "midi" for job in jobs))

    def test_explicit_relative_file_is_resolved_against_input_directory(self) -> None:
        jobs = self.resolver.resolve(["beta.mp3"], "midi", {})

        self.assertEqual(len(jobs), 1)
        self.assertEqual(jobs[0].source, self.input_dir / "beta.mp3")

    def test_per_file_format_overrides_default(self) -> None:
        jobs = self.resolver.resolve(
            None,
            "midi",
            {"beta.mp3": "sheet"},
        )

        formats = {job.source.name: job.output_format for job in jobs}
        self.assertEqual(formats["alpha.mp3"], "midi")
        self.assertEqual(formats["beta.mp3"], "sheet")


class FakeSuccessfulRunner:
    """Test double for subprocess.run that also creates expected outputs."""

    def __init__(self) -> None:
        self.commands: list[list[str]] = []

    def __call__(self, command: list[str], check: bool) -> subprocess.CompletedProcess:
        self.commands.append(command)
        self._materialize_expected_output(command)
        return subprocess.CompletedProcess(command, 0)

    def _materialize_expected_output(self, command: list[str]) -> None:
        if "--format" in command and "sheets" in command:
            output_dir = Path(command[command.index("--output") + 1])
            output_dir.mkdir(parents=True, exist_ok=True)
            (output_dir / "score.mid").touch()
            return

        if "-o" in command:
            output_file = Path(command[command.index("-o") + 1])
            output_file.parent.mkdir(parents=True, exist_ok=True)
            output_file.touch()
            return

        # ffmpeg command: output path is the final argument.
        output_file = Path(command[-1])
        output_file.parent.mkdir(parents=True, exist_ok=True)
        output_file.touch()


class ConverterTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.input_dir = self.root / "in"
        self.output_dir = self.root / "out"
        self.input_dir.mkdir()

        self.source = self.input_dir / "My Song.mp3"
        self.source.touch()

        self.settings = AppSettings(
            input_dir=self.input_dir,
            output_dir=self.output_dir,
            muscriptor_command="uvx muscriptor",
            ffmpeg_command="ffmpeg",
            default_format="midi",
        )

    def tearDown(self) -> None:
        self.temp.cleanup()

    def test_midi_conversion_calls_muscriptor_and_checks_output(self) -> None:
        runner = FakeSuccessfulRunner()
        converter = Converter(self.settings, runner=runner)

        ok = converter.convert([ConversionJob(self.source, "midi")])

        self.assertTrue(ok)
        self.assertTrue((self.output_dir / "My Song.mid").exists())
        self.assertIn("transcribe", runner.commands[0])

    def test_wav_conversion_calls_ffmpeg(self) -> None:
        runner = FakeSuccessfulRunner()
        converter = Converter(self.settings, runner=runner)

        ok = converter.convert([ConversionJob(self.source, "wav")])

        self.assertTrue(ok)
        self.assertTrue((self.output_dir / "My Song.wav").exists())
        self.assertEqual(runner.commands[0][0], "ffmpeg")

    def test_sheet_conversion_expects_score_mid(self) -> None:
        runner = FakeSuccessfulRunner()
        converter = Converter(self.settings, runner=runner)

        ok = converter.convert([ConversionJob(self.source, "sheet")])

        self.assertTrue(ok)
        self.assertTrue((self.output_dir / "My Song" / "score.mid").exists())

    def test_missing_source_raises_file_not_found(self) -> None:
        converter = Converter(self.settings, runner=FakeSuccessfulRunner())

        with self.assertRaises(FileNotFoundError):
            converter.convert(
                [ConversionJob(self.input_dir / "missing.mp3", "midi")]
            )

    def test_invalid_format_raises_value_error(self) -> None:
        converter = Converter(self.settings, runner=FakeSuccessfulRunner())

        with self.assertRaises(ValueError):
            converter.convert([ConversionJob(self.source, "mp4")])

    def test_external_process_failure_returns_false(self) -> None:
        def failing_runner(command: list[str], check: bool) -> None:
            raise subprocess.CalledProcessError(1, command)

        messages: list[str] = []
        converter = Converter(self.settings, runner=failing_runner)

        ok = converter.convert(
            [ConversionJob(self.source, "midi")],
            on_message=messages.append,
        )

        self.assertFalse(ok)
        self.assertTrue(any("FOUT" in message for message in messages))

    def test_successful_process_without_output_is_reported_as_failure(self) -> None:
        def no_output_runner(command: list[str], check: bool) -> subprocess.CompletedProcess:
            return subprocess.CompletedProcess(command, 0)

        converter = Converter(self.settings, runner=no_output_runner)

        ok = converter.convert([ConversionJob(self.source, "midi")])

        self.assertFalse(ok)


if __name__ == "__main__":
    unittest.main(verbosity=2)
