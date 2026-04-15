# Grade Book Database System — Project Report

**Course:** Database Systems  
**Project:** Grade Book Database  

---

## 1. Introduction

Keeping track of student grades across multiple courses is something every professor has to deal with, but it gets complicated fast. A professor might teach two or three different courses in a semester, each with its own grading breakdown — some courses weight tests heavily, others care more about projects or participation. On top of that, the number of assignments in each category is not fixed. A professor might add a surprise quiz or an extra homework at any point in the semester.

The goal of this project was to design and implement a relational database system that handles exactly this situation. The system allows a professor to:

- Track multiple courses, each with its own grading categories and weights
- Manage a variable number of assignments per category
- Record scores for each student on each assignment
- Run useful queries — like listing all students in a course, computing final grades, or giving bonus points to the whole class

The database was built using SQLite, with a Python script layered on top to make the common operations easier to run. All the raw SQL queries are also provided separately so the system can be used with any SQL client.

---

## 2. Design Decisions

### 2.1 Why Six Tables?

The first challenge was figuring out how to represent the data without repeating information. The natural entities in this problem are students, courses, and assignments. But between them there are relationships that are not simple — a student can be in many courses, and a course has many students. An assignment belongs to a category, and a category belongs to a course.

After working through those relationships, six tables emerged:

| Table | Purpose |
|-------|---------|
| **Student** | Stores each student once — name and email |
| **Course** | Stores each course — department, number, name, semester, year |
| **Category** | Stores grading categories per course (e.g., Homework = 20%) |
| **Assignment** | Stores individual assignments, linked to a category and course |
| **Enrollment** | Resolves the many-to-many relationship between Student and Course |
| **Score** | Resolves the many-to-many relationship between Student and Assignment |

The key insight was that **Category sits between Course and Assignment**. A course defines its grading breakdown through categories, and each assignment belongs to one of those categories. This is what makes the per-category weighting work correctly — if a course has 5 homework assignments and Homework is worth 20%, each homework is automatically worth 20%/5 = 4% of the final grade.

### 2.2 Normalization

The schema was designed to be in Third Normal Form (3NF). Each non-key attribute depends only on the primary key of its table, not on another non-key attribute. For example, student information (name, email) lives only in the Student table — it is never repeated in Enrollment or Score. Category weights are stored only in Category, not duplicated per assignment.

The one deliberate denormalization was keeping `course_id` in the Assignment table alongside `category_id`. Technically, the course could be inferred by following Assignment → Category → Course. But storing it directly makes course-level queries faster and more readable without violating normalization rules, since `course_id` in Assignment is always consistent with its category's `course_id` (enforced by the application layer).

### 2.3 Constraints

Several constraints were added to protect data integrity:

- `UNIQUE(student_id, course_id)` in Enrollment — a student cannot be enrolled twice in the same course
- `UNIQUE(student_id, assignment_id)` in Score — one score per student per assignment
- `CHECK(weight_percent >= 0 AND weight_percent <= 100)` in Category
- `CHECK(score >= 0)` in Score
- The requirement that category weights sum to 100% per course is enforced in the Python layer using a validation check before any update is committed

---

## 3. Task Implementations

**Task 4 — Assignment Statistics:**  
A single `SELECT` with `AVG()`, `MAX()`, and `MIN()` aggregates, joined across Assignment and Score, filtered by course and assignment name. Straightforward but useful for a professor checking how a class performed on a specific assignment.

**Task 5 — List Students in a Course:**  
Joins Student with Enrollment and filters by `course_id`. Results are ordered alphabetically by last name.

**Task 6 — Students and All Their Scores:**  
A multi-table join across Student, Enrollment, Score, Assignment, and Category, filtered by `course_id` on both the enrollment and the assignment side. This ensures only scores relevant to the selected course appear.

**Task 7 — Add an Assignment:**  
The Python function looks up the `category_id` by category name and course, then inserts a new row into Assignment. The SQL version uses a subquery inside the `INSERT` to do the same lookup in one statement.

**Task 8 — Change Category Weights:**  
The Python function validates that the new weights sum to 100 before issuing any `UPDATE` statements. If the total is off, it raises an error rather than saving an inconsistent state. This validation is the most important safeguard in the whole system.

**Tasks 9 & 10 — Add Bonus Points:**  
Task 9 updates all scores for a given assignment with `score + 2`. Task 10 adds a filter using `WHERE student_id IN (SELECT student_id FROM Student WHERE last_name LIKE '%Q%')` to target only students whose last name contains the letter Q. Both Bob Qureshi and David Quinn are correctly affected.

**Task 11 — Compute Final Grade:**  
For each category, the average normalized score is calculated (`AVG(score / max_score)`), then multiplied by the category's weight percentage. The sum of all category contributions is the final grade on a 0–100 scale. This correctly handles categories with different numbers of assignments and different maximum scores.

**Task 12 — Grade with Lowest Dropped:**  
This was the most complex query. A Common Table Expression (CTE) uses `ROW_NUMBER()` with `PARTITION BY category_id ORDER BY score/max_score ASC` to rank each assignment within its category from lowest to highest. The lowest-ranked assignment is excluded from the average calculation, but only if the category has more than one graded assignment. Without that condition, a student with only one test would have their only score dropped, which would be wrong.

---

## 4. Challenges

**Cross-Course Score Contamination:**  
The most significant bug discovered during testing was that the seed data for Course 2 assignments incorrectly referenced the category IDs belonging to Course 1 (IDs 1–4 instead of 5–8). Because the grade computation query filtered by `Category.course_id` but joined Assignment only on `category_id`, Course 2 assignments were silently included in Course 1 grade calculations. Alice's grade was computed as 88.8% instead of the correct 87.5%. The fix required correcting the seed data and adding `AND a.course_id = c.course_id` to the join condition in the grade functions as a defensive guard.

**Grade Formula Consistency:**  
There are two common ways to compute a weighted category grade — averaging the normalized scores, or summing all earned points divided by total possible points. For assignments with equal max scores within a category (which is the case in this dataset), both methods give the same result. The "average of normalized scores" approach was chosen because it explicitly implements the problem statement's rule: if there are 5 homeworks and Homework is worth 20%, each homework contributes 4%.

**Drop-Lowest Query:**  
Writing the drop-lowest SQL as a single query without procedural code took a few attempts. The solution uses two layers: the CTE computes ranks and counts per category using window functions, and the outer query filters out the lowest-ranked row before computing the weighted average.

---

## 5. Conclusion

This project resulted in a fully functional grade book database that covers all twelve required operations. The six-table normalized schema cleanly separates the concerns of course structure, student enrollment, assignment definition, and score recording. The Python script makes the system easy to run from the command line, while the SQL queries file provides the raw statements for use in any SQL client.

The most valuable lesson from this project was about data integrity: one wrong foreign key in the seed data silently corrupted grade calculations for all students. It was only caught by carefully checking the computed output against hand-calculated expected values. This reinforced the importance of writing tests that verify not just that queries run, but that they return mathematically correct results.

---

*All source files, SQL scripts, and test cases are available in the project repository.*
