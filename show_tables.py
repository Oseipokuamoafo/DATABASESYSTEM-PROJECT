"""
show_tables.py — Task 3: Show all tables with inserted contents.

Usage:
    python3 show_tables.py [database_file]

If no database file is given, initialises a fresh in-memory database from
schema.sql + seed.sql and prints every table, so the output is fully
reproducible without an existing .db file.
"""

import sqlite3
import sys
from pathlib import Path

ROOT = Path(__file__).parent
SCHEMA_FILE = ROOT / "schema.sql"
SEED_FILE   = ROOT / "seed.sql"

# ── Helpers ───────────────────────────────────────────────────────────────────

def _connect(db_path: str | None) -> sqlite3.Connection:
    if db_path:
        conn = sqlite3.connect(db_path)
    else:
        conn = sqlite3.connect(":memory:")
        conn.executescript(SCHEMA_FILE.read_text())
        conn.executescript(SEED_FILE.read_text())
    conn.execute("PRAGMA foreign_keys = ON")
    conn.row_factory = sqlite3.Row
    return conn


def _col_widths(headers: list[str], rows: list[sqlite3.Row]) -> list[int]:
    widths = [len(h) for h in headers]
    for row in rows:
        for i, val in enumerate(row):
            widths[i] = max(widths[i], len(str(val) if val is not None else "NULL"))
    return widths


def _print_table(title: str, rows: list[sqlite3.Row]) -> None:
    if not rows:
        print(f"\n  [ {title} — (empty) ]\n")
        return

    headers = list(rows[0].keys())
    widths  = _col_widths(headers, rows)

    sep   = "+-" + "-+-".join("-" * w for w in widths) + "-+"
    hdr   = "| " + " | ".join(h.ljust(w) for h, w in zip(headers, widths)) + " |"
    title_width = len(sep) - 4
    title_line  = f"| {title.center(title_width)} |"
    top_border  = "+" + "=" * (len(sep) - 2) + "+"

    print()
    print(top_border)
    print(title_line)
    print(sep)
    print(hdr)
    print(sep)
    for row in rows:
        cells = [(str(v) if v is not None else "NULL") for v in row]
        print("| " + " | ".join(c.ljust(w) for c, w in zip(cells, widths)) + " |")
    print(sep)
    print(f"  {len(rows)} row{'s' if len(rows) != 1 else ''}")


# ── Tables to display ─────────────────────────────────────────────────────────

TABLES = [
    ("Course",     "SELECT * FROM Course ORDER BY course_id"),
    ("Category",   "SELECT * FROM Category ORDER BY course_id, category_id"),
    ("Student",    "SELECT * FROM Student ORDER BY student_id"),
    ("Enrollment", "SELECT * FROM Enrollment ORDER BY course_id, student_id"),
    ("Assignment", "SELECT * FROM Assignment ORDER BY course_id, assignment_id"),
    ("Score",      "SELECT * FROM Score ORDER BY assignment_id, student_id"),
]

# ── Main ──────────────────────────────────────────────────────────────────────

def show_all(db_path: str | None = None) -> None:
    conn = _connect(db_path)

    print("=" * 60)
    print("  GRADE BOOK DATABASE — TABLE CONTENTS")
    source = db_path if db_path else "in-memory (schema.sql + seed.sql)"
    print(f"  Source: {source}")
    print("=" * 60)

    for title, sql in TABLES:
        rows = conn.execute(sql).fetchall()
        _print_table(title, rows)

    conn.close()
    print()


if __name__ == "__main__":
    db_arg = sys.argv[1] if len(sys.argv) > 1 else None
    show_all(db_arg)
