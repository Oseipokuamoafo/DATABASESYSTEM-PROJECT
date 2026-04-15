-- Grade Book Database Queries
-- All required queries for the assignment

-- a) Compute average, highest, and lowest score for an assignment
-- Example: For 'Discussion 1' in course 1
SELECT a.name AS assignment_name,
       AVG(s.score) AS average_score,
       MAX(s.score) AS highest_score,
       MIN(s.score) AS lowest_score
FROM Assignment a
JOIN Score s ON s.assignment_id = a.assignment_id
WHERE a.course_id = 1 AND a.name = 'Discussion 1'
GROUP BY a.assignment_id;

-- b) List all students in a given course
-- Example: Course 1
SELECT s.student_id, s.first_name, s.last_name, s.email
FROM Student s
JOIN Enrollment e ON e.student_id = s.student_id
WHERE e.course_id = 1
ORDER BY s.last_name, s.first_name;

-- c) List all students in a course with ALL their assignment scores
-- Example: Course 1
SELECT s.student_id, s.first_name, s.last_name, a.name AS assignment_name,
       c.name AS category_name, sc.score, a.max_score
FROM Student s
JOIN Enrollment e ON e.student_id = s.student_id
JOIN Score sc ON sc.student_id = s.student_id
JOIN Assignment a ON a.assignment_id = sc.assignment_id
JOIN Category c ON c.category_id = a.category_id
WHERE e.course_id = 1 AND a.course_id = 1
ORDER BY s.last_name, s.first_name, c.category_id, a.assignment_id;

-- d) Add a new assignment to a course
-- Example: Add 'Homework 4' to Course 1, Category 'Homework'
INSERT INTO Assignment (course_id, category_id, name, max_score, due_date)
SELECT 1, category_id, 'Homework 4', 20, '2025-11-14'
FROM Category
WHERE course_id = 1 AND name = 'Homework';

-- e) Update category percentages
-- Example: Shift 5% from Participation to Homework for Course 1
-- Before: Participation=10, Homework=20, Tests=50, Projects=20  (total=100)
-- After:  Participation=5,  Homework=25, Tests=50, Projects=20  (total=100)
UPDATE Category SET weight_percent = 5  WHERE course_id = 1 AND name = 'Participation';
UPDATE Category SET weight_percent = 25 WHERE course_id = 1 AND name = 'Homework';

-- f) Add 2 points to all students for a specific assignment
-- Example: Add 2 points to 'Homework 1'
UPDATE Score SET score = score + 2
WHERE assignment_id = (SELECT assignment_id FROM Assignment WHERE course_id = 1 AND name = 'Homework 1');

-- g) Add 2 points ONLY to students whose last name contains 'Q'
-- Example: For 'Homework 1'
UPDATE Score SET score = score + 2
WHERE assignment_id = (SELECT assignment_id FROM Assignment WHERE course_id = 1 AND name = 'Homework 1')
  AND student_id IN (SELECT student_id FROM Student WHERE last_name LIKE '%Q%' OR last_name LIKE '%q%');

-- h) Compute final grade for a student using weighted categories
-- Formula: sum over categories of (weight_percent * avg_normalized_score)
-- Example: Student 1 (Alice Smith) in Course 1
SELECT s.first_name, s.last_name,
       ROUND(SUM(cat_contribution), 2) AS final_grade
FROM Student s,
     (SELECT c.weight_percent * AVG(sc.score / a.max_score) AS cat_contribution
      FROM Category c
      JOIN Assignment a ON a.category_id = c.category_id AND a.course_id = c.course_id
      JOIN Score sc     ON sc.assignment_id = a.assignment_id
      WHERE c.course_id = 1 AND sc.student_id = 1
      GROUP BY c.category_id) AS contributions
WHERE s.student_id = 1;

-- i) Compute final grade where the lowest-scoring assignment per category is dropped
-- (Only dropped when the category has more than one graded assignment)
-- Example: Student 1 (Alice Smith) in Course 1
WITH ranked AS (
    SELECT c.category_id, c.weight_percent,
           sc.score, a.max_score,
           ROW_NUMBER() OVER (
               PARTITION BY c.category_id
               ORDER BY sc.score / a.max_score ASC
           ) AS rn,
           COUNT(*) OVER (PARTITION BY c.category_id) AS total_in_cat
    FROM Category c
    JOIN Assignment a ON a.category_id = c.category_id AND a.course_id = c.course_id
    JOIN Score sc     ON sc.assignment_id = a.assignment_id
    WHERE c.course_id = 1 AND sc.student_id = 1
)
SELECT ROUND(SUM(cat_contribution), 2) AS final_grade_drop_lowest
FROM (
    SELECT category_id, weight_percent,
           weight_percent * AVG(score / max_score) AS cat_contribution
    FROM ranked
    WHERE NOT (rn = 1 AND total_in_cat > 1)   -- exclude the single lowest per category
    GROUP BY category_id, weight_percent
);
