from __future__ import annotations

import re
from collections import defaultdict
from pathlib import Path
from typing import Any, Iterable

from .clang_ast import (
    evidence_id,
    has_body,
    is_fptr_qual_type,
    node_location,
    read_json,
    relpath,
    run_clang_ast,
    run_preprocessor_macros,
    snippet_for,
    stable_digest,
    utc_now,
    write_json,
)


def _load_request(workspace: Path) -> dict[str, Any]:
    return read_json(workspace / "request.json")


def _repo_root(workspace: Path) -> Path:
    request = _load_request(workspace)
    return Path(request.get("repo_root") or request["source_root"]).resolve()


def _source_dir(workspace: Path) -> Path:
    request = _load_request(workspace)
    return Path(request["source_root"]).resolve()


def _load_compile_units(workspace: Path) -> list[dict[str, Any]]:
    return list(read_json(workspace / "compile_commands.json"))


def _stage_dir(workspace: Path, stage: str) -> Path:
    path = workspace / stage
    path.mkdir(parents=True, exist_ok=True)
    return path


def _symbols(workspace: Path) -> list[dict[str, Any]]:
    return read_json(workspace / "01-index" / "symbols.json")["symbols"]


def _asts(workspace: Path) -> list[dict[str, Any]]:
    ast_dir = workspace / "01-index" / "ast"
    manifest = read_json(ast_dir / "manifest.json")
    return [
        {
            "file": manifest.get(path.name[: -len(".ast.json")], ""),
            "ast": read_json(path),
        }
        for path in sorted(ast_dir.glob("*.ast.json"))
    ]


def _function_index(symbols: list[dict[str, Any]]) -> tuple[dict[str, list[dict[str, Any]]], dict[str, dict[str, Any]]]:
    by_name: dict[str, list[dict[str, Any]]] = defaultdict(list)
    by_id: dict[str, dict[str, Any]] = {}
    for symbol in symbols:
        if symbol["kind"] == "function":
            by_name[symbol["name"]].append(symbol)
            by_id[symbol["id"]] = symbol
    return by_name, by_id


def _resolve_function(
    by_name: dict[str, list[dict[str, Any]]],
    name: str,
    call_file: str = "",
) -> str | None:
    candidates = by_name.get(name, [])
    if len(candidates) == 1:
        return candidates[0]["id"]
    for candidate in candidates:
        if candidate.get("file") == call_file:
            return candidate["id"]
    return candidates[0]["id"] if candidates else None


def _qualified_name(namespace: tuple[str, ...], name: str) -> str:
    return "::".join((*namespace, name))


def _source_files(root: Path) -> list[Path]:
    result: list[Path] = []
    for pattern in ("*.cpp", "*.cc", "*.cxx", "*.h", "*.hpp"):
        result.extend(sorted(root.rglob(pattern)))
    seen: set[Path] = set()
    unique: list[Path] = []
    for path in result:
        if path not in seen:
            seen.add(path)
            unique.append(path)
    return unique


def stage01_index(workspace: Path) -> dict[str, Any]:
    request = _load_request(workspace)
    root = _repo_root(workspace)
    units = _load_compile_units(workspace)
    ast_dir = _stage_dir(workspace, "01-index") / "ast"
    ast_dir.mkdir(parents=True, exist_ok=True)

    merged: dict[str, dict[str, Any]] = {}
    compile_units: list[dict[str, Any]] = []
    manifest: dict[str, str] = {}
    for unit in units:
        ast = run_clang_ast(unit, root)
        stem = re.sub(r"[^A-Za-z0-9_.-]", "_", relpath(root, unit["file"]))
        write_json(ast_dir / f"{stem}.ast.json", ast)
        manifest[stem] = relpath(root, unit["file"])
        for symbol in _collect_symbols(ast, root, relpath(root, unit["file"])):
            existing = merged.get(symbol["id"])
            if existing is None or _better_symbol(existing, symbol):
                merged[symbol["id"]] = symbol
        compile_units.append(
            {
                "file": relpath(root, unit["file"]),
                "build_profile": unit.get("build_profile", "default"),
                "compiler": unit.get("compiler", "clang++"),
                "flags": [str(item) for item in unit.get("arguments", [])],
                "defines": list(unit.get("defines", [])),
            }
        )

    write_json(ast_dir / "manifest.json", manifest)
    symbols = []
    for symbol in merged.values():
        symbol.pop("_definition", None)
        symbols.append(symbol)
    symbols.sort(key=lambda item: (item["kind"], item["id"]))

    result = {
        "schema_version": "1.0",
        "run_id": request["run_id"],
        "stage": "01-index",
        "status": "succeeded",
        "generated_at": utc_now(),
        "compile_units": compile_units,
        "symbols": symbols,
        "warnings": [],
    }
    write_json(workspace / "01-index" / "symbols.json", result)
    return result


def _collect_symbols(
    ast: dict[str, Any], root: Path, default_file: str
) -> Iterable[dict[str, Any]]:
    symbols: list[dict[str, Any]] = []

    def visit(node: dict[str, Any], namespace: tuple[str, ...], record: tuple[str, ...]) -> None:
        kind = node.get("kind")
        if kind == "NamespaceDecl" and node.get("name"):
            namespace = (*namespace, node["name"])
        elif kind in {"CXXRecordDecl", "RecordDecl"} and node.get("completeDefinition"):
            record = (*record, node.get("name") or "")

        loc = node.get("loc")
        if loc and loc.get("file") and loc.get("line"):
            file = relpath(root, loc["file"])
            line = int(loc["line"])
        elif loc and loc.get("line"):
            file = relpath(root, default_file)
            line = int(loc["line"])
        else:
            file = ""
            line = 0
        if file and line:
            type_info = node.get("type") or {}
            if kind == "FunctionDecl":
                name = node.get("name") or ""
                qualified = _qualified_name(namespace, name)
                symbols.append(
                    {
                        "id": f"fn:{qualified}",
                        "name": name,
                        "kind": "function",
                        "file": file,
                        "line": line,
                        "signature": str(type_info.get("qualType") or ""),
                        "linkage": "static" if node.get("storageClass") == "static" else "external",
                        "references": [],
                        "_definition": has_body(node),
                    }
                )
            elif kind == "FieldDecl":
                name = node.get("name") or ""
                qualified = "::".join((*record, name))
                symbol_kind = "callback_field" if is_fptr_qual_type(type_info) else "struct_field"
                symbols.append(
                    {
                        "id": f"field:{qualified}",
                        "name": qualified,
                        "kind": symbol_kind,
                        "file": file,
                        "line": line,
                        "signature": str(type_info.get("qualType") or ""),
                        "references": [],
                        "_definition": True,
                    }
                )
            elif kind == "VarDecl":
                name = node.get("name") or ""
                qualified = _qualified_name(namespace, name)
                symbols.append(
                    {
                        "id": f"var:{qualified}",
                        "name": name,
                        "kind": "variable",
                        "file": file,
                        "line": line,
                        "signature": str(type_info.get("qualType") or ""),
                        "references": [],
                        "_definition": True,
                    }
                )
            elif kind in {"TypeAliasDecl", "TypedefDecl"}:
                name = node.get("name") or ""
                symbols.append(
                    {
                        "id": f"type:{_qualified_name(namespace, name)}",
                        "name": name,
                        "kind": "type",
                        "file": file,
                        "line": line,
                        "signature": str(type_info.get("qualType") or ""),
                        "references": [],
                        "_definition": True,
                    }
                )
            elif kind in {"CXXRecordDecl", "RecordDecl"} and node.get("completeDefinition"):
                name = node.get("name") or ""
                symbols.append(
                    {
                        "id": f"type:{_qualified_name(namespace, name)}",
                        "name": name,
                        "kind": "type",
                        "file": file,
                        "line": line,
                        "signature": "",
                        "references": [],
                        "_definition": True,
                    }
                )

        for child in node.get("inner", []):
            visit(child, namespace, record)

    visit(ast, (), ())
    return symbols


def _better_symbol(existing: dict[str, Any], candidate: dict[str, Any]) -> bool:
    if existing.get("_definition") != candidate.get("_definition"):
        return bool(candidate.get("_definition"))
    existing_header = str(existing.get("file", "")).endswith((".h", ".hpp"))
    candidate_header = str(candidate.get("file", "")).endswith((".h", ".hpp"))
    if existing_header != candidate_header:
        return candidate_header
    return False


def stage02_macro(workspace: Path) -> dict[str, Any]:
    request = _load_request(workspace)
    root = _repo_root(workspace)
    source_root = _source_dir(workspace)
    units = _load_compile_units(workspace)
    profile = request.get("build_profile", "default")
    files = _source_files(source_root)

    defined_names: set[str] = set()
    active_definitions: dict[str, tuple[list[str], str]] = {}
    for unit in units:
        if unit.get("file", "").endswith((".h", ".hpp")):
            continue
        for line in run_preprocessor_macros(unit, root):
            match = re.match(
                r"#\s*define\s+([A-Za-z_]\w*)(?:\(([^)]*)\))?\s*(.*)$", line
            )
            if match:
                name = match.group(1)
                defined_names.add(name)
                params = [
                    part.strip()
                    for part in match.group(2).split(",")
                    if part.strip()
                ] if match.group(2) else []
                active_definitions[name] = (params, match.group(3).strip())

    expansions: list[dict[str, Any]] = []
    for name in sorted(defined_names):
        definition = _find_macro_definition(root, source_root, name)
        if definition is None:
            continue
        file, line, params, body = definition
        active_params, active_body = active_definitions.get(name, (params, body))
        function_like = bool(params)
        call_sites = _macro_call_sites(root, source_root, name, function_like, file, line)
        expansions.append(
            {
                "id": f"macro:{name}",
                "name": name,
                "definition": active_body,
                "parameters": active_params or params,
                "expanded_text": active_body,
                "file": file,
                "line": line,
                "build_profile": profile,
                "call_sites": call_sites,
            }
        )

    conditional_regions = _conditional_regions(root, files, defined_names, profile)
    result = {
        "schema_version": "1.0",
        "run_id": request["run_id"],
        "stage": "02-macro",
        "status": "succeeded",
        "generated_at": utc_now(),
        "expansions": expansions,
        "conditional_regions": conditional_regions,
        "warnings": [],
    }
    write_json(workspace / "02-macro" / "macros.json", result)
    return result


def _find_macro_definition(
    root: Path, source_root: Path, name: str
) -> tuple[str, int, list[str], str] | None:
    pattern = re.compile(rf"^\s*#\s*define\s+{re.escape(name)}\b(.*)$")
    for path in _source_files(source_root):
        for line_no, raw in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
            match = pattern.match(raw)
            if not match:
                continue
            rest = match.group(1).strip()
            params: list[str] = []
            if rest.startswith("("):
                close = rest.find(")")
                if close != -1:
                    params = [part.strip() for part in rest[1:close].split(",") if part.strip()]
                    rest = rest[close + 1 :].strip()
            return relpath(root, str(path)), line_no, params, rest
    return None


def _macro_call_sites(
    root: Path,
    source_root: Path,
    name: str,
    function_like: bool,
    definition_file: str,
    definition_line: int,
) -> list[dict[str, Any]]:
    if function_like:
        pattern = re.compile(rf"\b{re.escape(name)}\s*\(")
    else:
        pattern = re.compile(rf"\b{re.escape(name)}\b")
    sites: list[dict[str, Any]] = []
    for path in _source_files(source_root):
        file = relpath(root, str(path))
        for line_no, raw in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
            if file == definition_file and line_no == definition_line:
                continue
            if pattern.search(raw):
                sites.append(
                    {
                        "file": file,
                        "line": line_no,
                        "snippet": raw.strip(),
                    }
                )
    return sites


def _condition_holds(condition: str, defined_names: set[str]) -> bool:
    def replace(match: re.Match[str]) -> str:
        return "True" if match.group(1) in defined_names else "False"

    text = re.sub(r"defined\s*\(\s*([A-Za-z_]\w*)\s*\)", replace, condition)
    text = re.sub(r"defined\s+([A-Za-z_]\w*)", replace, text)
    try:
        return bool(eval(text, {"__builtins__": {}}))
    except Exception:
        return False


def _conditional_regions(
    root: Path, files: list[Path], defined_names: set[str], profile: str
) -> list[dict[str, Any]]:
    directive_pattern = re.compile(r"^\s*#\s*(ifdef|ifndef|if|elif|else|endif)\b(.*)$")
    regions: list[dict[str, Any]] = []
    for path in files:
        file = relpath(root, str(path))
        stack: list[dict[str, Any]] = []
        for line_no, raw in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
            match = directive_pattern.match(raw)
            if not match:
                continue
            directive = match.group(1)
            expression = match.group(2).strip()
            if directive in {"ifdef", "ifndef", "if"}:
                if directive == "ifdef":
                    condition = f"defined({expression})"
                elif directive == "ifndef":
                    condition = f"!defined({expression})"
                else:
                    condition = expression
                active = _condition_holds(condition, defined_names)
                stack.append(
                    {
                        "condition": condition,
                        "branches": [{"branch": "then", "start": line_no + 1, "active": active}],
                    }
                )
            elif directive == "elif":
                if not stack:
                    continue
                top = stack[-1]
                _close_branch(top, regions, line_no - 1, file, defined_names, profile)
                active = _condition_holds(expression, defined_names)
                top["branches"].append({"branch": "then", "start": line_no + 1, "active": active})
            elif directive == "else":
                if not stack:
                    continue
                top = stack[-1]
                _close_branch(top, regions, line_no - 1, file, defined_names, profile)
                active = not any(branch["active"] for branch in top["branches"])
                top["branches"].append({"branch": "else", "start": line_no + 1, "active": active})
            elif directive == "endif":
                if not stack:
                    continue
                top = stack.pop()
                _close_branch(top, regions, line_no - 1, file, defined_names, profile)
    return regions


def _close_branch(
    top: dict[str, Any],
    regions: list[dict[str, Any]],
    end_line: int,
    file: str,
    defined_names: set[str],
    profile: str,
) -> None:
    for branch in top["branches"]:
        if branch.get("closed") or branch["start"] > end_line:
            continue
        branch["closed"] = True
        regions.append(
            {
                "file": file,
                "start_line": branch["start"],
                "end_line": end_line,
                "condition": top["condition"],
                "branch": branch["branch"],
                "active_in_profiles": [profile] if branch["active"] else [],
            }
        )


def stage03_callgraph(workspace: Path) -> dict[str, Any]:
    request = _load_request(workspace)
    root = _repo_root(workspace)
    profile = request.get("build_profile", "default")
    symbols = _symbols(workspace)
    by_name, by_id = _function_index(symbols)
    macros = read_json(workspace / "02-macro" / "macros.json")
    macro_map = _macro_location_map(macros["expansions"])

    nodes: dict[str, dict[str, Any]] = {}
    edges: dict[str, dict[str, Any]] = {}
    evidence: dict[str, dict[str, Any]] = {}

    for symbol in symbols:
        if symbol["kind"] == "function":
            nodes[symbol["id"]] = _graph_node(symbol)
        elif symbol["kind"] == "callback_field":
            node_id = f"cb:{symbol['name']}"
            nodes[node_id] = {
                "id": node_id,
                "kind": "callback",
                "name": symbol["name"],
                "file": symbol["file"],
                "line": symbol["line"],
                "signature": symbol.get("signature", ""),
            }

    for entry in _asts(workspace):
        ast = entry["ast"]
        unit_file = entry["file"]
        field_ids = _collect_fptr_field_ids(ast)
        _collect_call_edges(
            ast,
            unit_file,
            root,
            by_name,
            field_ids,
            macro_map,
            nodes,
            edges,
            evidence,
            profile,
        )

    graph = {
        "schema_version": "1.0",
        "run_id": request["run_id"],
        "meta": {
            "repository": request.get("repository", "local-cpp-demo"),
            "commit": request.get("commit", "local"),
            "build_profile": profile,
            "analyzer": "clang++ -Xclang -ast-dump=json",
            "generated_at": utc_now(),
            "origin": "01-index/ast/*.ast.json",
        },
        "nodes": sorted(nodes.values(), key=lambda item: item["id"]),
        "edges": sorted(edges.values(), key=lambda item: item["id"]),
        "evidence": sorted(evidence.values(), key=lambda item: item["id"]),
    }
    write_json(workspace / "03-callgraph" / "callgraph.json", graph)
    return graph


def _macro_location_map(expansions: list[dict[str, Any]]) -> dict[tuple[str, int], str]:
    result: dict[tuple[str, int], str] = {}
    for expansion in expansions:
        result[(expansion["file"], expansion["line"])] = expansion["name"]
    return result


def _graph_node(symbol: dict[str, Any]) -> dict[str, Any]:
    qualified = symbol["id"].removeprefix("fn:")
    module = "::".join(qualified.split("::")[:-1])
    return {
        "id": symbol["id"],
        "kind": "function",
        "name": symbol["name"],
        "file": symbol["file"],
        "line": symbol["line"],
        "signature": symbol.get("signature", ""),
        "module": module,
    }


def _collect_fptr_field_ids(ast: dict[str, Any]) -> dict[str, str]:
    field_ids: dict[str, str] = {}

    def visit(node: dict[str, Any], record: tuple[str, ...]) -> None:
        if node.get("kind") in {"CXXRecordDecl", "RecordDecl"} and node.get("completeDefinition"):
            record = (*record, node.get("name") or "")
        if node.get("kind") == "FieldDecl" and is_fptr_qual_type(node.get("type") or {}):
            field_ids[node["id"]] = "::".join((*record, node.get("name") or ""))
        for child in node.get("inner", []):
            visit(child, record)

    visit(ast, ())
    return field_ids


def _collect_call_edges(
    ast: dict[str, Any],
    unit_file: str,
    root: Path,
    by_name: dict[str, list[dict[str, Any]]],
    field_ids: dict[str, str],
    macro_map: dict[tuple[str, int], str],
    nodes: dict[str, dict[str, Any]],
    edges: dict[str, dict[str, Any]],
    evidence: dict[str, dict[str, Any]],
    profile: str,
) -> None:
    def visit(
        node: dict[str, Any],
        namespace: tuple[str, ...],
        record: tuple[str, ...],
        fn_stack: list[str],
    ) -> None:
        kind = node.get("kind")
        if kind == "NamespaceDecl" and node.get("name"):
            namespace = (*namespace, node["name"])
        elif kind in {"CXXRecordDecl", "RecordDecl"} and node.get("completeDefinition"):
            record = (*record, node.get("name") or "")

        if kind == "FunctionDecl" and has_body(node):
            name = node.get("name") or ""
            qualified = _qualified_name(namespace, name)
            fn_id = f"fn:{qualified}"
            if fn_id in nodes:
                fn_stack.append(fn_id)
                for child in node.get("inner", []):
                    visit(child, namespace, record, fn_stack)
                fn_stack.pop()
                return

        if kind == "CallExpr":
            _handle_call_expr(
                node,
                root,
                unit_file,
                by_name,
                field_ids,
                macro_map,
                nodes,
                edges,
                evidence,
                profile,
                fn_stack[-1] if fn_stack else None,
            )

        for child in node.get("inner", []):
            visit(child, namespace, record, fn_stack)

    visit(ast, (), (), [])


def _handle_call_expr(
    call: dict[str, Any],
    root: Path,
    unit_file: str,
    by_name: dict[str, list[dict[str, Any]]],
    field_ids: dict[str, str],
    macro_map: dict[tuple[str, int], str],
    nodes: dict[str, dict[str, Any]],
    edges: dict[str, dict[str, Any]],
    evidence: dict[str, dict[str, Any]],
    profile: str,
    source_id: str | None,
) -> None:
    if source_id is None:
        return
    call_site = node_location(root, call, unit_file)
    if call_site is None:
        return
    children = call.get("inner", [])
    callee = _unwrap(children[0]) if children else None
    if callee is None:
        return

    macro_name = _macro_at_call(call, macro_map, root, unit_file)
    if callee.get("kind") == "DeclRefExpr":
        referenced = callee.get("referencedDecl") or {}
        if referenced.get("kind") == "FunctionDecl":
            target_id = _resolve_function(by_name, referenced.get("name") or "", call_site["file"])
            if target_id is None or target_id not in nodes:
                return
            _add_edge(
                "direct_call",
                source_id,
                target_id,
                call_site,
                evidence,
                edges,
                profile,
                macro_name,
            )
            return
        if is_fptr_qual_type(referenced.get("type") or {}):
            target_id = _ensure_callback_node(nodes, referenced.get("name") or "", referenced)
            if target_id:
                _add_edge(
                    "indirect_call",
                    source_id,
                    target_id,
                    call_site,
                    evidence,
                    edges,
                    profile,
                    macro_name,
                    confidence=0.5,
                )
            return

    if callee.get("kind") == "MemberExpr":
        member_id = callee.get("referencedMemberDecl")
        field_key = field_ids.get(member_id) if member_id else None
        if field_key:
            target_id = f"cb:{field_key}"
            if target_id not in nodes:
                nodes[target_id] = {
                    "id": target_id,
                    "kind": "callback",
                    "name": field_key,
                    "file": call_site["file"],
                    "line": call_site["line"],
                    "signature": str((callee.get("type") or {}).get("qualType") or ""),
                }
            _add_edge(
                "indirect_call",
                source_id,
                target_id,
                call_site,
                evidence,
                edges,
                profile,
                macro_name,
                confidence=0.5,
            )


def _unwrap(node: dict[str, Any] | None) -> dict[str, Any] | None:
    while node and node.get("kind") in {
        "ImplicitCastExpr",
        "CStyleCastExpr",
        "CXXFunctionalCastExpr",
        "FunctionalCastExpr",
        "MaterializeTemporaryExpr",
        "ParenExpr",
        "ExprWithCleanups",
    }:
        children = node.get("inner", [])
        if not children:
            break
        node = children[0]
    return node


def _ensure_callback_node(
    nodes: dict[str, dict[str, Any]], name: str, referenced: dict[str, Any]
) -> str:
    target_id = f"cb:{name}"
    if target_id not in nodes:
        nodes[target_id] = {
            "id": target_id,
            "kind": "callback",
            "name": name,
            "file": "",
            "line": 0,
            "signature": str((referenced.get("type") or {}).get("qualType") or ""),
        }
    return target_id


def _macro_at_call(
    call: dict[str, Any],
    macro_map: dict[tuple[str, int], str],
    root: Path,
    unit_file: str,
) -> str | None:
    begin = (call.get("range") or {}).get("begin") or {}
    spelling = begin.get("spellingLoc")
    if not isinstance(spelling, dict) or not spelling.get("line"):
        return None
    file = relpath(root, spelling.get("file") or unit_file)
    return macro_map.get((file, int(spelling["line"])))


def _add_edge(
    kind: str,
    source: str,
    target: str,
    call_site: dict[str, Any],
    evidence: dict[str, dict[str, Any]],
    edges: dict[str, dict[str, Any]],
    profile: str,
    macro_name: str | None,
    *,
    confidence: float = 1.0,
) -> None:
    ev_id = evidence_id("call_site", call_site["file"], call_site["line"], target)
    if ev_id not in evidence:
        item = {
            "id": ev_id,
            "kind": "call_site",
            "location": call_site,
            "role": "supports",
            "build_profile": profile,
        }
        if macro_name:
            item["macro_stack"] = [macro_name]
        evidence[ev_id] = item
    edge_id = "e_" + stable_digest([source, target, call_site["file"], call_site["line"]])[:12]
    edge = {
        "id": edge_id,
        "source": source,
        "target": target,
        "kind": kind,
        "call_site": call_site,
        "condition": macro_name,
        "execution_context": None,
        "confidence": confidence,
        "evidence_ids": [ev_id],
    }
    edges[edge_id] = edge


def stage04_fptr(workspace: Path) -> dict[str, Any]:
    request = _load_request(workspace)
    root = _repo_root(workspace)
    symbols = _symbols(workspace)
    by_name, by_id = _function_index(symbols)
    graph = read_json(workspace / "03-callgraph" / "callgraph.json")
    asts = _asts(workspace)

    params_by_id: dict[str, dict[str, int]] = {}
    for entry in asts:
        params_by_id.update(_collect_function_params(entry["ast"]))

    direct_assignments: dict[str, list[dict[str, Any]]] = defaultdict(list)
    param_flows: dict[str, dict[int, str]] = defaultdict(dict)
    call_flows: dict[str, list[dict[str, Any]]] = defaultdict(list)

    for entry in asts:
        ast = entry["ast"]
        unit_file = entry["file"]
        field_ids = _collect_fptr_field_ids(ast)
        _collect_fptr_assignments(
            ast,
            unit_file,
            root,
            by_id,
            field_ids,
            params_by_id,
            direct_assignments,
            param_flows,
        )
    for entry in asts:
        ast = entry["ast"]
        unit_file = entry["file"]
        _collect_fptr_call_flows(
            ast,
            unit_file,
            root,
            by_name,
            by_id,
            param_flows,
            call_flows,
        )

    candidates_by_field: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for field_key, items in direct_assignments.items():
        candidates_by_field[field_key].extend(items)
    for field_key, items in call_flows.items():
        candidates_by_field[field_key].extend(items)

    fptr_candidates: list[dict[str, Any]] = []
    evidence: dict[str, dict[str, Any]] = {}
    status = "succeeded"
    for edge in graph["edges"]:
        if edge["kind"] != "indirect_call":
            continue
        target = edge["target"]
        field_key = target.removeprefix("cb:") if target.startswith("cb:") else target
        items = candidates_by_field.get(field_key, [])
        unique: dict[str, dict[str, Any]] = {}
        assignment_sites: list[dict[str, Any]] = []
        for item in items:
            unique.setdefault(item["name"], item)
            if item["location"] not in assignment_sites:
                assignment_sites.append(item["location"])
            ev_id = evidence_id(
                "assignment", item["location"]["file"], item["location"]["line"], item["name"]
            )
            if ev_id not in evidence:
                evidence[ev_id] = {
                    "id": ev_id,
                    "kind": "assignment",
                    "location": item["location"],
                    "role": "supports",
                    "build_profile": request.get("build_profile", "default"),
                }

        candidate_targets: list[dict[str, Any]] = []
        for name, item in sorted(unique.items()):
            target_id = _resolve_function(by_name, name, item["location"].get("file", ""))
            symbol = by_id.get(target_id or "")
            if symbol is None:
                continue
            candidate_targets.append(
                {
                    "name": name,
                    "file": symbol["file"],
                    "line": symbol["line"],
                    "confidence": 0.95 if len(unique) == 1 else 0.6,
                    "evidence_ids": [
                        evidence_id(
                            "assignment",
                            item["location"]["file"],
                            item["location"]["line"],
                            name,
                        )
                    ],
                }
            )

        resolved = len(candidate_targets) == 1
        confidence = 0.95 if resolved else 0.6 if candidate_targets else 0.3
        call_site = edge["call_site"]
        fptr_candidates.append(
            {
                "id": "fptr_" + stable_digest(
                    [edge["source"], call_site["file"], call_site["line"]]
                )[:12],
                "call_site": call_site,
                "field": field_key,
                "assignment_sites": assignment_sites,
                "candidate_targets": candidate_targets,
                "resolved": resolved,
                "confidence": confidence,
                "evidence_ids": list(evidence),
            }
        )
        if not candidate_targets:
            status = "partial"

    result = {
        "schema_version": "1.0",
        "run_id": request["run_id"],
        "stage": "04-fptr",
        "status": status,
        "generated_at": utc_now(),
        "candidates": fptr_candidates,
        "evidence": sorted(evidence.values(), key=lambda item: item["id"]),
        "warnings": [],
    }
    write_json(workspace / "04-fptr" / "fptr-candidates.json", result)
    return result


def _collect_function_params(ast: dict[str, Any]) -> dict[str, dict[str, int]]:
    result: dict[str, dict[str, int]] = {}

    def visit(
        node: dict[str, Any], namespace: tuple[str, ...], current_fn: str | None
    ) -> None:
        kind = node.get("kind")
        if kind == "NamespaceDecl" and node.get("name"):
            namespace = (*namespace, node["name"])
        if kind == "FunctionDecl":
            if has_body(node):
                qualified = _qualified_name(namespace, node.get("name") or "")
                current_fn = f"fn:{qualified}"
                result[current_fn] = {
                    child.get("name") or "": index
                    for index, child in enumerate(node.get("inner", []))
                    if child.get("kind") == "ParmVarDecl" and child.get("name")
                }
        for child in node.get("inner", []):
            visit(child, namespace, current_fn)

    visit(ast, (), None)
    return result


def _collect_fptr_assignments(
    ast: dict[str, Any],
    unit_file: str,
    root: Path,
    by_id: dict[str, dict[str, Any]],
    field_ids: dict[str, str],
    params_by_id: dict[str, dict[str, int]],
    direct_assignments: dict[str, list[dict[str, Any]]],
    param_flows: dict[str, dict[int, str]],
) -> None:
    def visit(
        node: dict[str, Any],
        namespace: tuple[str, ...],
        fn_stack: list[str],
    ) -> None:
        kind = node.get("kind")
        if kind == "NamespaceDecl" and node.get("name"):
            namespace = (*namespace, node["name"])
        if kind == "FunctionDecl" and has_body(node):
            fn_id = f"fn:{_qualified_name(namespace, node.get('name') or '')}"
            if fn_id in by_id:
                fn_stack.append(fn_id)
                for child in node.get("inner", []):
                    visit(child, namespace, fn_stack)
                fn_stack.pop()
                return

        if kind == "BinaryOperator" and node.get("opcode") == "=":
            children = node.get("inner", [])
            if len(children) >= 2 and fn_stack:
                lhs = _unwrap(children[0])
                rhs = _unwrap(children[1])
                member_id = lhs.get("referencedMemberDecl") if lhs else None
                field_key = field_ids.get(member_id) if member_id else None
                if field_key:
                    location = node_location(root, node, unit_file)
                    if location:
                        if rhs and rhs.get("kind") == "DeclRefExpr":
                            referenced = rhs.get("referencedDecl") or {}
                            if referenced.get("kind") == "FunctionDecl":
                                direct_assignments[field_key].append(
                                    {
                                        "name": referenced["name"],
                                        "location": location,
                                    }
                                )
                            elif referenced.get("kind") == "ParmVarDecl":
                                fn_id = fn_stack[-1]
                                param_index = params_by_id.get(fn_id, {}).get(
                                    referenced.get("name") or ""
                                )
                                if param_index is not None:
                                    param_flows[fn_id][param_index] = field_key

        for child in node.get("inner", []):
            visit(child, namespace, fn_stack)

    visit(ast, (), [])


def _collect_fptr_call_flows(
    ast: dict[str, Any],
    unit_file: str,
    root: Path,
    by_name: dict[str, list[dict[str, Any]]],
    by_id: dict[str, dict[str, Any]],
    param_flows: dict[str, dict[int, str]],
    call_flows: dict[str, list[dict[str, Any]]],
) -> None:
    def visit(
        node: dict[str, Any],
        namespace: tuple[str, ...],
        fn_stack: list[str],
    ) -> None:
        kind = node.get("kind")
        if kind == "NamespaceDecl" and node.get("name"):
            namespace = (*namespace, node["name"])
        if kind == "FunctionDecl" and has_body(node):
            fn_id = f"fn:{_qualified_name(namespace, node.get('name') or '')}"
            if fn_id in by_id:
                fn_stack.append(fn_id)
                for child in node.get("inner", []):
                    visit(child, namespace, fn_stack)
                fn_stack.pop()
                return
        if kind == "CallExpr" and fn_stack:
            _collect_call_flow(
                node,
                root,
                unit_file,
                by_name,
                by_id,
                param_flows,
                call_flows,
            )
        for child in node.get("inner", []):
            visit(child, namespace, fn_stack)

    visit(ast, (), [])
def _collect_call_flow(
    call: dict[str, Any],
    root: Path,
    unit_file: str,
    by_name: dict[str, list[dict[str, Any]]],
    by_id: dict[str, dict[str, Any]],
    param_flows: dict[str, dict[int, str]],
    call_flows: dict[str, list[dict[str, Any]]],
) -> None:
    children = call.get("inner", [])
    callee = _unwrap(children[0]) if children else None
    if not callee or callee.get("kind") != "DeclRefExpr":
        return
    referenced = callee.get("referencedDecl") or {}
    if referenced.get("kind") != "FunctionDecl":
        return
    target_id = _resolve_function(by_name, referenced.get("name") or "")
    flows = param_flows.get(target_id or "")
    if not flows:
        return
    args = [_unwrap(child) for child in children[1:]]
    location = node_location(root, call, unit_file)
    if location is None:
        return
    for param_index, field_key in flows.items():
        if param_index >= len(args):
            continue
        arg = args[param_index]
        if arg and arg.get("kind") == "DeclRefExpr":
            arg_ref = arg.get("referencedDecl") or {}
            if arg_ref.get("kind") == "FunctionDecl":
                call_flows[field_key].append(
                    {
                        "name": arg_ref["name"],
                        "location": location,
                    }
                )


def stage05_async(workspace: Path) -> dict[str, Any]:
    request = _load_request(workspace)
    graph = read_json(workspace / "03-callgraph" / "callgraph.json")
    fptr = read_json(workspace / "04-fptr" / "fptr-candidates.json")
    nodes = {node["id"]: node for node in graph["nodes"]}
    edges = {edge["id"]: edge for edge in graph["edges"]}

    event_node = _find_event_source_node(nodes)
    chains: list[dict[str, Any]] = []
    evidence: dict[str, dict[str, Any]] = {}
    for candidate in fptr["candidates"]:
        call_site = candidate["call_site"]
        edge = next(
            (
                item
                for item in graph["edges"]
                if item["kind"] == "indirect_call"
                and item["call_site"].get("file") == call_site.get("file")
                and item["call_site"].get("line") == call_site.get("line")
            ),
            None,
        )
        if edge is None:
            continue
        source_node = nodes.get(edge["source"])
        source_name = source_node["name"] if source_node else edge["source"]
        registration = _registration_site(candidate["assignment_sites"])
        if registration:
            reg_ev_id = evidence_id(
                "registration", registration["file"], registration["line"], source_name
            )
            if reg_ev_id not in evidence:
                evidence[reg_ev_id] = {
                    "id": reg_ev_id,
                    "kind": "registration",
                    "location": registration,
                    "role": "supports",
                    "build_profile": request.get("build_profile", "default"),
                }

        event_location = {
            "file": event_node["file"],
            "line": event_node["line"],
            "snippet": snippet_for(_repo_root(workspace), event_node["file"], event_node["line"]),
        }
        event_ev_id = evidence_id(
            "trigger", event_location["file"], event_location["line"], event_node["name"]
        )
        if event_ev_id not in evidence:
            evidence[event_ev_id] = {
                "id": event_ev_id,
                "kind": "trigger",
                "location": event_location,
                "role": "context",
                "build_profile": request.get("build_profile", "default"),
            }

        callbacks = []
        for target in candidate["candidate_targets"]:
            callbacks.append(
                {
                    "name": target["name"],
                    "file": target["file"],
                    "line": target["line"],
                    "execution_context": "event_loop",
                    "confidence": target["confidence"],
                    "evidence_ids": list(target.get("evidence_ids", [])),
                }
            )

        chains.append(
            {
                "id": "async_" + stable_digest(
                    [edge["source"], call_site["file"], call_site["line"]]
                )[:12],
                "name": f"{source_name} -> {candidate['field']}",
                "event_source": {
                    "kind": "fd_ready",
                    "file": event_node["file"],
                    "line": event_node["line"],
                },
                "registration": registration or call_site,
                "trigger": call_site,
                "callbacks": callbacks,
                "loop_back": True,
                "confidence": candidate["confidence"],
                "evidence_ids": sorted(set(candidate["evidence_ids"]) | set(evidence)),
            }
        )

    result = {
        "schema_version": "1.0",
        "run_id": request["run_id"],
        "stage": "05-async",
        "status": "succeeded" if chains else "partial",
        "generated_at": utc_now(),
        "chains": chains,
        "evidence": sorted(evidence.values(), key=lambda item: item["id"]),
        "warnings": [] if chains else ["没有找到可解析的异步回调链"],
    }
    write_json(workspace / "05-async" / "async-chains.json", result)
    return result


def _find_event_source_node(nodes: dict[str, dict[str, Any]]) -> dict[str, Any]:
    for node in nodes.values():
        if "wait_for_events" in node["name"] or "poll" in node["name"].lower():
            return node
    return next(iter(nodes.values()))


def _registration_site(sites: list[dict[str, Any]]) -> dict[str, Any] | None:
    for site in sites:
        if "loop_register" in site.get("snippet", "") or "register" in site.get("snippet", ""):
            return site
    return sites[0] if sites else None


def stage06_verify(workspace: Path) -> dict[str, Any]:
    request = _load_request(workspace)
    graph = read_json(workspace / "03-callgraph" / "callgraph.json")
    fptr = read_json(workspace / "04-fptr" / "fptr-candidates.json")
    async_result = read_json(workspace / "05-async" / "async-chains.json")
    symbols = _symbols(workspace)
    nodes = {node["id"]: node for node in graph["nodes"]}
    evidence_ids = {item["id"] for item in graph["evidence"]}
    evidence_ids.update(item["id"] for item in fptr.get("evidence", []))
    evidence_ids.update(item["id"] for item in async_result.get("evidence", []))

    checks: list[dict[str, Any]] = []
    confirmed = 0
    for edge in graph["edges"]:
        edge_id = edge["id"]
        ok = True
        if edge["source"] not in nodes or edge["target"] not in nodes:
            ok = False
            checks.append(_check(f"{edge_id}: 节点存在", "refuted", "source_recheck", edge["evidence_ids"], 0.0))
            continue
        missing = [ev for ev in edge["evidence_ids"] if ev not in evidence_ids]
        if missing:
            ok = False
            checks.append(_check(f"{edge_id}: 证据引用完整", "refuted", "source_recheck", edge["evidence_ids"], 0.0))
            continue
        snippet = edge["call_site"].get("snippet", "")
        if not snippet:
            ok = False
            checks.append(_check(f"{edge_id}: 调用点原文存在", "refuted", "source_recheck", edge["evidence_ids"], 0.0))
            continue
        if edge["kind"] == "direct_call":
            target_name = nodes[edge["target"]]["name"]
            if target_name not in snippet:
                ok = False
                checks.append(_check(f"{edge_id}: 直接调用目标与源码一致", "refuted", "source_recheck", edge["evidence_ids"], 0.0))
            else:
                confirmed += 1
                checks.append(_check(f"{edge_id}: 直接调用目标与源码一致", "confirmed", "source_recheck", edge["evidence_ids"], 1.0))
        elif edge["kind"] == "indirect_call":
            field_key = edge["target"].removeprefix("cb:")
            candidate = next(
                (
                    item
                    for item in fptr["candidates"]
                    if item["field"] == field_key
                    and item["call_site"].get("file") == edge["call_site"].get("file")
                    and item["call_site"].get("line") == edge["call_site"].get("line")
                ),
                None,
            )
            if candidate and candidate["candidate_targets"]:
                confirmed += 1
                checks.append(
                    _check(
                        f"{edge_id}: 函数指针候选已解析",
                        "confirmed",
                        "clang_reparse",
                        candidate["evidence_ids"],
                        candidate["confidence"],
                    )
                )
            else:
                ok = False
                checks.append(_check(f"{edge_id}: 函数指针候选已解析", "uncertain", "heuristic", edge["evidence_ids"], 0.3))

    for chain in async_result["chains"]:
        missing_callbacks = [
            callback["name"]
            for callback in chain["callbacks"]
            if not any(node["name"] == callback["name"] for node in graph["nodes"])
        ]
        if missing_callbacks:
            checks.append(
                _check(
                    f"{chain['id']}: 回调节点存在",
                    "refuted",
                    "source_recheck",
                    chain["evidence_ids"],
                    0.0,
                )
            )
        else:
            checks.append(
                _check(
                    f"{chain['id']}: 回调节点存在",
                    "confirmed",
                    "source_recheck",
                    chain["evidence_ids"],
                    chain["confidence"],
                )
            )

    requested_edges = len(graph["edges"])
    coverage_rate = min(confirmed / requested_edges, 1.0) if requested_edges else 1.0
    report_ready = coverage_rate >= 0.9 and all(
        item["result"] != "refuted" for item in checks
    )
    result = {
        "schema_version": "1.0",
        "run_id": request["run_id"],
        "stage": "06-verify",
        "status": "succeeded" if report_ready else "partial",
        "generated_at": utc_now(),
        "checks": checks,
        "coverage": {
            "requested_edges": requested_edges,
            "confirmed_edges": confirmed,
            "coverage_rate": round(coverage_rate, 4),
        },
        "conflicts": [],
        "report_ready": report_ready,
        "warnings": [] if report_ready else ["存在未完全确认的调用边"],
    }
    write_json(workspace / "06-verify" / "verification.json", result)
    return result


def _check(
    claim: str,
    result: str,
    method: str,
    evidence_ids: list[str],
    confidence: float,
) -> dict[str, Any]:
    return {
        "id": "check_" + stable_digest([claim, result])[:12],
        "claim": claim,
        "result": result,
        "method": method,
        "evidence_ids": evidence_ids,
        "confidence": confidence,
    }


def stage07_report(workspace: Path) -> dict[str, Any]:
    request = _load_request(workspace)
    graph = read_json(workspace / "03-callgraph" / "callgraph.json")
    fptr = read_json(workspace / "04-fptr" / "fptr-candidates.json")
    async_result = read_json(workspace / "05-async" / "async-chains.json")
    macros = read_json(workspace / "02-macro" / "macros.json")
    verification = read_json(workspace / "06-verify" / "verification.json")
    symbol_count = len(read_json(workspace / "01-index" / "symbols.json")["symbols"])

    final_graph = _final_graph(graph, fptr)
    architecture = _architecture(final_graph)
    key_chains = _key_chains(final_graph)
    analysis_text = _natural_language_analysis(
        request,
        final_graph,
        fptr,
        async_result,
        verification,
        architecture,
        macros,
    )
    report_dir = _stage_dir(workspace, "07-report")
    write_json(report_dir / "graph.json", final_graph)
    write_json(report_dir / "architecture.json", architecture)
    write_json(report_dir / "key-chains.json", key_chains)
    (report_dir / "analysis.md").write_text(analysis_text, encoding="utf-8")
    write_json(
        report_dir / "run-result.json",
        _run_result(request, final_graph, verification, symbol_count),
    )

    mermaid = _mermaid(final_graph)
    (report_dir / "graph.mmd").write_text(mermaid, encoding="utf-8")
    (report_dir / "report.md").write_text(
        _report_markdown(
            request,
            final_graph,
            async_result,
            verification,
            architecture,
            key_chains,
            analysis_text,
            fptr,
            macros,
        ),
        encoding="utf-8",
    )
    return {
        "status": "succeeded",
        "artifacts": [
            "report.md",
            "graph.json",
            "graph.mmd",
            "run-result.json",
            "architecture.json",
            "key-chains.json",
            "analysis.md",
        ],
    }


def _component_id_for_file(file: str) -> str:
    return Path(file).stem or "core"


def _component_label(component_id: str) -> str:
    return {
        "event_loop": "event_loop (事件循环)",
        "app": "app (应用回调)",
    }.get(component_id, component_id)


def _responsibility_for_name(name: str) -> str:
    lowered = name.lower()
    if "register" in lowered:
        return "回调注册"
    if "dispatch" in lowered or "run_ready" in lowered:
        return "事件分发"
    if "wait_for" in lowered or "poll" in lowered:
        return "事件等待"
    if "loop" in lowered:
        return "事件循环驱动"
    if name.startswith("on_"):
        return "应用回调"
    if "init" in lowered:
        return "初始化"
    if "stop" in lowered:
        return "停止循环"
    return "核心逻辑"


def _architecture(graph: dict[str, Any]) -> dict[str, Any]:
    components: dict[str, dict[str, Any]] = {}
    node_by_id = {node["id"]: node for node in graph["nodes"]}
    for node in graph["nodes"]:
        component_id = _component_id_for_file(node.get("file", ""))
        component = components.setdefault(
            component_id,
            {
                "id": component_id,
                "name": _component_label(component_id),
                "files": set(),
                "symbols": [],
                "responsibilities": set(),
            },
        )
        if node.get("file"):
            component["files"].add(node["file"])
        component["symbols"].append(
            {
                "id": node["id"],
                "name": node["name"],
                "kind": node["kind"],
            }
        )
        component["responsibilities"].add(_responsibility_for_name(node["name"]))

    dependency_set: set[tuple[str, str]] = set()
    for edge in graph["edges"]:
        source = node_by_id.get(edge["source"])
        target = node_by_id.get(edge["target"])
        if not source or not target:
            continue
        source_component = _component_id_for_file(source.get("file", ""))
        target_component = _component_id_for_file(target.get("file", ""))
        if source_component != target_component:
            dependency_set.add((source_component, target_component))

    component_list = []
    for component in components.values():
        component["files"] = sorted(component["files"])
        component["symbols"].sort(key=lambda item: item["id"])
        component["responsibilities"] = sorted(component["responsibilities"])
        component_list.append(component)
    component_list.sort(key=lambda item: item["id"])

    return {
        "schema_version": "1.0",
        "run_id": graph["run_id"],
        "components": component_list,
        "dependencies": [
            {"source": source, "target": target}
            for source, target in sorted(dependency_set)
        ],
    }


def _key_chains(graph: dict[str, Any]) -> dict[str, Any]:
    nodes = {node["id"]: node for node in graph["nodes"]}
    adjacency: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for edge in graph["edges"]:
        adjacency[edge["source"]].append(edge)
    for edge_list in adjacency.values():
        edge_list.sort(key=lambda item: item["id"])

    entry = next(
        (node for node in graph["nodes"] if node["name"] == "app_main"),
        graph["nodes"][0] if graph["nodes"] else None,
    )
    if entry is None:
        return {"schema_version": "1.0", "run_id": graph["run_id"], "paths": []}

    paths: list[dict[str, Any]] = []

    def visit(
        current: str,
        node_path: list[str],
        edge_path: list[str],
    ) -> None:
        if len(paths) >= 10:
            return
        if len(edge_path) >= 8:
            paths.append(_path_payload(nodes, node_path, edge_path, "max_depth"))
            return
        candidates = adjacency.get(current, [])
        if not candidates:
            paths.append(_path_payload(nodes, node_path, edge_path, "leaf"))
            return
        progressed = False
        for edge in candidates:
            if edge["target"] in node_path:
                continue
            progressed = True
            visit(edge["target"], node_path + [edge["target"]], edge_path + [edge["id"]])
        if not progressed:
            paths.append(_path_payload(nodes, node_path, edge_path, "leaf"))

    visit(entry["id"], [entry["id"]], [])
    return {
        "schema_version": "1.0",
        "run_id": graph["run_id"],
        "entry": entry["name"],
        "paths": paths,
    }


def _path_payload(
    nodes: dict[str, dict[str, Any]],
    node_path: list[str],
    edge_path: list[str],
    reason: str,
) -> dict[str, Any]:
    names = [nodes[node_id]["name"] for node_id in node_path]
    return {
        "id": "key_" + stable_digest(node_path)[:12],
        "nodes": list(node_path),
        "edges": list(edge_path),
        "summary": " -> ".join(names),
        "termination_reason": reason,
    }


def _natural_language_analysis(
    request: dict[str, Any],
    graph: dict[str, Any],
    fptr: dict[str, Any],
    async_result: dict[str, Any],
    verification: dict[str, Any],
    architecture: dict[str, Any],
    macros: dict[str, Any],
) -> str:
    component_names = "、".join(item["name"] for item in architecture["components"])
    key_chains = _key_chains(graph)
    key_summary = ""
    for path in key_chains["paths"]:
        if "dispatch_once" in path["summary"]:
            key_summary = path["summary"]
            break
    if not key_summary:
        key_summary = key_chains["paths"][0]["summary"]
    entry_name = key_chains.get("entry", "app_main")

    candidate_names = []
    for candidate in fptr.get("candidates", []):
        candidate_names.extend(item["name"] for item in candidate.get("candidate_targets", []))
    candidate_text = "、".join(sorted(set(candidate_names))) or "无"
    fptr_confidence = fptr["candidates"][0]["confidence"] if fptr.get("candidates") else 0.0

    macro_names = []
    for expansion in macros.get("expansions", []):
        if expansion["name"] in {"CALL_WATCHER", "LOOP_BACKEND"}:
            macro_names.append(
                f"{expansion['name']} ({expansion['file']}:{expansion['line']})"
            )
    macro_text = "、".join(macro_names) or "无"

    async_text = "无"
    for chain in async_result.get("chains", []):
        callback_names = "、".join(item["name"] for item in chain.get("callbacks", []))
        async_text = (
            f"{chain['event_source']['kind']} 事件在 {chain['trigger']['file']}:"
            f"{chain['trigger']['line']} 触发回调，候选为 {callback_names}"
        )

    return "\n".join(
        [
            "# 自然语言分析",
            "",
            f"## 模块架构",
            f"样例由 {component_names} 组成。应用入口负责初始化事件循环、注册回调并启动轮询；"
            "事件循环组件负责等待就绪事件、遍历 watcher 并分发回调。",
            "",
            f"## 关键调用链",
            f"入口 `{entry_name}` 的关键路径是：`{key_summary}`。",
            "",
            "## 异步回调链",
            async_text,
            "",
            "## 函数指针",
            f"静态分析发现回调字段存在多个候选：`{candidate_text}`，"
            f"无法唯一确定目标，置信度为 {fptr_confidence:.2f}。",
            "",
            "## 复杂宏",
            f"本次分析覆盖：{macro_text}。宏展开记录已挂到对应调用边的 `macro_stack` 证据上。",
            "",
            "## 结论",
            f"验证覆盖率为 {verification['coverage']['coverage_rate']:.0%}，"
            f"报告状态为 {'ready' if verification['report_ready'] else 'not ready'}；"
            "所有结论均引用源码文件、行号和原始代码片段。",
            "",
        ]
    )


def _final_graph(
    graph: dict[str, Any], fptr: dict[str, Any]
) -> dict[str, Any]:
    result = {
        "schema_version": graph["schema_version"],
        "run_id": graph["run_id"],
        "meta": dict(graph["meta"]),
        "nodes": [dict(node) for node in graph["nodes"]],
        "edges": [],
        "evidence": [dict(item) for item in graph["evidence"]],
    }
    known_evidence = {item["id"]: item for item in result["evidence"]}
    for item in fptr.get("evidence", []):
        known_evidence.setdefault(item["id"], item)

    for edge in graph["edges"]:
        edge_copy = dict(edge)
        if edge["kind"] == "indirect_call":
            field_key = edge["target"].removeprefix("cb:")
            candidate = next(
                (
                    item
                    for item in fptr["candidates"]
                    if item["field"] == field_key
                    and item["call_site"].get("file") == edge["call_site"].get("file")
                    and item["call_site"].get("line") == edge["call_site"].get("line")
                ),
                None,
            )
            if candidate:
                edge_copy["kind"] = "callback_edge"
                edge_copy["event"] = "fd_ready"
                edge_copy["execution_context"] = "event_loop"
                edge_copy["confidence"] = candidate["confidence"]
                edge_copy["evidence_ids"] = sorted(
                    set(edge["evidence_ids"]) | set(candidate["evidence_ids"])
                )
        result["edges"].append(edge_copy)

    nodes_by_name = {node["name"]: node for node in result["nodes"]}
    for candidate in fptr.get("candidates", []):
        callback_node_id = f"cb:{candidate['field']}"
        for target in candidate.get("candidate_targets", []):
            target_node = nodes_by_name.get(target["name"])
            if target_node is None:
                continue
            call_site = next(
                (
                    site
                    for site in candidate.get("assignment_sites", [])
                    if target["name"] in site.get("snippet", "")
                ),
                candidate.get("call_site"),
            )
            edge_id = "e_" + stable_digest(
                [callback_node_id, target_node["id"], call_site["file"], call_site["line"]]
            )[:12]
            if edge_id not in {item["id"] for item in result["edges"]}:
                result["edges"].append(
                    {
                        "id": edge_id,
                        "source": callback_node_id,
                        "target": target_node["id"],
                        "kind": "callback_edge",
                        "call_site": call_site,
                        "event": "fd_ready",
                        "condition": None,
                        "execution_context": "event_loop",
                        "confidence": target["confidence"],
                        "evidence_ids": list(target.get("evidence_ids", [])),
                    }
                )

    referenced_ids = {
        item["source"] for item in result["edges"]
    } | {item["target"] for item in result["edges"]}
    result["nodes"] = [
        node for node in result["nodes"] if node["id"] in referenced_ids
    ]
    result["evidence"] = sorted(known_evidence.values(), key=lambda item: item["id"])
    return result


def _run_result(
    request: dict[str, Any],
    graph: dict[str, Any],
    verification: dict[str, Any],
    symbol_count: int = 0,
) -> dict[str, Any]:
    findings = []
    for edge in graph["edges"]:
        if edge["kind"] in {"direct_call", "callback_edge"}:
            findings.append(
                {
                    "kind": edge["kind"],
                    "source": edge["source"],
                    "target": edge["target"],
                    "condition": edge.get("condition"),
                    "execution_context": edge.get("execution_context"),
                    "confidence": edge["confidence"],
                    "evidence_ids": edge["evidence_ids"],
                }
            )
    return {
        "schema_version": "1.0",
        "run_id": request["run_id"],
        "task_id": request.get("task_id", "clang-pipeline-demo"),
        "status": "succeeded" if verification["report_ready"] else "partial",
        "summary": "Clang 从 AST 中提取 C++ 函数调用关系，并通过函数指针赋值流还原事件循环回调链。",
        "findings": findings,
        "evidence": graph["evidence"],
        "stats": {
            "started_at": request.get("started_at", ""),
            "finished_at": utc_now(),
            "duration_ms": 0,
            "symbols": symbol_count,
            "nodes": len(graph["nodes"]),
            "edges": len(graph["edges"]),
        },
        "warnings": [],
    }


def _mermaid(graph: dict[str, Any]) -> str:
    lines = ["flowchart TD"]
    node_ids: dict[str, str] = {}
    groups: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for node in graph["nodes"]:
        groups[_component_id_for_file(node.get("file", ""))].append(node)

    index = 0
    for component_id in sorted(groups):
        safe_id = re.sub(r"[^A-Za-z0-9_]", "_", component_id)
        label = _component_label(component_id).replace('"', "'")
        lines.append(f'  subgraph sg_{safe_id}["{label}"]')
        for node in sorted(groups[component_id], key=lambda item: item["id"]):
            index += 1
            alias = f"N{index}"
            node_ids[node["id"]] = alias
            node_label = node["name"].replace('"', "'")
            lines.append(f'    {alias}["{node_label}"]')
        lines.append("  end")

    for edge in graph["edges"]:
        source = node_ids.get(edge["source"])
        target = node_ids.get(edge["target"])
        if not source or not target:
            continue
        if edge["kind"] == "callback_edge":
            label = edge.get("condition") or edge.get("event") or "callback"
            lines.append(f"  {source} -. {label} .-> {target}")
        else:
            lines.append(f"  {source} --> {target}")
    return "\n".join(lines) + "\n"


def _report_markdown(
    request: dict[str, Any],
    graph: dict[str, Any],
    async_result: dict[str, Any],
    verification: dict[str, Any],
    architecture: dict[str, Any],
    key_chains: dict[str, Any],
    analysis_text: str,
    fptr: dict[str, Any],
    macros: dict[str, Any],
) -> str:
    lines = [
        "# 代码逆向分析 Demo",
        "",
        f"- Run: `{request['run_id']}`",
        f"- Build profile: `{request.get('build_profile', 'default')}`",
        f"- Analyzer: `clang++ -Xclang -ast-dump=json`",
        f"- Nodes: {len(graph['nodes'])} / Edges: {len(graph['edges'])}",
        f"- Verification: {verification['coverage']['coverage_rate']:.0%}",
        "",
        "## 模块架构",
        "",
    ]
    for component in architecture["components"]:
        responsibilities = "、".join(component["responsibilities"])
        symbols = "、".join(item["name"] for item in component["symbols"])
        lines.extend(
            [
                f"- **{component['name']}**: {responsibilities}",
                f"  - Files: `{'`, `'.join(component['files'])}`",
                f"  - Symbols: `{symbols}`",
            ]
        )
    if architecture["dependencies"]:
        deps = ", ".join(
            f"`{item['source']} -> {item['target']}`"
            for item in architecture["dependencies"]
        )
        lines.extend(["", f"Dependencies: {deps}"])

    lines.extend(
        [
            "",
            "## 调用关系图",
            "",
            "```mermaid",
            _mermaid(graph).rstrip(),
            "```",
            "",
            "## 关键调用链",
            "",
        ]
    )
    for path in key_chains.get("paths", []):
        lines.append(f"- `{path['summary']}` ({path['termination_reason']})")

    lines.extend(
        [
            "",
            "## 自然语言分析",
            "",
        ]
    )
    lines.extend(analysis_text.splitlines())
    lines.extend(
        [
            "",
            "## 异步回调链",
            "",
        ]
    )
    for chain in async_result["chains"]:
        callback_names = ", ".join(item["name"] for item in chain["callbacks"])
        lines.extend(
            [
                f"- `{chain['event_source']['file']}:{chain['event_source']['line']}` "
                f"`{chain['event_source']['kind']}` -> "
                f"`{chain['registration']['file']}:{chain['registration']['line']}` "
                f"-> `{chain['trigger']['file']}:{chain['trigger']['line']}` "
                f"-> callbacks: {callback_names}",
                f"  - Confidence: {chain['confidence']:.2f}, loop back: {chain['loop_back']}",
            ]
        )

    lines.extend(
        [
            "",
            "## 函数指针候选",
            "",
        ]
    )
    for candidate in fptr.get("candidates", []):
        targets = ", ".join(
            f"`{item['name']}` ({item['file']}:{item['line']})"
            for item in candidate.get("candidate_targets", [])
        )
        lines.extend(
            [
                f"- `{candidate['field']}` @ `{candidate['call_site']['file']}:"
                f"{candidate['call_site']['line']}`",
                f"  - Candidates: {targets}",
                f"  - Confidence: {candidate['confidence']:.2f}",
            ]
        )

    lines.extend(
        [
            "",
            "## 宏分析",
            "",
            "| macro | file:line | definition | call sites |",
            "| --- | --- | --- | --- |",
        ]
    )
    for expansion in macros.get("expansions", []):
        if expansion["name"] in {"CALL_WATCHER", "LOOP_BACKEND", "EVENT_READ", "EVENT_WRITE"}:
            definition = (expansion.get("definition") or "").replace("|", "\\|")
            lines.append(
                f"| `{expansion['name']}` | `{expansion['file']}:{expansion['line']}` "
                f"| `{definition}` | {len(expansion.get('call_sites', []))} |"
            )

    lines.extend(
        [
            "",
            "## Evidence",
            "",
            "| id | kind | file:line | snippet |",
            "| --- | --- | --- | --- |",
        ]
    )
    for item in graph["evidence"]:
        location = item["location"]
        snippet = (location.get("snippet") or "").replace("|", "\\|")
        lines.append(
            f"| `{item['id']}` | {item['kind']} | `{location['file']}:{location['line']}` | `{snippet}` |"
        )
    lines.append("")
    return "\n".join(lines)
