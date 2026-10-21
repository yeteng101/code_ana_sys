from __future__ import annotations

import unittest

from scripts.run_validation_project import build_gate
from scripts.prepare_validation_truth import combined_review


class QualityGateTests(unittest.TestCase):
    def report(self, *, call_recall=1.0, resource_recall=0.7, sync_recall=0.2, fp=0):
        return {
            "review": {"human_review": "pending"},
            "categories": {
                "call_chain": {"recall": call_recall, "fp": fp},
                "resource_flow": {"recall": resource_recall, "fp": 0},
                "sync_relation": {"recall": sync_recall, "fp": 0},
            },
        }

    def gate(self, report, **kwargs):
        return build_gate(
            report,
            min_call_recall=kwargs.get("min_call_recall", 0.95),
            min_resource_recall=kwargs.get("min_resource_recall", 0.6),
            min_sync_recall=kwargs.get("min_sync_recall", 0.1),
            max_fp=kwargs.get("max_fp", 0),
            strict_review=kwargs.get("strict_review", False),
        )

    def test_passes_thresholds_and_reports_pending_review_informationally(self):
        result = self.gate(self.report())
        self.assertEqual(result["status"], "passed")
        review = next(item for item in result["checks"] if item["name"] == "human_review")
        self.assertEqual(review["status"], "informational")

    def test_fails_on_metric_regression_and_false_positive(self):
        result = self.gate(self.report(call_recall=0.9, fp=1))
        self.assertEqual(result["status"], "failed")
        self.assertTrue(any(
            item["name"] == "call_chain.recall" and item["status"] == "failed"
            for item in result["checks"]
        ))
        self.assertTrue(any(
            item["name"] == "false_positives" and item["status"] == "failed"
            for item in result["checks"]
        ))

    def test_strict_review_requires_confirmed(self):
        result = self.gate(self.report(), strict_review=True)
        self.assertEqual(result["status"], "failed")
        review = next(item for item in result["checks"] if item["name"] == "human_review")
        self.assertEqual(review["status"], "failed")

    def test_review_status_is_confirmed_only_when_all_datasets_are_confirmed(self):
        pending = {"review": {"human_review": "pending", "method": "ai"}}
        confirmed = {"review": {"human_review": "confirmed", "method": "human"}}
        self.assertEqual(
            combined_review(confirmed, pending)["human_review"],
            "pending",
        )
        self.assertEqual(
            combined_review(confirmed, confirmed)["human_review"],
            "confirmed",
        )


if __name__ == "__main__":
    unittest.main()
