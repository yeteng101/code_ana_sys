import unittest

from scripts.simulate_validation_review import (
    ROOT,
    read_json,
    review_libuv_calls,
    review_libuv_sync,
    review_redis_calls,
    review_redis_sync,
    review_resources,
)


class SimulatedReviewTests(unittest.TestCase):
    def test_category_decision_counts(self):
        self.assertEqual(
            {
                "Confirmed": 33,
                "Confirmed with condition": 3,
                "Rejected": 64,
            },
            {
                decision: sum(
                    item["decision"] == decision
                    for item in review_libuv_calls(
                        read_json(ROOT / "validation/call-chains/dataset.json")
                    )
                )
                for decision in ("Confirmed", "Confirmed with condition", "Rejected")
            },
        )
        self.assertEqual(
            len(
                review_redis_calls(
                    read_json(ROOT / "validation/redis/call-chains.json")
                )
            ),
            120,
        )
        self.assertEqual(
            {
                "Confirmed": 23,
                "Confirmed with condition": 4,
                "Rejected": 55,
            },
            {
                decision: sum(
                    item["decision"] == decision
                    for item in review_resources(
                        read_json(ROOT / "validation/resource-flow/dataset.json")
                    )
                )
                for decision in ("Confirmed", "Confirmed with condition", "Rejected")
            },
        )
        self.assertEqual(
            sum(
                item["decision"] == "Confirmed with condition"
                for item in review_libuv_sync(
                    read_json(ROOT / "validation/sync-relations/dataset.json")
                )
            ),
            6,
        )
        self.assertEqual(
            sum(
                item["decision"] == "Confirmed with condition"
                for item in review_redis_sync(
                    read_json(ROOT / "validation/redis/sync-relations.json")
                )
            ),
            4,
        )


if __name__ == "__main__":
    unittest.main()
