"""
File     : test_version_cli_ui_red.py
Version  : 0.2.2
ChatID   : 6F3A9C21
Purpose  : RED tests for embedded release metadata, --version, and UI release identity.
"""

from __future__ import annotations

import subprocess
import sys
import unittest
from pathlib import Path

import muscriptor_batch


class VersionCliUiRedTests(unittest.TestCase):
    EXPECTED_VERSION = "0.2.2"
    EXPECTED_CHAT_ID = "6F3A9C21"

    def test_release_constants_are_embedded(self) -> None:
        self.assertEqual(muscriptor_batch.VERSION, self.EXPECTED_VERSION)
        self.assertEqual(muscriptor_batch.RELEASE_CHAT_ID, self.EXPECTED_CHAT_ID)

    def test_source_header_contains_file_version_chatid_purpose(self) -> None:
        source = Path(muscriptor_batch.__file__).read_text(encoding="utf-8")
        header = "\n".join(source.splitlines()[:20])
        self.assertIn("File", header)
        self.assertIn("muscriptor_batch.py", header)
        self.assertIn("Version", header)
        self.assertIn(self.EXPECTED_VERSION, header)
        self.assertIn("ChatID", header)
        self.assertIn(self.EXPECTED_CHAT_ID, header)
        self.assertIn("Purpose", header)

    def test_release_display_text_contains_version_and_chatid(self) -> None:
        text = muscriptor_batch.DesktopApp.build_release_text()
        self.assertIn(self.EXPECTED_VERSION, text)
        self.assertIn(self.EXPECTED_CHAT_ID, text)

    def test_cli_version_returns_version_and_chatid(self) -> None:
        source = Path(muscriptor_batch.__file__).resolve()
        result = subprocess.run(
            [sys.executable, str(source), "--version"],
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn(self.EXPECTED_VERSION, result.stdout)
        self.assertIn(self.EXPECTED_CHAT_ID, result.stdout)


if __name__ == "__main__":
    unittest.main(verbosity=2)
