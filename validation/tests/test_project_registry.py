import csv
import json
from pathlib import Path
import shutil
import tempfile
import unittest

from scripts.validation_projects import (
    ROOT,
    build_ground_truth,
    check_project,
    check_registry,
    collect_candidates,
    pin_validation_sources,
    scaffold_project,
)
from validation.benchmark import evaluate


class ValidationProjectRegistryTests(unittest.TestCase):
    def setUp(self):
        self.root = Path(tempfile.mkdtemp(prefix="validation-project-test-"))
        (self.root / "validation" / "templates").mkdir(parents=True)
        shutil.copytree(
            ROOT / "validation" / "templates" / "new-project",
            self.root / "validation" / "templates" / "new-project",
        )
        (self.root / "schemas").mkdir()
        shutil.copyfile(
            ROOT / "schemas" / "validation-benchmark.schema.json",
            self.root / "schemas" / "validation-benchmark.schema.json",
        )
        self.source_root = self.root / "repo"
        self.source_root.mkdir()
        self.source = self.source_root / "main.c"
        self.source.write_text(
            "void target();\ntarget();\nreturn;\n",
            encoding="utf-8",
        )
        self.commit = "f" * 40
        self.registry = self.root / "validation" / "projects.json"
        self.registry.write_text(
            json.dumps({"schema_version": "1.0", "projects": []}),
            encoding="utf-8",
        )
        self.predictions = self.root / "predictions"
        self.predictions.mkdir()
        evidence = [
            {
                "id": "ev1",
                "file": "main.c",
                "line": 2,
                "snippet": "target();",
            },
            {
                "id": "ev2",
                "file": "main.c",
                "line": 2,
                "snippet": "target();",
            },
            {
                "id": "ev3",
                "file": "main.c",
                "line": 2,
                "snippet": "target();",
            },
            {
                "id": "ev4",
                "file": "main.c",
                "line": 3,
                "snippet": "return;",
            },
        ]
        source_meta = {"repository": "fixture/repo", "commit": self.commit}
        self.documents = {
            "call_chain": {
                "schema_version": "1.0",
                "run_id": "run_fixture",
                "result_type": "call_chain",
                "status": "partial",
                "source": source_meta,
                "origin": "analyzer",
                "items": [
                    {
                        "id": "item-call",
                        "entry": "fn:a",
                        "direction": "caller_to_callee",
                        "nodes": [
                            {"id": "fn:a", "kind": "function", "name": "a"},
                            {"id": "fn:b", "kind": "function", "name": "b"},
                        ],
                        "edges": [
                            {
                                "id": "edge-call",
                                "source": "fn:a",
                                "target": "fn:b",
                                "kind": "direct_call",
                                "confidence": 1.0,
                                "evidence_ids": ["ev1"],
                                "status": "unconfirmed",
                            }
                        ],
                        "confidence": 1.0,
                        "evidence_ids": ["ev1"],
                        "status": "unconfirmed",
                    }
                ],
                "evidence": evidence[:1],
                "warnings": [],
            },
            "resource_flow": {
                "schema_version": "1.0",
                "run_id": "run_fixture",
                "result_type": "resource_flow",
                "status": "succeeded",
                "source": source_meta,
                "origin": "analyzer",
                "items": [
                    {
                        "id": "item-resource",
                        "resource": "rf_fixture",
                        "resource_type": "memory",
                        "operations": [
                            {
                                "id": "operation-resource",
                                "kind": "acquire",
                                "function": "a",
                                "file": "main.c",
                                "line": 2,
                                "snippet": "target();",
                                "evidence_ids": ["ev2"],
                                "confidence": 0.9,
                                "status": "unconfirmed",
                            }
                        ],
                        "confidence": 0.9,
                        "status": "unconfirmed",
                        "evidence_ids": ["ev2"],
                    }
                ],
                "evidence": evidence[1:2],
                "warnings": [],
            },
            "sync_relation": {
                "schema_version": "1.0",
                "run_id": "run_fixture",
                "result_type": "sync_relation",
                "status": "succeeded",
                "source": source_meta,
                "origin": "analyzer",
                "items": [
                    {
                        "id": "item-sync",
                        "relation_type": "happens_before",
                        "source": {
                            "function": "a",
                            "thread": None,
                            "file": "main.c",
                            "line": 2,
                            "snippet": "target();",
                            "held_locks": [],
                            "evidence_ids": ["ev3"],
                        },
                        "target": {
                            "function": "a",
                            "thread": None,
                            "file": "main.c",
                            "line": 3,
                            "snippet": "return;",
                            "held_locks": [],
                            "evidence_ids": ["ev4"],
                        },
                        "order": "happens_before",
                        "condition": "program order",
                        "execution_context": {},
                        "confidence": 0.7,
                        "evidence_ids": ["ev3", "ev4"],
                        "status": "unconfirmed",
                    }
                ],
                "evidence": evidence[2:],
                "warnings": [],
            },
        }
        filenames = {
            "call_chain": "call-chains.json",
            "resource_flow": "resource-flow.json",
            "sync_relation": "sync-relations.json",
        }
        for name, document in self.documents.items():
            (self.predictions / filenames[name]).write_text(
                json.dumps(document),
                encoding="utf-8",
            )

    def scaffold(self):
        return scaffold_project(
            project_id="fixture",
            name="Fixture",
            repository="fixture/repo",
            repository_url="https://example.com/fixture/repo.git",
            commit=self.commit,
            source_root="repo",
            root=self.root,
            registry_path=self.registry,
            template_path=self.root / "validation" / "templates" / "new-project",
        )

    def set_review_decisions(self, decisions):
        table = self.root / "validation" / "datasets" / "fixture" / "review-table.csv"
        with table.open(encoding="utf-8-sig", newline="") as stream:
            rows = list(csv.DictReader(stream))
        self.assertEqual(len(rows), 3)
        for row in rows:
            row["decision"] = decisions.get(row["candidate_id"], "Pending")
            row["notes"] = f"reviewed {row['candidate_id']}"
        with table.open("w", encoding="utf-8-sig", newline="") as stream:
            writer = csv.DictWriter(stream, fieldnames=rows[0].keys())
            writer.writeheader()
            writer.writerows(rows)

    def test_full_new_project_workflow(self):
        scaffolded = self.scaffold()
        self.assertEqual(scaffolded["status"], "not_started")
        project = self.root / "validation" / "datasets" / "fixture"
        self.assertTrue((project / "review-table.csv").is_file())

        collected = collect_candidates(
            project_id="fixture",
            predictions_dir=self.predictions,
            source_root=self.source_root,
            root=self.root,
            registry_path=self.registry,
        )
        self.assertEqual(collected["total_candidates"], 3)
        self.assertFalse(collected["warnings"])
        candidates = json.loads((project / "candidates.json").read_text(encoding="utf-8"))
        self.assertEqual(candidates["facts"][0]["evidence"][0]["file"], "main.c")

        candidate_ids = {fact["category"]: fact["id"] for fact in candidates["facts"]}
        self.set_review_decisions(
            {
                candidate_ids["call_chain"]: "Confirmed",
                candidate_ids["resource_flow"]: "Confirmed",
                candidate_ids["sync_relation"]: "Rejected",
            }
        )
        additions = {"schema_version": "1.0", "cases": [
            {
                "id": "manual_sync_missed",
                "category": "sync_relation",
                "identity": ["a", "b", "main.c", 2, "main.c", 3],
                "kind": "happens_before",
                "expected_exists": True,
                "evidence": [
                    {"file": "main.c", "line": 2, "snippet": "target();"},
                    {"file": "main.c", "line": 3, "snippet": "return;"},
                ],
                "notes": "manually added missed fact",
            }
        ]}
        (project / "gold-additions.json").write_text(json.dumps(additions), encoding="utf-8")

        built = build_ground_truth(
            project_id="fixture",
            root=self.root,
            registry_path=self.registry,
        )
        self.assertEqual(built["cases"], 4)
        self.assertEqual(built["human_review"], "confirmed")
        truth = json.loads((project / "ground-truth.json").read_text(encoding="utf-8"))
        self.assertEqual(
            {case["expected_exists"] for case in truth["cases"]},
            {True, False},
        )

        pinned = pin_validation_sources(
            project_id="fixture",
            root=self.root,
            registry_path=self.registry,
        )
        self.assertEqual(pinned["source_files"], 1)
        checked = check_project(
            project_id="fixture",
            root=self.root,
            registry_path=self.registry,
        )
        self.assertEqual(checked["status"], "passed")
        self.assertEqual(checked["human_review"], "confirmed")

        report = evaluate(truth, self.documents)
        self.assertEqual(report["categories"]["call_chain"]["tp"], 1)
        self.assertEqual(report["categories"]["resource_flow"]["tp"], 1)
        self.assertEqual(report["categories"]["sync_relation"]["fp"], 1)

        registry = check_registry(root=self.root, registry_path=self.registry)
        self.assertEqual(registry["status"], "passed")
        self.assertEqual(registry["projects"][0]["cases"], 4)


if __name__ == "__main__":
    unittest.main()
