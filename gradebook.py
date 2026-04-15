import argparse
import sqlite3
from pathlib import Path

SCHEMA_FILE = Path(__file__).with_name('schema.sql')
SEED_FILE = Path(__file__).with_name('seed.sql')


def connect(db_path):
    conn = sqlite3.connect(db_path)
    conn.execute('PRAGMA foreign_keys = ON')
    conn.row_factory = sqlite3.Row
    return conn


def init_db(db_path):
    conn = connect(db_path)
    sql = SCHEMA_FILE.read_text()
    conn.executescript(sql)
    conn.commit()
    conn.close()
    print(f'Initialized database: {db_path}')


def seed_db(db_path):
    conn = connect(db_path)
    sql = SEED_FILE.read_text()
    conn.executescript(sql)
    conn.commit()
    conn.close()
    print(f'Seeded database: {db_path}')


def query(conn, sql, params=()):
    return conn.execute(sql, params).fetchall()


def get_assignment_stats(conn, course_id, assignment_name):
    sql = '''
    SELECT a.assignment_id, a.name AS assignment_name, a.max_score,
           AVG(s.score) AS avg_score,
           MAX(s.score) AS max_score_value,
           MIN(s.score) AS min_score_value
    FROM Assignment a
    JOIN Score s ON s.assignment_id = a.assignment_id
    WHERE a.course_id = ? AND a.name = ?
    GROUP BY a.assignment_id
    '''
    return query(conn, sql, (course_id, assignment_name))


def list_students(conn, course_id):
    sql = '''
    SELECT s.student_id, s.first_name, s.last_name, s.email
    FROM Student s
    JOIN Enrollment e ON e.student_id = s.student_id
    WHERE e.course_id = ?
    ORDER BY s.last_name, s.first_name
    '''
    return query(conn, sql, (course_id,))


def list_scores(conn, course_id):
    sql = '''
    SELECT s.student_id, s.first_name, s.last_name, a.name AS assignment_name,
           a.category_id, c.name AS category_name, sc.score, a.max_score
    FROM Student s
    JOIN Enrollment e ON e.student_id = s.student_id
    JOIN Score sc ON sc.student_id = s.student_id
    JOIN Assignment a ON a.assignment_id = sc.assignment_id
    JOIN Category c ON c.category_id = a.category_id
    WHERE e.course_id = ? AND a.course_id = ?
    ORDER BY s.last_name, s.first_name, c.category_id, a.assignment_id
    '''
    return query(conn, sql, (course_id, course_id))


def add_assignment(conn, course_id, category_name, assignment_name, max_score, due_date=None):
    sql = '''
    SELECT category_id FROM Category WHERE course_id = ? AND name = ?
    '''
    row = conn.execute(sql, (course_id, category_name)).fetchone()
    if not row:
        raise ValueError(f'Category {category_name} not found for course {course_id}')
    category_id = row['category_id']
    sql = '''
    INSERT INTO Assignment (course_id, category_id, name, max_score, due_date)
    VALUES (?, ?, ?, ?, ?)
    '''
    conn.execute(sql, (course_id, category_id, assignment_name, max_score, due_date))
    conn.commit()
    print(f'Added assignment "{assignment_name}" to course {course_id}')


def update_category_weights(conn, course_id, weights):
    total = sum(weights.values())
    if abs(total - 100.0) > 1e-6:
        raise ValueError('Category weights must sum to 100 percent')
    for name, weight in weights.items():
        conn.execute(
            'UPDATE Category SET weight_percent = ? WHERE course_id = ? AND name = ?',
            (weight, course_id, name)
        )
    conn.commit()
    print(f'Updated category weights for course {course_id}')


def add_points_to_assignment(conn, assignment_id, points):
    conn.execute(
        'UPDATE Score SET score = score + ? WHERE assignment_id = ?',
        (points, assignment_id)
    )
    conn.commit()
    print(f'Added {points} points to assignment {assignment_id}')


def add_points_lastname_contains_q(conn, assignment_id, points):
    conn.execute(
        '''
        UPDATE Score
        SET score = score + ?
        WHERE assignment_id = ?
          AND student_id IN (
              SELECT student_id FROM Student WHERE last_name LIKE '%Q%' OR last_name LIKE '%q%'
          )
        ''',
        (points, assignment_id)
    )
    conn.commit()
    print(f'Added {points} points to Q last-name students for assignment {assignment_id}')


def compute_student_grade(conn, student_id, course_id):
    sql = '''
    SELECT c.category_id, c.weight_percent, a.assignment_id,
           sc.score, a.max_score
    FROM Category c
    JOIN Assignment a ON a.category_id = c.category_id AND a.course_id = c.course_id
    LEFT JOIN Score sc ON sc.assignment_id = a.assignment_id AND sc.student_id = ?
    WHERE c.course_id = ?
    '''
    rows = query(conn, sql, (student_id, course_id))
    categories = {}
    for row in rows:
        cat_id = row['category_id']
        categories.setdefault(cat_id, {
            'weight': row['weight_percent'],
            'scores': []
        })
        if row['score'] is not None:
            categories[cat_id]['scores'].append((row['score'], row['max_score']))
    total = 0.0
    for cat in categories.values():
        if not cat['scores']:
            continue
        total_points = sum(score / max_score for score, max_score in cat['scores'])
        average = total_points / len(cat['scores'])
        total += average * cat['weight']
    return total


def compute_student_grade_drop_lowest(conn, student_id, course_id, category_name):
    sql = '''
    SELECT c.category_id, c.weight_percent, a.assignment_id,
           sc.score, a.max_score, c.name AS category_name
    FROM Category c
    JOIN Assignment a ON a.category_id = c.category_id AND a.course_id = c.course_id
    LEFT JOIN Score sc ON sc.assignment_id = a.assignment_id AND sc.student_id = ?
    WHERE c.course_id = ?
    '''
    rows = query(conn, sql, (student_id, course_id))
    categories = {}
    for row in rows:
        cat_id = row['category_id']
        categories.setdefault(cat_id, {
            'weight': row['weight_percent'],
            'name': row['category_name'],
            'scores': []
        })
        if row['score'] is not None:
            categories[cat_id]['scores'].append((row['score'], row['max_score']))
    total = 0.0
    for cat in categories.values():
        scores = cat['scores']
        if not scores:
            continue
        if cat['name'] == category_name and len(scores) > 1:
            lowest = min(scores, key=lambda item: item[0])
            scores = [item for item in scores if item is not lowest]
        total_points = sum(score / max_score for score, max_score in scores)
        average = total_points / len(scores)
        total += average * cat['weight']
    return total


def demo(db_path):
    conn = connect(db_path)
    print('--- Enrollment ---')
    for row in list_students(conn, 1):
        print(dict(row))
    print('\n--- Scores ---')
    for row in list_scores(conn, 1):
        print({k: row[k] for k in row.keys()})
    print('\n--- Participation stats for Discussion 1 ---')
    for row in get_assignment_stats(conn, 1, 'Discussion 1'):
        print(dict(row))
    print('\n--- Alice Smith grade ---')
    print(compute_student_grade(conn, 1, 1))
    print('\n--- Bob Qureshi grade drop lowest Homework ---')
    print(compute_student_grade_drop_lowest(conn, 2, 1, 'Homework'))
    conn.close()


def parse_args():
    parser = argparse.ArgumentParser(description='Grade Book Database manager')
    parser.add_argument('--init-db', dest='init_db', help='Initialize a new SQLite database file')
    parser.add_argument('--seed-db', dest='seed_db', help='Seed the SQLite database file')
    parser.add_argument('--demo', dest='demo', help='Run demo queries against the database file')
    parser.add_argument('--course-id', type=int, default=1, help='Course ID for query commands')
    parser.add_argument('--assignment-name', help='Assignment name for stats query')
    parser.add_argument('--student-id', type=int, help='Student ID for grade calculation')
    parser.add_argument('--drop-category', help='Category name to drop lowest score from')
    return parser.parse_args()


def main():
    args = parse_args()
    if args.init_db:
        init_db(args.init_db)
    elif args.seed_db:
        seed_db(args.seed_db)
    elif args.demo:
        demo(args.demo)
    else:
        print('Use --init-db, --seed-db, or --demo')


if __name__ == '__main__':
    main()
