"""
File     : test_stop_conversion_red.py
Version  : 0.2.3
ChatID   : B71E4C2A
Purpose  : RED TDD tests for stopping an active MuScriptor/ffmpeg
           conversion from the desktop UI.
"""

from __future__ import annotations

import inspect
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import Mock

import muscriptor_batch
from muscriptor_batch import (
    AppSettings,
    ConversionJob,
    Converter,
    DesktopApp,
)


EXPECTED_VERSION = "0.2.3"
EXPECTED_CHAT_ID = "B71E4C2A"


class FakeStdout:
    """Small iterable stdout replacement for process tests."""

    def __init__(self, lines: list[str]) -> None:
        self._lines = lines

    def __iter__(self):
        return iter(self._lines)


class FakeProcess:
    """
    Minimal Popen-compatible process for RED tests.

    terminate() records that termination was requested.
    """

    def __init__(
        self,
        lines: list[str] | None = None,
        return_code: int = 0,
    ) -> None:
        self.stdout = FakeStdout(lines or [])
        self.return_code = return_code
        self.terminated = False

    def wait(self) -> int:
        return self.return_code

    def terminate(self) -> None:
        self.terminated = True
        self.return_code = -15

    def poll(self):
        if self.terminated:
            return self.return_code

        return None


class StopConversionRedPhaseTests(unittest.TestCase):
    """
    RED specification for user-controlled cancellation.

    These tests describe the desired 0.2.3 behaviour and should
    initially fail against 0.2.2.
    """

    def test_converter_exposes_stop_method(self) -> None:
        """
        Converter must expose an explicit stop operation.
        """

        self.assertTrue(
            hasattr(
                Converter,
                "stop",
            ),
            "Converter must implement stop().",
        )

    def test_converter_tracks_current_process(self) -> None:
        """
        Converter must retain the active Popen instance so another
        thread can terminate it.
        """

        settings = AppSettings()

        converter = Converter(
            settings
        )

        self.assertTrue(
            hasattr(
                converter,
                "_current_process",
            ),
            (
                "Converter must track the currently running "
                "external process."
            ),
        )

    def test_converter_tracks_stop_request(self) -> None:
        """
        Converter needs cancellation state so it does not start
        another batch item after Stop was pressed.
        """

        settings = AppSettings()

        converter = Converter(
            settings
        )

        self.assertTrue(
            hasattr(
                converter,
                "_stop_requested",
            ),
            "Converter must track whether Stop was requested.",
        )

    def test_stop_terminates_active_process(self) -> None:
        """
        stop() must call terminate() on the active external process.
        """

        settings = AppSettings()

        converter = Converter(
            settings
        )

        fake_process = FakeProcess()

        # This assignment represents an external command currently
        # being executed by Converter.
        converter._current_process = fake_process

        converter.stop()

        self.assertTrue(
            fake_process.terminated,
            (
                "Stopping conversion must terminate the active "
                "MuScriptor/ffmpeg process."
            ),
        )

    def test_stop_sets_stop_requested_state(self) -> None:
        """
        stop() must remember cancellation even when no subprocess
        happens to be active at that exact instant.
        """

        settings = AppSettings()

        converter = Converter(
            settings
        )

        converter.stop()

        self.assertTrue(
            converter._stop_requested,
            "stop() must set the cancellation flag.",
        )

    def test_stop_without_active_process_is_safe(self) -> None:
        """
        Pressing Stop during a transition between files must not
        crash the application.
        """

        settings = AppSettings()

        converter = Converter(
            settings
        )

        converter._current_process = None

        try:
            converter.stop()

        except Exception as exc:
            self.fail(
                "stop() must be safe without an active process; "
                f"got {exc!r}"
            )

    def test_batch_does_not_start_next_job_after_stop(self) -> None:
        """
        Once cancellation has been requested, Converter must not
        continue through the remaining batch.
        """

        with TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)

            input_one = root / "one.mp3"
            input_two = root / "two.mp3"

            input_one.write_bytes(b"fake mp3")
            input_two.write_bytes(b"fake mp3")

            output_dir = root / "output"

            settings = AppSettings(
                input_dir=root,
                output_dir=output_dir,
            )

            process_factory = Mock()

            converter = Converter(
                settings,
                process_factory=process_factory,
            )

            jobs = [
                ConversionJob(
                    source=input_one,
                    output_format="midi",
                ),
                ConversionJob(
                    source=input_two,
                    output_format="midi",
                ),
            ]

            converter._stop_requested = True

            converter.convert(
                jobs,
            )

            process_factory.assert_not_called()

    def test_desktop_app_exposes_stop_handler(self) -> None:
        """
        DesktopApp must have a handler connected to the Stop button.
        """

        self.assertTrue(
            hasattr(
                DesktopApp,
                "_stop_conversion",
            ),
            "DesktopApp must implement _stop_conversion().",
        )

    def test_ui_contains_stop_button(self) -> None:
        """
        The desktop UI must visibly expose Stop.
        """

        source = inspect.getsource(
            DesktopApp._build_ui
        )

        self.assertIn(
            'text="Stop"',
            source,
            "Desktop UI must contain a Stop button.",
        )

    def test_stop_button_calls_stop_conversion(self) -> None:
        """
        Stop button must be wired to the stop handler.
        """

        source = inspect.getsource(
            DesktopApp._build_ui
        )

        self.assertIn(
            "command=self._stop_conversion",
            source,
            (
                "Stop button must call "
                "DesktopApp._stop_conversion()."
            ),
        )

    def test_stop_button_is_instance_attribute(self) -> None:
        """
        UI must retain access to the button so its state can change.
        """

        source = inspect.getsource(
            DesktopApp._build_ui
        )

        self.assertIn(
            "self._stop_button = ttk.Button",
            source,
        )

    def test_stop_button_starts_disabled(self) -> None:
        """
        There is nothing to stop before conversion begins.
        """

        source = inspect.getsource(
            DesktopApp._build_ui
        )

        stop_position = source.find(
            "self._stop_button = ttk.Button"
        )

        self.assertNotEqual(
            stop_position,
            -1,
        )

        stop_section = source[
            stop_position:
            stop_position + 700
        ]

        self.assertIn(
            'state="disabled"',
            stop_section,
            "Stop button must initially be disabled.",
        )

    def test_start_conversion_enables_stop_button(self) -> None:
        """
        Starting a conversion enables Stop.
        """

        source = inspect.getsource(
            DesktopApp._start_conversion
        )

        self.assertIn(
            "self._stop_button.configure",
            source,
        )

        self.assertIn(
            'state="normal"',
            source,
        )

    def test_finish_conversion_disables_stop_button(self) -> None:
        """
        Once processing is finished there is nothing left to stop.
        """

        source = inspect.getsource(
            DesktopApp._finish_conversion
        )

        self.assertIn(
            "self._stop_button.configure",
            source,
        )

        self.assertIn(
            'state="disabled"',
            source,
        )

    def test_desktop_app_tracks_active_converter(self) -> None:
        """
        DesktopApp needs a reference to the worker's Converter so
        the GUI thread can request cancellation.
        """

        source = inspect.getsource(
            DesktopApp.__init__
        )

        self.assertIn(
            "self._active_converter",
            source,
            (
                "DesktopApp must retain the active Converter "
                "instance."
            ),
        )

    def test_stop_handler_calls_converter_stop(self) -> None:
        """
        The UI handler must delegate process cancellation to
        Converter instead of directly manipulating subprocesses.
        """

        self.assertTrue(
            hasattr(
                DesktopApp,
                "_stop_conversion",
            ),
            "DesktopApp._stop_conversion() does not exist yet.",
        )

        source = inspect.getsource(
            DesktopApp._stop_conversion
        )

        self.assertIn(
            ".stop()",
            source,
            (
                "_stop_conversion() must delegate to "
                "Converter.stop()."
            ),
        )


if __name__ == "__main__":
    unittest.main(verbosity=2)
    