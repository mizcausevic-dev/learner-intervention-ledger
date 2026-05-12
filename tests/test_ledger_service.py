from __future__ import annotations

from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from app.services.ledger_service import build_service


class InterventionLedgerTests(unittest.TestCase):
    def setUp(self) -> None:
        self.service = build_service(ROOT)

    def test_summary_shape(self) -> None:
        summary = self.service.summary()
        self.assertEqual(summary["institution"], "Northstar Online University")
        self.assertGreater(summary["interventionCount"], 0)

    def test_lookup(self) -> None:
        item = self.service.intervention("int-4041")
        self.assertIsNotNone(item)
        self.assertEqual(item["effectiveness"], "strong")

    def test_events_are_sorted_with_open_work_first(self) -> None:
        events = self.service.events()
        self.assertIn(events[0]["status"], {"open", "in-progress"})


if __name__ == "__main__":
    unittest.main()
