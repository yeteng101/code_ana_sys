from __future__ import annotations

import ctypes
import shlex
from pathlib import Path
from typing import Any


LIBRARY_PATHS = [
    "/Library/Developer/CommandLineTools/usr/lib/libclang.dylib",
    "/usr/local/opt/llvm/lib/libclang.dylib",
    "/opt/homebrew/opt/llvm/lib/libclang.dylib",
    "libclang.so",
]


class CXString(ctypes.Structure):
    _fields_ = [("data", ctypes.c_char_p), ("private_flags", ctypes.c_uint)]


class CXCursor(ctypes.Structure):
    _fields_ = [
        ("_kind_id", ctypes.c_int),
        ("xdata", ctypes.c_int),
        ("data", ctypes.c_void_p * 3),
    ]


class CXSourceLocation(ctypes.Structure):
    _fields_ = [
        ("ptr_data", ctypes.c_void_p * 2),
        ("int_data", ctypes.c_uint),
    ]


class CXSourceRange(ctypes.Structure):
    _fields_ = [
        ("ptr_data", ctypes.c_void_p * 2),
        ("begin_int_data", ctypes.c_uint),
        ("end_int_data", ctypes.c_uint),
    ]


class CXType(ctypes.Structure):
    _fields_ = [("kind", ctypes.c_int), ("data", ctypes.c_void_p * 2)]


class CXFile(ctypes.c_void_p):
    pass


CXChildVisitResult = ctypes.c_uint
CXCursorVisitor = ctypes.CFUNCTYPE(
    CXChildVisitResult, CXCursor, CXCursor, ctypes.c_void_p
)


def _load_library() -> ctypes.CDLL:
    last_error: Exception | None = None
    for path in LIBRARY_PATHS:
        try:
            return ctypes.CDLL(path)
        except OSError as exc:
            last_error = exc
    raise RuntimeError(f"无法加载 libclang: {last_error}")


lib = _load_library()

lib.clang_createIndex.argtypes = [ctypes.c_int, ctypes.c_int]
lib.clang_createIndex.restype = ctypes.c_void_p
lib.clang_disposeIndex.argtypes = [ctypes.c_void_p]
lib.clang_parseTranslationUnit2.argtypes = [
    ctypes.c_void_p,
    ctypes.c_char_p,
    ctypes.POINTER(ctypes.c_char_p),
    ctypes.c_int,
    ctypes.c_void_p,
    ctypes.c_uint,
    ctypes.c_uint,
    ctypes.POINTER(ctypes.c_void_p),
]
lib.clang_parseTranslationUnit2.restype = ctypes.c_int
lib.clang_disposeTranslationUnit.argtypes = [ctypes.c_void_p]
lib.clang_getTranslationUnitCursor.argtypes = [ctypes.c_void_p]
lib.clang_getTranslationUnitCursor.restype = CXCursor
lib.clang_visitChildren.argtypes = [CXCursor, CXCursorVisitor, ctypes.c_void_p]
lib.clang_visitChildren.restype = ctypes.c_uint
lib.clang_getCursorKind.argtypes = [CXCursor]
lib.clang_getCursorKind.restype = ctypes.c_int
lib.clang_getCursorSpelling.argtypes = [CXCursor]
lib.clang_getCursorSpelling.restype = CXString
lib.clang_getCursorType.argtypes = [CXCursor]
lib.clang_getCursorType.restype = CXType
lib.clang_getTypeSpelling.argtypes = [CXType]
lib.clang_getTypeSpelling.restype = CXString
lib.clang_getCanonicalType.argtypes = [CXType]
lib.clang_getCanonicalType.restype = CXType
lib.clang_getCursorLocation.argtypes = [CXCursor]
lib.clang_getCursorLocation.restype = CXSourceLocation
lib.clang_getFileLocation.argtypes = [
    CXSourceLocation,
    ctypes.POINTER(CXFile),
    ctypes.POINTER(ctypes.c_uint),
    ctypes.POINTER(ctypes.c_uint),
    ctypes.POINTER(ctypes.c_uint),
]
lib.clang_getFileName.argtypes = [CXFile]
lib.clang_getFileName.restype = CXString
lib.clang_getCursorExtent.argtypes = [CXCursor]
lib.clang_getCursorExtent.restype = CXSourceRange
lib.clang_getRangeStart.argtypes = [CXSourceRange]
lib.clang_getRangeStart.restype = CXSourceLocation
lib.clang_getRangeEnd.argtypes = [CXSourceRange]
lib.clang_getRangeEnd.restype = CXSourceLocation
lib.clang_getCursorReferenced.argtypes = [CXCursor]
lib.clang_getCursorReferenced.restype = CXCursor
lib.clang_getCursorDefinition.argtypes = [CXCursor]
lib.clang_getCursorDefinition.restype = CXCursor
lib.clang_isCursorDefinition.argtypes = [CXCursor]
lib.clang_isCursorDefinition.restype = ctypes.c_uint
lib.clang_getCursorUSR.argtypes = [CXCursor]
lib.clang_getCursorUSR.restype = CXString
lib.clang_hashCursor.argtypes = [CXCursor]
lib.clang_hashCursor.restype = ctypes.c_uint
lib.clang_getCursorBinaryOperatorKind.argtypes = [CXCursor]
lib.clang_getCursorBinaryOperatorKind.restype = ctypes.c_int
lib.clang_getBinaryOperatorKindSpelling.argtypes = [ctypes.c_int]
lib.clang_getBinaryOperatorKindSpelling.restype = CXString
lib.clang_getCString.argtypes = [CXString]
lib.clang_getCString.restype = ctypes.c_char_p
lib.clang_disposeString.argtypes = [CXString]


KIND_MAP = {
    2: "RecordDecl",
    3: "RecordDecl",
    4: "CXXRecordDecl",
    5: "EnumDecl",
    6: "FieldDecl",
    7: "EnumConstantDecl",
    8: "FunctionDecl",
    9: "VarDecl",
    10: "ParmVarDecl",
    11: "TypedefDecl",
    12: "CXXMethodDecl",
    13: "NamespaceDecl",
    14: "LinkageSpecDecl",
    15: "CXXConstructorDecl",
    16: "CXXDestructorDecl",
    27: "TypeAliasDecl",
    101: "DeclRefExpr",
    102: "MemberExpr",
    103: "CallExpr",
    106: "IntegerLiteral",
    107: "FloatingLiteral",
    109: "StringLiteral",
    110: "CharacterLiteral",
    111: "ParenExpr",
    112: "UnaryOperator",
    113: "ArraySubscriptExpr",
    114: "BinaryOperator",
    115: "CompoundAssignmentOperator",
    116: "ConditionalOperator",
    117: "CStyleCastExpr",
    118: "CompoundLiteralExpr",
    201: "LabelStmt",
    202: "CompoundStmt",
    203: "CaseStmt",
    204: "DefaultStmt",
    205: "IfStmt",
    206: "SwitchStmt",
    207: "WhileStmt",
    208: "DoStmt",
    209: "ForStmt",
    210: "GotoStmt",
    211: "IndirectGotoStmt",
    212: "ContinueStmt",
    213: "BreakStmt",
    214: "ReturnStmt",
    231: "DeclStmt",
    100: "ImplicitCastExpr",
}


def _string(value: CXString) -> str:
    try:
        raw = lib.clang_getCString(value)
        return raw.decode("utf-8", errors="replace") if raw else ""
    finally:
        lib.clang_disposeString(value)


def _cursor_id(cursor: CXCursor) -> str:
    usr = _string(lib.clang_getCursorUSR(cursor))
    if usr:
        return "cur_" + usr
    return "cur_hash_" + str(lib.clang_hashCursor(cursor))


def _location_dict(location: CXSourceLocation) -> dict[str, Any] | None:
    file = CXFile()
    line = ctypes.c_uint()
    column = ctypes.c_uint()
    offset = ctypes.c_uint()
    lib.clang_getFileLocation(
        location,
        ctypes.byref(file),
        ctypes.byref(line),
        ctypes.byref(column),
        ctypes.byref(offset),
    )
    filename = _string(lib.clang_getFileName(file)) if file else ""
    if not filename:
        return None
    result: dict[str, Any] = {
        "file": filename,
        "line": int(line.value),
        "col": int(column.value),
        "offset": int(offset.value),
    }
    return result


def _type_dict(type_info: CXType) -> dict[str, Any]:
    canonical = lib.clang_getCanonicalType(type_info)
    return {
        "qualType": _string(lib.clang_getTypeSpelling(type_info)),
        "desugaredQualType": _string(lib.clang_getTypeSpelling(canonical)),
    }


def _cursor_type_dict(cursor: CXCursor) -> dict[str, Any]:
    return _type_dict(lib.clang_getCursorType(cursor))


def _referenced_info(cursor: CXCursor) -> dict[str, Any]:
    kind = lib.clang_getCursorKind(cursor)
    return {
        "id": _cursor_id(cursor),
        "kind": KIND_MAP.get(kind, "UnexposedDecl"),
        "name": _string(lib.clang_getCursorSpelling(cursor)),
        "type": _cursor_type_dict(cursor),
    }


def _node_dict(cursor: CXCursor) -> dict[str, Any]:
    kind_number = lib.clang_getCursorKind(cursor)
    kind = KIND_MAP.get(kind_number, "UnexposedDecl")
    node: dict[str, Any] = {"id": _cursor_id(cursor), "kind": kind}
    spelling = _string(lib.clang_getCursorSpelling(cursor))
    if spelling:
        node["name"] = spelling
    location = _location_dict(lib.clang_getCursorLocation(cursor))
    if location:
        node["loc"] = location
    type_info = _cursor_type_dict(cursor)
    if type_info.get("qualType"):
        node["type"] = type_info

    if kind == "BinaryOperator":
        op_kind = lib.clang_getCursorBinaryOperatorKind(cursor)
        node["opcode"] = _string(lib.clang_getBinaryOperatorKindSpelling(op_kind))
    elif kind == "DeclRefExpr":
        referenced = lib.clang_getCursorReferenced(cursor)
        if referenced.data[0]:
            node["referencedDecl"] = _referenced_info(referenced)
    elif kind == "MemberExpr":
        referenced = lib.clang_getCursorReferenced(cursor)
        if referenced.data[0]:
            node["referencedMemberDecl"] = _cursor_id(referenced)
    elif kind in {"FunctionDecl", "CXXMethodDecl"}:
        if lib.clang_isCursorDefinition(cursor):
            node["_definition"] = True
    elif kind in {"RecordDecl", "CXXRecordDecl"} and lib.clang_isCursorDefinition(cursor):
        node["completeDefinition"] = True
    return node


def _should_include(cursor: CXCursor, source_root: Path) -> bool:
    location = _location_dict(lib.clang_getCursorLocation(cursor))
    if not location:
        return True
    try:
        path = Path(location["file"]).resolve()
        return path.is_relative_to(source_root.resolve())
    except ValueError:
        return False


def _build_subtree(cursor: CXCursor, source_root: Path) -> dict[str, Any]:
    node = _node_dict(cursor)
    children: list[dict[str, Any]] = []

    def visitor(
        child: CXCursor,
        parent: CXCursor,
        client_data: ctypes.c_void_p,
    ) -> int:
        if _should_include(child, source_root):
            children.append(_build_subtree(child, source_root))
        return 1

    lib.clang_visitChildren(cursor, CXCursorVisitor(visitor), None)
    if children:
        node["inner"] = children
    return node


def _parse_args(unit: dict[str, Any]) -> list[str]:
    arguments = unit.get("arguments")
    if not arguments:
        arguments = shlex.split(unit.get("command", ""))
    arguments = [str(item) for item in arguments]
    if arguments and Path(arguments[0]).name in {"clang", "clang++", "cc", "gcc"}:
        arguments = arguments[1:]
    result: list[str] = []
    index = 0
    while index < len(arguments):
        value = arguments[index]
        if value in {"-c", "-MD", "-MMD", "-MQ"}:
            index += 1
            continue
        if value in {"-o", "-MF", "-MT"}:
            index += 2
            continue
        if value.startswith("-o") and len(value) > 2:
            index += 1
            continue
        result.append(value)
        index += 1
    return result


def extract_compact_ast(unit: dict[str, Any], source_root: Path) -> dict[str, Any]:
    index = lib.clang_createIndex(1, 1)
    translation_unit = ctypes.c_void_p()
    args = _parse_args(unit)
    argv = (ctypes.c_char_p * len(args))(
        *(item.encode("utf-8") for item in args)
    )
    error = lib.clang_parseTranslationUnit2(
        index,
        None,
        argv,
        len(args),
        None,
        0,
        0,
        ctypes.byref(translation_unit),
    )
    if error != 0 or not translation_unit:
        lib.clang_disposeIndex(index)
        raise RuntimeError(f"libclang 解析失败: {unit.get('file')} (error={error})")
    try:
        root_cursor = lib.clang_getTranslationUnitCursor(translation_unit)
        return _build_subtree(root_cursor, source_root)
    finally:
        lib.clang_disposeTranslationUnit(translation_unit)
        lib.clang_disposeIndex(index)
