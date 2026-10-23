from __future__ import annotations

import re
import shlex
import shutil
import subprocess
from collections import Counter
from pathlib import Path
from typing import Any

from .clang_ast import stable_digest


OPTIMIZATION_PATTERN = re.compile(r"^-O(?:[0-3sgz]|fast)?$")
IR_FUNCTION_PATTERN = re.compile(
    r'^define\b.*@(?:"(?P<quoted>[^"]+)"|(?P<plain>[A-Za-z0-9_.$-]+))\s*\('
)
IR_CALL_PATTERN = re.compile(
    r'\b(?:call|invoke)\b[^@]*@(?:"(?P<quoted>[^"]+)"|(?P<plain>[A-Za-z0-9_.$-]+))'
)
IGNORED_IR_PREFIXES = ("llvm.dbg.", "llvm.lifetime.", "llvm.memcpy.", "llvm.memset.")


def _arguments(unit: dict[str, Any]) -> list[str]:
    values = unit.get("arguments")
    if not values:
        values = shlex.split(unit.get("command", ""))
    return [str(item) for item in values]


def _value_after(arguments: list[str], flag: str) -> str:
    for index, value in enumerate(arguments[:-1]):
        if value == flag:
            return arguments[index + 1]
    return ""


def _joined_values(arguments: list[str], prefix: str) -> list[str]:
    values = []
    for index, value in enumerate(arguments):
        if value == prefix and index + 1 < len(arguments):
            values.append(arguments[index + 1])
        elif value.startswith(prefix):
            values.append(value[len(prefix) :])
    return values


def extract_build_profile(
    compile_commands: list[dict[str, Any]],
    repo_root: str | Path,
) -> dict[str, Any]:
    root = Path(repo_root).resolve()
    units = []
    optimizations: Counter[str] = Counter()
    standards: Counter[str] = Counter()
    sanitizers: set[str] = set()
    defines: set[str] = set()
    include_dirs: set[str] = set()
    targets: set[str] = set()
    features = {
        "lto": False,
        "debug": False,
        "fast_math": False,
        "warnings_as_errors": False,
        "rtti": True,
        "exceptions": True,
        "stack_protector": False,
    }
    for unit in compile_commands:
        arguments = _arguments(unit)
        optimization = next(
            (value for value in reversed(arguments) if OPTIMIZATION_PATTERN.match(value)),
            "default",
        )
        standard = next(
            (value for value in reversed(arguments) if value.startswith("-std=")),
            "",
        )
        target = _value_after(arguments, "-target") or _value_after(arguments, "--target")
        unit_sanitizers = _joined_values(arguments, "-fsanitize=")
        unit_defines = _joined_values(arguments, "-D")
        unit_includes = _joined_values(arguments, "-I")
        optimizations[optimization] += 1
        if standard:
            standards[standard] += 1
        sanitizers.update(unit_sanitizers)
        defines.update(unit_defines)
        include_dirs.update(unit_includes)
        if target:
            targets.add(target)
        features["lto"] = features["lto"] or "-flto" in arguments
        features["debug"] = features["debug"] or any(
            value.startswith("-g") and value != "-g0" for value in arguments
        )
        features["fast_math"] = features["fast_math"] or any(
            value in {"-ffast-math", "-Ofast"} for value in arguments
        )
        features["warnings_as_errors"] = (
            features["warnings_as_errors"] or "-Werror" in arguments
        )
        if "-fno-rtti" in arguments:
            features["rtti"] = False
        if "-fno-exceptions" in arguments:
            features["exceptions"] = False
        features["stack_protector"] = (
            features["stack_protector"]
            or any(value.startswith("-fstack-protector") for value in arguments)
        )
        file = str(unit.get("file", ""))
        path = Path(file)
        if not path.is_absolute():
            path = root / path
        units.append(
            {
                "id": "unit_" + stable_digest([file, standard, optimization])[:12],
                "file": file,
                "compiler": str(
                    unit.get("compiler")
                    or (Path(arguments[0]).name if arguments else "")
                ),
                "optimization": optimization,
                "standard": standard,
                "target": target,
                "sanitizers": sorted(set(unit_sanitizers)),
                "defines": sorted(set(unit_defines)),
                "include_dirs": sorted(set(unit_includes)),
            }
        )
    return {
        "schema_version": "1.0",
        "repo_root": str(root),
        "units": units,
        "summary": {
            "unit_count": len(units),
            "optimization": dict(optimizations),
            "standards": dict(standards),
            "targets": sorted(targets),
            "sanitizers": sorted(sanitizers),
            "defines": sorted(defines),
            "include_dirs": sorted(include_dirs),
            "features": features,
        },
    }


def _ir_arguments(unit: dict[str, Any]) -> list[str]:
    arguments = _arguments(unit)
    result = []
    index = 0
    while index < len(arguments):
        value = arguments[index]
        if value in {"-c", "-S", "-fsyntax-only"}:
            index += 1
            continue
        if value == "-o":
            index += 2
            continue
        if value.startswith("-o") and len(value) > 2:
            index += 1
            continue
        result.append(value)
        index += 1
    result += ["-S", "-emit-llvm", "-o", "-"]
    return result


def extract_llvm_calls(
    unit: dict[str, Any],
    repo_root: str | Path,
    *,
    timeout: int = 180,
) -> dict[str, Any]:
    root = Path(repo_root).resolve()
    completed = subprocess.run(
        _ir_arguments(unit),
        cwd=unit.get("directory") or str(root),
        capture_output=True,
        text=True,
        timeout=timeout,
        check=False,
    )
    if completed.returncode != 0:
        return {
            "status": "failed",
            "file": unit.get("file", ""),
            "error": completed.stderr.strip()[:2000],
            "calls": [],
        }
    current = ""
    calls = []
    for raw in completed.stdout.splitlines():
        line = raw.strip()
        defined = IR_FUNCTION_PATTERN.match(line)
        if defined:
            current = defined.group("quoted") or defined.group("plain") or ""
            continue
        call = IR_CALL_PATTERN.search(line)
        if not call or not current:
            continue
        target = call.group("quoted") or call.group("plain") or ""
        if target.startswith(IGNORED_IR_PREFIXES):
            continue
        calls.append(
            {
                "id": "ir_call_" + stable_digest([current, target, unit.get("file")])[:12],
                "function": current,
                "target": target,
                "file": unit.get("file", ""),
                "line": 0,
                "origin": "optimized_llvm_ir",
            }
        )
    return {
        "status": "succeeded",
        "file": unit.get("file", ""),
        "calls": calls,
    }


def _demangle_names(names: set[str]) -> dict[str, str]:
    if not names or not shutil.which("c++filt"):
        return {name: name for name in names}
    completed = subprocess.run(
        ["c++filt", "-n"],
        input="\n".join(sorted(names)) + "\n",
        capture_output=True,
        text=True,
        timeout=30,
        check=False,
    )
    if completed.returncode != 0:
        return {name: name for name in names}
    values = completed.stdout.splitlines()
    if len(values) != len(names):
        return {name: name for name in names}
    return dict(zip(sorted(names), values))


def _canonical_ir_name(name: str, demangled: str) -> str:
    value = demangled or name
    value = value.split("(", 1)[0].strip()
    value = re.sub(r"<[^>]+>", "", value)
    return value.rsplit("::", 1)[-1].strip() or name.removeprefix("_")


def optimized_ir_facts(
    compile_commands: list[dict[str, Any]],
    graph: dict[str, Any],
    repo_root: str | Path,
) -> dict[str, Any]:
    units = []
    ir_calls = []
    for unit in compile_commands:
        if str(unit.get("file", "")).endswith((".h", ".hpp")):
            continue
        result = extract_llvm_calls(unit, repo_root)
        units.append(result)
        ir_calls.extend(result.get("calls", []))
    names = {
        value
        for item in ir_calls
        for value in (item["function"], item["target"])
    }
    demangled = _demangle_names(names)
    for item in ir_calls:
        item["canonical_function"] = _canonical_ir_name(
            item["function"], demangled.get(item["function"], item["function"])
        )
        item["canonical_target"] = _canonical_ir_name(
            item["target"], demangled.get(item["target"], item["target"])
        )
    node_names = {
        str(node.get("id")): str(node.get("name") or "")
        for node in graph.get("nodes", [])
    }
    ast_calls = {
        (
            node_names.get(str(edge.get("source")), ""),
            node_names.get(str(edge.get("target")), ""),
        )
        for edge in graph.get("edges", [])
        if edge.get("kind") in {"direct_call", "callback_edge"}
    }
    optimized_calls = {
        (item["canonical_function"], item["canonical_target"])
        for item in ir_calls
    }
    changes = []
    for function, target in sorted(ast_calls - optimized_calls):
        if not function or not target:
            continue
        changes.append(
            {
                "id": "opt_" + stable_digest([function, target, "not_visible"])[:12],
                "kind": "inlined_or_eliminated",
                "function": function,
                "target": target,
                "detail": "AST call is not visible in optimized LLVM IR",
            }
        )
    for function, target in sorted(optimized_calls - ast_calls):
        if not function or not target or target.startswith("llvm."):
            continue
        changes.append(
            {
                "id": "opt_" + stable_digest([function, target, "introduced"])[:12],
                "kind": "introduced_by_optimization",
                "function": function,
                "target": target,
                "detail": "Call appears only after compiler lowering/optimization",
            }
        )
    return {
        "schema_version": "1.0",
        "status": "succeeded" if any(item.get("status") == "succeeded" for item in units) else "failed",
        "units": units,
        "calls": ir_calls,
        "changes": changes,
    }
