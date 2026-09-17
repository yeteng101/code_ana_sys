import copy
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from scripts.check_sync_validation import ROOT, check_dataset


class SyncValidationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = json.loads((ROOT / "validation/sync-relations/dataset.json").read_text(encoding="utf-8"))

    def check(self, mutate=lambda data: None, root=ROOT):
        data = copy.deepcopy(self.data)
        mutate(data)
        with tempfile.TemporaryDirectory() as directory:
            dataset = Path(directory) / "dataset.json"
            dataset.write_text(json.dumps(data), encoding="utf-8")
            return check_dataset(dataset, root)

    def test_curated_dataset(self):
        summary, errors = self.check()
        self.assertEqual(errors, [])
        self.assertEqual(summary["samples"], 32)

    def test_missing_source_fails_closed(self):
        with tempfile.TemporaryDirectory() as directory:
            _, errors = self.check(root=Path(directory))
        self.assertTrue(any("missing source" in error for error in errors))

    def test_wrong_checkout(self):
        with patch("scripts.check_sync_validation.subprocess.run") as run:
            run.return_value.returncode = 0
            run.return_value.stdout = "0" * 40
            _, errors = self.check()
        self.assertTrue(any("HEAD" in error for error in errors))

    def test_tampered_hash(self):
        _, errors = self.check(lambda d: d["source_files"].update({next(iter(d["source_files"])): "0" * 64}))
        self.assertTrue(any("hash mismatch" in error for error in errors))

    def test_bad_annotations(self):
        mutations = {
            "duplicate sample": lambda d: d["samples"].append(d["samples"][0]),
            "duplicate evidence": lambda d: d["samples"][0]["evidence"].append(d["samples"][0]["evidence"][0]),
            "dangling": lambda d: d["samples"][0]["source"].update(evidence_ids=["missing"]),
            "snippet": lambda d: d["samples"][0]["evidence"][0].update(snippet="invented();"),
            "line": lambda d: d["samples"][0]["evidence"][0].update(line=999999),
            "positive": lambda d: d["samples"][3].update(label="positive"),
            "negative": lambda d: d["samples"][0].update(label="negative"),
            "classification": lambda d: d["samples"][0].update(classification="unknown"),
            "schema": lambda d: d["samples"][0].pop("condition"),
            "unknown file": lambda d: d["samples"][0]["evidence"][0].update(file="third_party/libuv/src/missing.c"),
            "traversal": lambda d: d["source_files"].update({"../outside": "0" * 64}),
            "empty dataset": lambda d: d.update(samples=[]),
        }
        for name, mutate in mutations.items():
            with self.subTest(name=name):
                _, errors = self.check(mutate)
                self.assertTrue(errors, name)


if __name__ == "__main__":
    unittest.main()
