from __future__ import annotations

import tempfile
import unittest
import shutil
from pathlib import Path

from clang_pipeline.compiler_facts import (
    extract_build_profile,
    extract_llvm_calls,
    optimized_ir_facts,
)
from clang_pipeline.knowledge_graph import build_knowledge_graph
from clang_pipeline.log_facts import collect_log_facts


class KnowledgeGraphTests(unittest.TestCase):
    @unittest.skipUnless(shutil.which("clang"), "clang is required")
    def test_optimized_ir_calls_are_extracted(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source = root / "main.c"
            source.write_text(
                "extern void sink(void);\n"
                "static void caller(void) { sink(); }\n"
                "int main(void) { caller(); return 0; }\n",
                encoding="utf-8",
            )
            result = extract_llvm_calls(
                {
                    "file": str(source),
                    "directory": str(root),
                    "arguments": ["clang", "-O2", "-c", str(source)],
                },
                root,
            )
            self.assertEqual("succeeded", result["status"])
            self.assertTrue(
                any(call["target"] == "sink" for call in result["calls"])
            )

    @unittest.skipUnless(
        shutil.which("clang++") and shutil.which("c++filt"),
        "clang++ and c++filt are required",
    )
    def test_cpp_ir_names_are_normalized_without_false_optimization_changes(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source = root / "main.cpp"
            source.write_text(
                "namespace demo {\n"
                "void foo();\n"
                "void bar() { foo(); }\n"
                "}\n",
                encoding="utf-8",
            )
            facts = optimized_ir_facts(
                [
                    {
                        "file": str(source),
                        "directory": str(root),
                        "arguments": ["clang++", "-O0", "-c", str(source)],
                    }
                ],
                {
                    "nodes": [
                        {"id": "fn:demo::bar", "kind": "function", "name": "bar"},
                        {"id": "fn:demo::foo", "kind": "function", "name": "foo"},
                    ],
                    "edges": [
                        {
                            "source": "fn:demo::bar",
                            "target": "fn:demo::foo",
                            "kind": "direct_call",
                        }
                    ],
                },
                root,
            )
            self.assertFalse(
                any(
                    change["function"] == "bar" and change["target"] == "foo"
                    for change in facts["changes"]
                )
            )

    def test_build_profile_logs_and_knowledge_graph(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source = root / "src" / "main.c"
            source.parent.mkdir()
            source.write_text(
                "int main(void) { return 0; }\n",
                encoding="utf-8",
            )
            log = root / "build.log"
            log.write_text(
                "src/main.c:1:1: warning: unused result\n"
                "function=main event=startup\n",
                encoding="utf-8",
            )
            units = [
                {
                    "file": "src/main.c",
                    "directory": str(root),
                    "arguments": [
                        "clang",
                        "-O2",
                        "-g",
                        "-std=c11",
                        "-DDEBUG=1",
                        "-Iinclude",
                        "-c",
                        "src/main.c",
                    ],
                }
            ]
            profile = extract_build_profile(units, root)
            self.assertEqual(profile["summary"]["optimization"], {"-O2": 1})
            self.assertTrue(profile["summary"]["features"]["debug"])
            logs = collect_log_facts([log], source_root=root)
            self.assertEqual(len(logs["events"]), 2)
            self.assertTrue(
                any(event["kind"] == "compiler_diagnostic" for event in logs["events"])
            )

            graph = {
                "run_id": "run_kg_test",
                "meta": {"repository": "fixture/repo", "commit": "a" * 40},
                "nodes": [
                    {
                        "id": "fn:main",
                        "kind": "function",
                        "name": "main",
                        "file": "src/main.c",
                        "line": 1,
                    }
                ],
                "edges": [],
                "evidence": [],
            }
            resource = {
                "items": [
                    {
                        "id": "rf_test",
                        "resource": "buf",
                        "resource_expression": "buf",
                        "resource_type": "memory",
                        "ownership_model": "visible_acquire_release",
                        "operations": [
                            {
                                "kind": "acquire",
                                "function": "main",
                                "file": "src/main.c",
                                "line": 1,
                            }
                        ],
                    }
                ]
            }
            sync = {
                "items": [
                    {
                        "id": "sync_test",
                        "relation_type": "mutex_lock",
                        "source": {"function": "main", "file": "src/main.c", "line": 1},
                        "target": {"function": "main", "file": "src/main.c", "line": 1},
                        "order": "happens_before",
                        "evidence_ids": ["ev"],
                    }
                ]
            }
            kg = build_knowledge_graph(
                graph,
                resource,
                sync,
                build_profile=profile,
                log_facts=logs,
            )
            self.assertGreaterEqual(kg["summary"]["entities"], 5)
            self.assertTrue(
                any(
                    relation["type"] == "uses_resource"
                    for relation in kg["relations"]
                )
            )
            self.assertTrue(
                any(
                    relation["type"] == "references_symbol"
                    for relation in kg["relations"]
                )
            )


if __name__ == "__main__":
    unittest.main()
