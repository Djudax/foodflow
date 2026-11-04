#!/usr/bin/env python3
"""Локальний аналог `radon cc -s -j`: цикломатична складність за Мак-Кейбом.

Вихід має ту саму структуру JSON, що й у radon:
{ "<файл>": [ {"type", "rank", "name", "classname"?, "lineno", "endline", "complexity"} ] }

Лише стандартна бібліотека (ast). Потрібен для офлайн-запуску; у CI замість нього
працює справжній radon (див. .github/workflows/quality.yml).

Використання:  python tools/cc_local.py src > reports/complexity.json
"""
import ast
import json
import sys
from pathlib import Path


def rank(cc: int) -> str:
    for limit, letter in ((5, "A"), (10, "B"), (20, "C"), (30, "D"), (40, "E")):
        if cc <= limit:
            return letter
    return "F"


def complexity(node: ast.AST) -> int:
    """1 + кількість точок прийняття рішень (правила radon)."""
    total = 1
    for n in ast.walk(node):
        if isinstance(n, (ast.If, ast.IfExp, ast.Assert, ast.ExceptHandler)):
            total += 1
        elif isinstance(n, (ast.For, ast.AsyncFor, ast.While)):
            total += 1 + (1 if n.orelse else 0)
        elif isinstance(n, ast.BoolOp):
            total += len(n.values) - 1
        elif isinstance(n, ast.comprehension):
            total += 1 + len(n.ifs)
    return total


def block(fn, classname=None) -> dict:
    cc = complexity(fn)
    data = {
        "type": "method" if classname else "function",
        "rank": rank(cc),
        "name": fn.name,
        "lineno": fn.lineno,
        "endline": fn.end_lineno,
        "complexity": cc,
    }
    if classname:
        data["classname"] = classname
    return data


def analyze_source(source: str) -> list:
    tree = ast.parse(source)
    blocks = []
    for node in tree.body:
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            blocks.append(block(node))
        elif isinstance(node, ast.ClassDef):
            for item in node.body:
                if isinstance(item, (ast.FunctionDef, ast.AsyncFunctionDef)):
                    blocks.append(block(item, node.name))
    return blocks


def main(argv) -> None:
    roots = [Path(a) for a in argv] or [Path("src")]
    report = {}
    for root in roots:
        files = [root] if root.is_file() else sorted(root.rglob("*.py"))
        for f in files:
            report[f.as_posix()] = analyze_source(f.read_text(encoding="utf-8"))
    json.dump(report, sys.stdout, ensure_ascii=False, indent=2)
    sys.stdout.write("\n")


if __name__ == "__main__":
    main(sys.argv[1:])
