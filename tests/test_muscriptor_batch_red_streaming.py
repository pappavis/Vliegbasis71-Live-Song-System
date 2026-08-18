"""RED-phase tests for live MuScriptor/ffmpeg command output streaming.

These tests intentionally describe the NEXT required behavior.
Against the current production implementation they should FAIL.

Target behavior:
- subprocess output is streamed line-by-line while conversion is running;
- stdout and stderr are visible through the existing on_message callback;
- a non-zero process exit is reported as conversion failure;
- existing expected-output validation remains intact.

Run from the repository root after copying/merging these tests:

    python -m unittest -v tests.test_muscriptor_batch

RED acceptance criterion:
    Existing 17 tests stay GREEN.
    These new streaming tests FAIL because live streaming is not implemented yet.
"""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from muscriptor_batch import AppSettings, ConversionJob, Converter


class FakeStream:
    def __init__(self, lines: list[str]) -> None:
        self._lines = iter(lines)

    def __iter__(self):
        return self

    def __next__(self) -> str:
        return next(self._lines)


class FakeStreamingProcess:
    """Popen-like test double for the future streaming implementation."""

    def __init__(
        self,
        lines: list[str],
        returncode: int = 0,
        output_file: Path | None = None,
    ) -> None:
        self.stdout = FakeStream(lines)
        self.returncode = None
        self._final_returncode = returncode
        self._output_file = output_file
        self.wait_called = False

    def wait(self) -> int:
        self.wait_called = True
        self.returncode = self._final_returncode

        if self.returncode == 0 and self._output_file is not None:
            self._output_file.parent.mkdir(parents=True, exist_ok=True)
            self._output_file.touch()

        return self.returncode


class LiveCommandOutputRedPhaseTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.input_dir = self.root / "in"
        self.output_dir = self.root / "out"
        self.input_dir.mkdir()

        self.source = self.input_dir / "Live Song.mp3"
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

    def test_converter_accepts_process_factory_for_live_streaming(self) -> None:
        """RED: Converter needs an injectable Popen-style process factory."""

        process_factory = lambda *args, **kwargs: FakeStreamingProcess([])

        # Expected to fail in RED because current Converter only accepts runner=.
        converter = Converter(
            self.settings,
            process_factory=process_factory,
        )

        self.assertIsNotNone(converter)

    def test_muscriptor_output_is_forwarded_line_by_line_to_callback(self) -> None:
        """RED: real command output must become visible during conversion."""

        expected_output = self.output_dir / "Live Song.mid"
        process = FakeStreamingProcess(
            [
                "Loading MuScriptor model...\n",
                "Separating instruments...\n",
                "Transcribing notes...\n",
                "Writing MIDI...\n",
            ],
            returncode=0,
            output_file=expected_output,
        )

        def process_factory(*args, **kwargs):
            return process

        messages: list[str] = []
        converter = Converter(
            self.settings,
            process_factory=process_factory,
        )

        ok = converter.convert(
            [ConversionJob(self.source, "midi")],
            on_message=messages.append,
        )

        self.assertTrue(ok)
        self.assertIn("Loading MuScriptor model...", messages)
        self.assertIn("Separating instruments...", messages)
        self.assertIn("Transcribing notes...", messages)
        self.assertIn("Writing MIDI...", messages)

        # Streaming output should retain chronological order.
        positions = [
            messages.index("Loading MuScriptor model..."),
            messages.index("Separating instruments..."),
            messages.index("Transcribing notes..."),
            messages.index("Writing MIDI..."),
        ]
        self.assertEqual(positions, sorted(positions))

    def test_stderr_is_merged_into_visible_debug_stream(self) -> None:
        """RED: stderr warnings/errors should appear in the same UI stream."""

        expected_output = self.output_dir / "Live Song.mid"
        process = FakeStreamingProcess(
            [
                "Loading model...\n",
                "WARNING: falling back to another backend\n",
                "Transcribing...\n",
            ],
            returncode=0,
            output_file=expected_output,
        )

        def process_factory(*args, **kwargs):
            # GREEN implementation should request stderr -> stdout.
            self.assertIn("stderr", kwargs)
            return process

        messages: list[str] = []
        converter = Converter(
            self.settings,
            process_factory=process_factory,
        )

        ok = converter.convert(
            [ConversionJob(self.source, "midi")],
            on_message=messages.append,
        )

        self.assertTrue(ok)
        self.assertIn(
            "WARNING: falling back to another backend",
            messages,
        )

    def test_nonzero_streaming_process_exit_returns_false(self) -> None:
        """RED: streamed process errors must still fail the conversion."""

        process = FakeStreamingProcess(
            [
                "Loading model...\n",
                "ERROR: transcription failed\n",
            ],
            returncode=7,
        )

        def process_factory(*args, **kwargs):
            return process

        messages: list[str] = []
        converter = Converter(
            self.settings,
            process_factory=process_factory,
        )

        ok = converter.convert(
            [ConversionJob(self.source, "midi")],
            on_message=messages.append,
        )

        self.assertFalse(ok)
        self.assertIn("ERROR: transcription failed", messages)
        self.assertTrue(
            any("FOUT" in message for message in messages),
            messages,
        )

    def test_blank_process_lines_are_not_added_to_ui_log(self) -> None:
        """RED: console should not be flooded with meaningless blank lines."""

        expected_output = self.output_dir / "Live Song.mid"
        process = FakeStreamingProcess(
            [
                "Loading model...\n",
                "\n",
                "   \n",
                "Transcribing...\n",
            ],
            returncode=0,
            output_file=expected_output,
        )

        def process_factory(*args, **kwargs):
            return process

        messages: list[str] = []
        converter = Converter(
            self.settings,
            process_factory=process_factory,
        )

        ok = converter.convert(
            [ConversionJob(self.source, "midi")],
            on_message=messages.append,
        )

        self.assertTrue(ok)
        self.assertNotIn("", messages)
        self.assertNotIn("   ", messages)
        self.assertIn("Loading model...", messages)
        self.assertIn("Transcribing...", messages)


if __name__ == "__main__":
    unittest.main(verbosity=2)
