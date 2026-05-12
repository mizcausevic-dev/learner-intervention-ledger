from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from statistics import mean
from typing import Any


def _clamp(value: float, low: int = 0, high: int = 100) -> int:
    return max(low, min(high, round(value)))


@dataclass(slots=True)
class LearnerInterventionLedgerService:
    source_path: Path

    def load(self) -> dict[str, Any]:
        return json.loads(self.source_path.read_text(encoding="utf-8"))

    def enrich(self, item: dict[str, Any]) -> dict[str, Any]:
        closure_score = _clamp(
            55
            + item["risk_shift"] * 2.8
            + (14 if item["response_received"] else -10)
            + (8 if item["status"] == "closed" else 0)
            - item["days_open"] * 2.6
            - item["touch_count"] * 1.9
            - item["escalation_level"] * 5.2
        )
        effectiveness = (
            "strong"
            if closure_score >= 72
            else "mixed"
            if closure_score >= 48
            else "stalled"
        )
        next_action = (
            "Close the case, document the successful pattern, and recycle it into the advising playbook."
            if item["status"] == "closed" and effectiveness == "strong"
            else "Keep the case open with the current owner lane, but reduce touch frequency because momentum is improving."
            if effectiveness == "mixed" and item["response_received"]
            else "Escalate the case again and change the owner lane or channel because the current pattern is not resolving risk."
        )
        return {
            "interventionId": item["intervention_id"],
            "studentId": item["student_id"],
            "studentName": item["student_name"],
            "program": item["program"],
            "ownerLane": item["owner_lane"],
            "channel": item["channel"],
            "eventType": item["event_type"],
            "status": item["status"],
            "outcome": item["outcome"],
            "daysOpen": item["days_open"],
            "touchCount": item["touch_count"],
            "responseReceived": item["response_received"],
            "riskShift": item["risk_shift"],
            "escalationLevel": item["escalation_level"],
            "closureScore": closure_score,
            "effectiveness": effectiveness,
            "nextAction": next_action,
        }

    def events(self) -> list[dict[str, Any]]:
        data = self.load()
        return sorted(
            [self.enrich(item) for item in data["interventions"]],
            key=lambda item: (item["status"] != "open", item["status"] != "in-progress", -item["daysOpen"], item["studentName"]),
        )

    def summary(self) -> dict[str, Any]:
        data = self.load()
        events = self.events()
        open_cases = [event for event in events if event["status"] != "closed"]
        closed = [event for event in events if event["status"] == "closed"]
        strong = [event for event in events if event["effectiveness"] == "strong"]
        avg_days_open = mean(event["daysOpen"] for event in events)
        avg_closure = mean(event["closureScore"] for event in events)
        return {
            "institution": data["institution"],
            "term": data["term"],
            "interventionCount": len(events),
            "openCaseCount": len(open_cases),
            "closedCaseCount": len(closed),
            "strongResolutionCount": len(strong),
            "averageDaysOpen": round(avg_days_open, 1),
            "averageClosureScore": round(avg_closure, 1),
            "leadRecommendation": (
                "Treat unresolved finance and care-team cases as their own operating lane, then mine the closed strong-resolution cases for reusable outreach patterns."
            ),
        }

    def lane_breakdown(self) -> list[dict[str, Any]]:
        counts: dict[str, int] = {}
        for event in self.events():
            counts[event["ownerLane"]] = counts.get(event["ownerLane"], 0) + 1
        return [{"ownerLane": lane, "count": count} for lane, count in sorted(counts.items())]

    def outcome_breakdown(self) -> list[dict[str, Any]]:
        counts: dict[str, int] = {}
        for event in self.events():
            counts[event["effectiveness"]] = counts.get(event["effectiveness"], 0) + 1
        order = {"strong": 0, "mixed": 1, "stalled": 2}
        return [{"effectiveness": name, "count": count} for name, count in sorted(counts.items(), key=lambda item: order[item[0]])]

    def intervention(self, intervention_id: str) -> dict[str, Any] | None:
        for event in self.events():
            if event["interventionId"] == intervention_id:
                return event
        return None

    def sample_payload(self) -> dict[str, Any]:
        events = self.events()
        return {
            "dashboard": self.summary(),
            "openCases": [
                {
                    "interventionId": event["interventionId"],
                    "studentName": event["studentName"],
                    "ownerLane": event["ownerLane"],
                    "closureScore": event["closureScore"],
                    "effectiveness": event["effectiveness"],
                    "nextAction": event["nextAction"],
                }
                for event in events[:3]
            ],
        }


def build_service(root: Path | None = None) -> LearnerInterventionLedgerService:
    base = root or Path(__file__).resolve().parents[2]
    return LearnerInterventionLedgerService(base / "app" / "data" / "sample_interventions.json")
