-- Sample Data for Grade Book Database

-- Insert Courses
INSERT INTO Course (department, course_number, course_name, semester, year)
VALUES
('CS', '101', 'Introduction to Databases', 'Fall', 2025),
('CS', '201', 'Data Structures', 'Spring', 2026);

-- Insert Categories for Course 1
INSERT INTO Category (course_id, name, weight_percent)
VALUES
(1, 'Participation', 10),
(1, 'Homework', 20),
(1, 'Tests', 50),
(1, 'Projects', 20);

-- Insert Categories for Course 2
INSERT INTO Category (course_id, name, weight_percent)
VALUES
(2, 'Participation', 15),
(2, 'Homework', 25),
(2, 'Tests', 40),
(2, 'Projects', 20);

-- Insert Students
INSERT INTO Student (first_name, last_name, email)
VALUES
('Alice', 'Smith', 'alice.smith@example.com'),
('Bob', 'Qureshi', 'bob.qureshi@example.com'),
('Carol', 'Diaz', 'carol.diaz@example.com'),
('David', 'Quinn', 'david.quinn@example.com'),
('Eve', 'Johnson', 'eve.johnson@example.com'),
('Frank', 'Williams', 'frank.williams@example.com');

-- Insert Enrollments
INSERT INTO Enrollment (student_id, course_id)
VALUES
(1, 1), (2, 1), (3, 1), (4, 1), (5, 1),  -- Course 1 students
(1, 2), (2, 2), (3, 2), (6, 2);          -- Course 2 students

-- Insert Assignments for Course 1
INSERT INTO Assignment (course_id, category_id, name, max_score, due_date)
VALUES
(1, 1, 'Discussion 1', 10, '2025-09-08'),
(1, 1, 'Discussion 2', 10, '2025-09-22'),
(1, 2, 'Homework 1', 20, '2025-09-12'),
(1, 2, 'Homework 2', 20, '2025-09-26'),
(1, 2, 'Homework 3', 20, '2025-10-10'),
(1, 3, 'Midterm', 100, '2025-10-20'),
(1, 3, 'Final', 100, '2025-12-12'),
(1, 4, 'Project 1', 100, '2025-11-05'),
(1, 4, 'Project 2', 100, '2025-12-08');

-- Insert Assignments for Course 2
-- Category IDs 5-8 are the Course 2 categories (Participation=5, Homework=6, Tests=7, Projects=8)
INSERT INTO Assignment (course_id, category_id, name, max_score, due_date)
VALUES
(2, 5, 'Discussion 1', 15, '2026-01-15'),
(2, 5, 'Discussion 2', 15, '2026-02-01'),
(2, 6, 'Homework 1', 25, '2026-01-20'),
(2, 6, 'Homework 2', 25, '2026-02-05'),
(2, 7, 'Midterm', 100, '2026-02-15'),
(2, 7, 'Final', 100, '2026-04-30'),
(2, 8, 'Project 1', 100, '2026-03-10'),
(2, 8, 'Project 2', 100, '2026-04-20');

-- Insert Scores for Course 1
INSERT INTO Score (student_id, assignment_id, score)
VALUES
-- Alice (1)
(1, 1, 9), (1, 2, 8), (1, 3, 18), (1, 4, 19), (1, 5, 17), (1, 6, 82), (1, 7, 90), (1, 8, 88), (1, 9, 92),
-- Bob (2)
(2, 1, 10), (2, 2, 9), (2, 3, 16), (2, 4, 15), (2, 5, 18), (2, 6, 76), (2, 7, 84), (2, 8, 95), (2, 9, 91),
-- Carol (3)
(3, 1, 7), (3, 2, 8), (3, 3, 15), (3, 4, 17), (3, 5, 16), (3, 6, 70), (3, 7, 75), (3, 8, 80), (3, 9, 85),
-- David (4)
(4, 1, 10), (4, 2, 10), (4, 3, 20), (4, 4, 20), (4, 5, 19), (4, 6, 88), (4, 7, 94), (4, 8, 96), (4, 9, 98),
-- Eve (5)
(5, 1, 8), (5, 2, 9), (5, 3, 17), (5, 4, 18), (5, 5, 16), (5, 6, 78), (5, 7, 85), (5, 8, 82), (5, 9, 87);

-- Insert Scores for Course 2
INSERT INTO Score (student_id, assignment_id, score)
VALUES
-- Alice (1)
(1, 10, 14), (1, 11, 13), (1, 12, 22), (1, 13, 24), (1, 14, 85), (1, 15, 92), (1, 16, 90), (1, 17, 95),
-- Bob (2)
(2, 10, 15), (2, 11, 14), (2, 12, 20), (2, 13, 23), (2, 14, 80), (2, 15, 88), (2, 16, 85), (2, 17, 90),
-- Carol (3)
(3, 10, 12), (3, 11, 11), (3, 12, 18), (3, 13, 21), (3, 14, 75), (3, 15, 80), (3, 16, 78), (3, 17, 82),
-- Frank (6)
(6, 10, 13), (6, 11, 12), (6, 12, 19), (6, 13, 22), (6, 14, 82), (6, 15, 89), (6, 16, 88), (6, 17, 93);
