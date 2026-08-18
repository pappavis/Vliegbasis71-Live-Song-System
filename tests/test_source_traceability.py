"""
File     : test_source_traceability.py
Version  : 0.2.1
ChatID   : 2D7A4C91
Purpose  : Enforces Version and ChatID headers across all Python source files.
"""

from __future__ import annotations

import unittest
from pathlib import Path


class SourceTraceabilityTests(unittest.TestCase):
    EXPECTED_VERSION = "0.2.1"
    EXPECTED_CHAT_ID = "2D7A4C91"

    def test_all_python_source_files_have_release_metadata(self) -> None:
        project_root = Path(__file__).resolve().parents[1]
        python_files = sorted(
            list((project_root / "src").rglob("*.py"))
            + list((project_root / "tests").rglob("*.py"))
        )

        self.assertTrue(python_files, "No Python source files found.")

        failures: list[str] = []
        for source_file in python_files:
            header = "\n".join(
                source_file.read_text(encoding="utf-8").splitlines()[:20]
            )
            if self.EXPECTED_VERSION not in header:
                failures.append(
                    f"{source_file}: missing Version {self.EXPECTED_VERSION}"
                )
            if self.EXPECTED_CHAT_ID not in header:
                failures.append(
                    f"{source_file}: missing ChatID {self.EXPECTED_CHAT_ID}"
                )

        self.assertEqual([], failures, "\n" + "\n".join(failures))


if __name__ == "__main__":
    unittest.main(verbosity=2)
