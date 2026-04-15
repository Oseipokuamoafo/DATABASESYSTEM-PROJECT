import os
import sqlite3
import tempfile
import pytest
from pathlib import Path
from gradebook import init_db, seed_db, connect, compute_student_grade, compute_student_grade_drop_lowest, list_students, get_assignment_stats

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DB_NAME = 'test_gradebook.db'


def create_test_db(tmp_path):
    db_path = tmp_path / DB_NAME
    init_db(str(db_path))
    seed_db(str(db_path))
    return db_path


def test_list_students_returns_five_students(tmp_path):
    db_path = create_test_db(tmp_path)
    conn = connect(str(db_path))
    students = list_students(conn, 1)
    conn.close()
    assert len(students) == 5  # Updated to 5 students
    assert students[0]['last_name'] in ('Diaz', 'Johnson', 'Quinn', 'Qureshi', 'Smith')


def test_assignment_stats_for_discussion_1(tmp_path):
    db_path = create_test_db(tmp_path)
    conn = connect(str(db_path))
    row = get_assignment_stats(conn, 1, 'Discussion 1')[0]
    conn.close()
    assert round(row['avg_score'], 2) == 8.8  # Updated average with 5 students
    assert row['max_score_value'] == 10
    assert row['min_score_value'] == 7


def test_compute_student_grade(tmp_path):
    db_path = create_test_db(tmp_path)
    conn = connect(str(db_path))
    grade = compute_student_grade(conn, 1, 1)
    conn.close()
    assert pytest.approx(87.5, rel=1e-4) == grade


def test_compute_student_grade_drop_lowest_homework(tmp_path):
    db_path = create_test_db(tmp_path)
    conn = connect(str(db_path))
    grade_drop = compute_student_grade_drop_lowest(conn, 1, 1, 'Homework')
    conn.close()
    conn2 = connect(str(db_path))
    grade_full = compute_student_grade(conn2, 1, 1)
    conn2.close()
    assert grade_drop >= grade_full


def test_add_assignment_inserts_record(tmp_path):
    from gradebook import add_assignment
    db_path = create_test_db(tmp_path)
    conn = connect(str(db_path))
    add_assignment(conn, 1, 'Homework', 'Homework 4', 20)
    row = conn.execute("SELECT * FROM Assignment WHERE name = 'Homework 4'").fetchone()
    conn.close()
    assert row is not None
    assert row['max_score'] == 20
