from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from clang_pipeline.nl_repo import (
    discover_compile_commands,
    extract_repo_path,
)
from clang_pipeline.pipeline import build_compile_commands


class NaturalLanguageRepositoryTests(unittest.TestCase):
    def test_extract_absolute_repository_path(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp) / "sample_repo"
            repo.mkdir()
            (repo / "main.cpp").write_text("int main() { return 0; }\n")
            question = f"请分析仓库 {repo}，看看 main 调用了谁"
            self.assertEqual(repo.resolve(), extract_repo_path(question))

    def test_invalid_explicit_path_fails_fast(self) -> None:
        with self.assertRaisesRegex(ValueError, "不存在或不是源码仓库"):
            extract_repo_path(
                "请分析仓库 /definitely/not/an/existing/repo",
                strict=True,
            )

    def test_discover_compile_commands_in_build_directory(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp) / "sample_repo"
            build = repo / "build"
            build.mkdir(parents=True)
            expected = build / "compile_commands.json"
            expected.write_text(json.dumps([]), encoding="utf-8")
            self.assertEqual(expected.resolve(), discover_compile_commands(repo))

    def test_generic_compile_commands_support_c_files(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp) / "c_repo"
            repo.mkdir()
            (repo / "main.c").write_text("int main(void) { return 0; }\n")
            commands = build_compile_commands(repo, "default", [])
            self.assertEqual(1, len(commands))
            self.assertEqual("clang", commands[0]["compiler"])
            self.assertIn("-std=c11", commands[0]["arguments"])


if __name__ == "__main__":
    unittest.main()
