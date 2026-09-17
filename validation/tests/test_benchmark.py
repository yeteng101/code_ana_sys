import copy
import unittest

from jsonschema.exceptions import ValidationError
from scripts.export_validation import envelope, export_graph, reviewed_resources, reviewed_sync
from validation.benchmark import ROOT, evaluate, flatten, read, validate_external


class BenchmarkTests(unittest.TestCase):
    def setUp(self):
        self.source = {"repository": "example/repo", "commit": "a" * 40}
        self.evidence = {"id": "ev", "file": "src/example.c", "line": 2, "snippet": "b();"}
        self.edge = {"id": "edge", "source": "fn:a", "target": "fn:b", "kind": "direct_call", "confidence": 0.9, "evidence_ids": ["ev"]}
        self.graph = {"run_id": "test", "meta": self.source, "nodes": [{"id": "fn:a"}, {"id": "fn:b"}], "edges": [self.edge], "evidence": [self.evidence]}
        self.docs = export_graph(self.graph)
        self.case = {"id": "positive", "category": "call_chain", "identity": ["fn:a", "fn:b"], "kind": "direct_call", "expected_exists": True, "evidence": [self.evidence]}
        self.truth = {"schema_version": "1.0", "dataset_id": "test", **self.source, "review": {}, "cases": [self.case]}

    def score(self):
        return evaluate(self.truth, self.docs)["categories"]["call_chain"]

    def test_perfect_candidate_is_not_confirmed(self):
        m = self.score()
        self.assertEqual((m["tp"], m["fp"], m["fn"]), (1, 0, 0))
        self.assertEqual(m["f1"], 1)
        self.assertEqual(m["confirmed_only"]["recall"], 0)
        self.assertEqual(m["unconfirmed_ratio"], 1)

    def test_missing_prediction_is_false_negative(self):
        self.docs["call_chain"]["items"] = []
        m = self.score()
        self.assertEqual(m["fn"], 1)
        self.assertEqual(m["recall"], 0)
        self.assertIsNone(m["precision"])

    def test_wrong_kind_is_fp_and_fn(self):
        self.docs["call_chain"]["items"][0]["edges"][0]["kind"] = "callback_edge"
        m = self.score()
        self.assertEqual((m["tp"], m["fp"], m["fn"]), (0, 1, 1))
        self.assertEqual(m["type_accuracy"], 0)

    def test_extra_wrong_kind_lowers_type_accuracy(self):
        item = self.docs["call_chain"]["items"][0]
        item["edges"].append({**item["edges"][0], "kind": "callback_edge"})
        self.assertEqual(self.score()["type_accuracy"], 0.5)

    def test_explicit_negative(self):
        self.case["expected_exists"] = False
        self.assertEqual(self.score()["fp"], 1)

    def test_duplicates_do_not_inflate_recall(self):
        item = copy.deepcopy(self.docs["call_chain"]["items"][0])
        item["id"] = "duplicate-semantic-fact"
        self.docs["call_chain"]["items"].append(item)
        m = self.score()
        self.assertEqual(m["tp"], 1)
        self.assertEqual(m["duplicate_predictions"], 1)

    def test_unlabelled_predictions_not_assumed_false(self):
        item = copy.deepcopy(self.docs["call_chain"]["items"][0])
        item["id"] = "unlabelled"
        item["edges"][0]["source"] = "fn:other"
        item["nodes"][0]["id"] = "fn:other"
        self.docs["call_chain"]["items"].append(item)
        m = self.score()
        self.assertEqual(m["unlabelled_predictions"], 1)
        self.assertEqual(m["fp"], 0)

    def test_evidence_must_match_all_required_anchors(self):
        self.truth["cases"][0]["evidence"] = [{**self.evidence, "line": 3}]
        self.assertEqual(self.score()["evidence_hit_rate"], 0)

    def test_refuted_is_not_a_positive_prediction(self):
        self.docs["call_chain"]["items"][0]["edges"][0]["status"] = "refuted"
        self.assertEqual(self.score()["fn"], 1)

    def test_verification_verdict_not_confidence_controls_confirmation(self):
        self.docs = export_graph(self.graph, {"checks": [{"claim": "edge: source matches", "result": "confirmed"}]})
        self.assertEqual(self.score()["confirmed_only"]["recall"], 1)

    def test_invalid_inputs_fail(self):
        for mutation in [lambda: self.truth["cases"].append(copy.deepcopy(self.case)),
                         lambda: self.docs["call_chain"]["source"].update(commit="b" * 40),
                         lambda: self.docs["call_chain"]["items"][0].update(evidence_ids=["missing"]),
                         lambda: self.docs["call_chain"]["items"][0].pop("status"),
                         lambda: self.docs["call_chain"]["items"][0].update(confidence=2)]:
            self.setUp()
            mutation()
            with self.assertRaises((ValueError, ValidationError)):
                self.score()

    def test_resource_and_sync_adapters_are_explicitly_reviewed(self):
        reviewed_resources(read(ROOT / "validation/resource-flow/dataset.json"), self.docs["resource_flow"])
        reviewed_sync(read(ROOT / "validation/sync-relations/dataset.json"), self.docs["sync_relation"])
        for category in ("resource_flow", "sync_relation"):
            doc = self.docs[category]
            validate_external(doc, category)
            self.assertIn("not_analyzer", doc["origin"])
            self.assertGreater(len(flatten(doc, category)), 0)
        facts = flatten(self.docs["sync_relation"], "sync_relation")
        unknown = next(f for f in facts if f["kind"] == "unknown")
        self.assertEqual(unknown["status"], "unconfirmed")
        self.assertTrue(unknown["identity"][-1])

    def test_resource_and_sync_scoring(self):
        for category, source in [("resource_flow", "resource-flow/dataset.json"),
                                 ("sync_relation", "sync-relations/dataset.json")]:
            with self.subTest(category=category):
                doc = self.docs[category]
                adapter = reviewed_resources if category == "resource_flow" else reviewed_sync
                adapter(read(ROOT / "validation" / source), doc)
                facts = flatten(doc, category)
                fact = facts[0]
                case = {"id": "semantic-fact", "category": category, "identity": fact["identity"],
                        "kind": fact["kind"], "evidence": [e.get("location", e) for e in fact["evidence"]],
                        "expected_exists": True}
                truth = {**self.truth, "cases": [case]}
                m = evaluate(truth, self.docs)["categories"][category]
                self.assertEqual((m["tp"], m["fp"], m["fn"], m["evidence_hit_rate"]), (1, 0, 0, 1))


if __name__ == "__main__":
    unittest.main()
