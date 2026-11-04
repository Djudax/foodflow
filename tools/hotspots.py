#!/usr/bin/env python3
"""Синергетична матриця Hotspots: складність (JSON radon) x Churn Rate (git log).

Приймає звіт у форматі `radon cc -s -j` (або tools/cc_local.py), рахує кількість
комітів на файл за період і розкладає файли на 4 категорії ризику.

Використання:
  python tools/hotspots.py --complexity reports/complexity.json --out-dir reports
"""
import argparse
import csv
import json
import subprocess
from collections import Counter
from pathlib import Path

ORDER = {"Hotspot": 0, "Sleeping": 1, "Active": 2, "Stable": 3}


def load_max_complexity(path: str) -> dict:
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    result = {}
    for filename, blocks in data.items():
        if not isinstance(blocks, list):  # radon повертає dict з помилкою
            continue
        flat = []
        for b in blocks:
            if b.get("type") == "class":
                flat.extend(b.get("methods", []))
            else:
                flat.append(b)
        if flat:
            result[filename.replace("\\", "/")] = max(b["complexity"] for b in flat)
    return result


def churn(since: str, path: str) -> Counter:
    out = subprocess.run(
        ["git", "log", f"--since={since}", "--format=format:", "--name-only", "--", path],
        capture_output=True, text=True, check=True,
    ).stdout
    return Counter(line for line in out.splitlines() if line.strip())


def classify(cc: int, commits: int, cc_limit: int, churn_limit: int) -> str:
    if cc > cc_limit:
        return "Hotspot" if commits >= churn_limit else "Sleeping"
    return "Active" if commits >= churn_limit else "Stable"


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--complexity", required=True)
    ap.add_argument("--since", default="90 days ago")
    ap.add_argument("--path", default="src")
    ap.add_argument("--cc-limit", type=int, default=10)
    ap.add_argument("--churn-limit", type=int, default=6)
    ap.add_argument("--out-dir", default="reports")
    args = ap.parse_args()

    cc_map = load_max_complexity(args.complexity)
    commits = churn(args.since, args.path)
    rows = []
    for filename, cc in cc_map.items():
        n = commits.get(filename, 0)
        rows.append((filename, cc, n, classify(cc, n, args.cc_limit, args.churn_limit)))
    rows.sort(key=lambda r: (ORDER[r[3]], -r[2], -r[1]))

    out = Path(args.out_dir)
    out.mkdir(parents=True, exist_ok=True)
    with (out / "hotspots.csv").open("w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(["file", "max_cc", "commits", "category"])
        w.writerows(rows)

    lines = ["| File | Max CC | Commits | Category |", "|---|---:|---:|---|"]
    lines += [f"| {f} | {cc} | {n} | {cat} |" for f, cc, n, cat in rows]
    (out / "hotspots.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("\n".join(lines))


if __name__ == "__main__":
    main()
