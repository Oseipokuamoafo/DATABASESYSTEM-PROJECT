-- Grade Book Database Schema
-- Normalized to 3NF: All attributes depend on the key, no transitive dependencies

PRAGMA foreign_keys = ON;

-- Course entity: Independent, no dependencies
CREATE TABLE IF NOT EXISTS Course (
    course_id INTEGER PRIMARY KEY AUTOINCREMENT,
    department TEXT NOT NULL,
    course_number TEXT NOT NULL,
    course_name TEXT NOT NULL,
    semester TEXT NOT NULL,
    year INTEGER NOT NULL,
    UNIQUE(department, course_number, semester, year)  -- Prevent duplicate courses
);

-- Category entity: Depends on Course
CREATE TABLE IF NOT EXISTS Category (
    category_id INTEGER PRIMARY KEY AUTOINCREMENT,
    course_id INTEGER NOT NULL,
    name TEXT NOT NULL,
    weight_percent REAL NOT NULL CHECK(weight_percent >= 0 AND weight_percent <= 100),
    FOREIGN KEY(course_id) REFERENCES Course(course_id) ON DELETE CASCADE,
    UNIQUE(course_id, name)  -- Category names unique per course
);

-- Student entity: Independent
CREATE TABLE IF NOT EXISTS Student (
    student_id INTEGER PRIMARY KEY AUTOINCREMENT,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE
);

-- Enrollment entity: Resolves M:N between Student and Course
CREATE TABLE IF NOT EXISTS Enrollment (
    enrollment_id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id INTEGER NOT NULL,
    course_id INTEGER NOT NULL,
    FOREIGN KEY(student_id) REFERENCES Student(student_id) ON DELETE CASCADE,
    FOREIGN KEY(course_id) REFERENCES Course(course_id) ON DELETE CASCADE,
    UNIQUE(student_id, course_id)  -- One enrollment per student per course
);

-- Assignment entity: Depends on Course and Category
CREATE TABLE IF NOT EXISTS Assignment (
    assignment_id INTEGER PRIMARY KEY AUTOINCREMENT,
    course_id INTEGER NOT NULL,
    category_id INTEGER NOT NULL,
    name TEXT NOT NULL,
    max_score REAL NOT NULL DEFAULT 100 CHECK(max_score > 0),
    due_date TEXT,  -- ISO date format YYYY-MM-DD
    FOREIGN KEY(course_id) REFERENCES Course(course_id) ON DELETE CASCADE,
    FOREIGN KEY(category_id) REFERENCES Category(category_id) ON DELETE CASCADE,
    UNIQUE(course_id, name)  -- Assignment names unique per course
);

-- Score entity: Resolves M:N between Student and Assignment
CREATE TABLE IF NOT EXISTS Score (
    score_id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id INTEGER NOT NULL,
    assignment_id INTEGER NOT NULL,
    score REAL NOT NULL CHECK(score >= 0),
    FOREIGN KEY(student_id) REFERENCES Student(student_id) ON DELETE CASCADE,
    FOREIGN KEY(assignment_id) REFERENCES Assignment(assignment_id) ON DELETE CASCADE,
    UNIQUE(student_id, assignment_id)  -- One score per student per assignment
);
