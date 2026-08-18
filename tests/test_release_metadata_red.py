"""RED phase: release traceability metadata.

Required behavior:
- production module exposes VERSION and RELEASE_CHAT_ID;
- values identify this release;
- UI title/label text can be generated without creating a Tk window;
- source header contains Version and ChatID comments for human traceability.

Expected RED state against the current production code:
these tests fail because release metadata is not implemented yet.
"""

from __future__ import annotations

import unittest
from pathlib import Path

import muscriptor_batch


class ReleaseMetadataRedPhaseTests(unittest.TestCase):
    EXPECTED_VERSION = "0.2.0"
    EXPECTED_CHAT_ID = "5A83D1C7"

    def test_module_exposes_version(self) -> None:
        self.assertTrue(hasattr(muscriptor_batch, "VERSION"))
        self.assertEqual(muscriptor_batch.VERSION, self.EXPECTED_VERSION)

    def test_module_exposes_release_chat_id(self) -> None:
        self.assertTrue(hasattr(muscriptor_batch, "RELEASE_CHAT_ID"))
        self.assertEqual(
            muscriptor_batch.RELEASE_CHAT_ID,
            self.EXPECTED_CHAT_ID,
        )

    def test_release_identity_contains_version_and_chat_id(self) -> None:
        self.assertTrue(hasattr(muscriptor_batch, "ReleaseInfo"))

        release = muscriptor_batch.ReleaseInfo(
            version=muscriptor_batch.VERSION,
            chat_id=muscriptor_batch.RELEASE_CHAT_ID,
        )

        text = release.display_text()

        self.assertIn("0.2.0", text)
        self.assertIn("5A83D1C7", text)

    def test_source_header_contains_traceability_metadata(self) -> None:
        source_path = Path(muscriptor_batch.__file__).resolve()
        header = "\n".join(
            source_path.read_text(encoding="utf-8").splitlines()[:20]
        )

        self.assertIn("Version", header)
        self.assertIn(self.EXPECTED_VERSION, header)
        self.assertIn("ChatID", header)
        self.assertIn(self.EXPECTED_CHAT_ID, header)

    def test_desktop_app_exposes_release_text_builder(self) -> None:
        self.assertTrue(
            hasattr(muscriptor_batch.DesktopApp, "build_release_text")
        )

        text = muscriptor_batch.DesktopApp.build_release_text()

        self.assertIn(self.EXPECTED_VERSION, text)
        self.assertIn(self.EXPECTED_CHAT_ID, text)


if __name__ == "__main__":
    unittest.main(verbosity=2)
