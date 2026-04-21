# Presentation Script — Grade Book Database
# Say this out loud. Lines in [brackets] are stage directions — do NOT read them.

---

## OPENING  (30 seconds)

"Good [morning/afternoon]. My name is Gerald, and my project is a Grade Book
Database System built with SQLite and Python.

The problem it solves is this — a professor teaches multiple courses. Every
course has its own grading breakdown, like 10% participation, 20% homework,
50% tests, 20% projects. And the number of assignments in each category can
change at any time. My database handles all of that automatically.

I'll walk you through the design, show you the actual data in the tables,
run through the queries, and explain how the grade calculation works."

---

## PART 1 — DATABASE DESIGN  (1.5 minutes)

[Pull up the ER diagram]

"The database has six tables. Let me go through them quickly.

**Student** and **Course** are independent — Student stores name and email,
Course stores department, course number, name, semester, and year.

Since a student can enroll in many courses and a course can have many students,
I resolved that many-to-many relationship with an **Enrollment** table — it
just holds a student ID and a course ID.

On the course side, each course has grading **Categories** — Participation,
Homework, Tests, Projects. Each category has a weight percentage. All weights
for a course must add up to 100.

Each category contains **Assignments** — so Homework might have three homework
assignments. Each assignment has a name, a max score, and a due date.

Finally, the **Score** table is where the actual grades live. One row per
student per assignment. That's another many-to-many relationship — one student
has many scores, one assignment has many students' scores.

So the structure is: Course drives Category drives Assignment on one side.
Student connects to Course through Enrollment. And Student plus Assignment
meets in Score."

---

## PART 2 — SHOWING THE TABLES  (1.5 minutes)

[Open terminal, navigate to project folder]

```
cd ~/gradebook-db
python3 show_tables.py
```

"I wrote a script called show_tables.py specifically to display every table
with its inserted data. It runs against either a database file or a fresh
in-memory database built from the schema and seed files — so the output is
always reproducible.

Let me walk through what you're seeing.

**Course table** — two courses. CS 101 Introduction to Databases in Fall 2025,
and CS 201 Data Structures in Spring 2026.

**Category table** — eight rows, four categories per course. Course 1 is
weighted 10-20-50-20. Course 2 is weighted 15-25-40-20. Every category links
back to its course through course_id.

**Student table** — six students. Notice two of them — Bob Qureshi and David
Quinn — have a Q in their last name. That matters for one of the queries later.

**Enrollment table** — nine rows. Five students are in Course 1, four are in
Course 2. Alice, Bob, and Carol are in both courses.

**Assignment table** — seventeen assignments total. Course 1 has nine: two
discussions, three homeworks, a midterm, a final, and two projects. Course 2
has eight. Every assignment links to a category and a course.

**Score table** — seventy-seven rows. One row for every student-assignment
combination. You can see the scores spread across both courses."

---

## PART 3 — THE QUERIES  (2 minutes)

[Switch to queries.sql or run gradebook.py --demo demo.db]

"Now let me walk through the required queries.

**Average, highest, lowest score on an assignment** — for Discussion 1 in
Course 1, the average is 8.8 out of 10, the highest is 10, the lowest is 7.
Simple aggregation with AVG, MAX, MIN grouped by assignment.

**List students in a course** — for Course 1, that returns five students
sorted alphabetically: Diaz, Johnson, Quinn, Qureshi, Smith.

**All students with all their scores** — this is a five-table join: Student,
Enrollment, Score, Assignment, Category. Every student gets a row per
assignment showing what category it belongs to, what they scored, and what
the max was.

**Add an assignment** — I add 'Homework 4' to Course 1 by looking up the
category ID for Homework in that course and inserting a new row. The category
weight doesn't change — it just means each homework is now worth a smaller
fraction of that 20%.

**Change category weights** — I shift 5% from Participation to Homework.
The Python function validates that the new weights still sum to 100 before
saving anything.

**Add 2 points to all students on an assignment** — straightforward UPDATE
on the Score table filtered by assignment ID.

**Add 2 points only to students whose last name contains Q** — same UPDATE
but with a subquery that filters the Student table for last names that
LIKE '%Q%'. That catches both Qureshi and Quinn."

---

## PART 4 — GRADE CALCULATION  (1.5 minutes)

"The grade formula is the most interesting part.

For each category, I normalize every score — divide each score by its max —
then take the average of those normalized values, then multiply by the
category's weight.

Let me walk through Alice Smith's grade for Course 1:

    Participation  10%  —  avg(9/10, 8/10) = 0.85  →  0.85 × 10 =  8.5
    Homework       20%  —  avg(18/20, 19/20, 17/20) = 0.90  →  0.90 × 20 = 18.0
    Tests          50%  —  avg(82/100, 90/100) = 0.86  →  0.86 × 50 = 43.0
    Projects       20%  —  avg(88/100, 92/100) = 0.90  →  0.90 × 20 = 18.0

    Final grade = 8.5 + 18.0 + 43.0 + 18.0 = 87.5

The system returns exactly 87.5. And because the formula divides by however
many assignments exist in each category, it automatically adjusts whenever
a new assignment is added.

For the drop-lowest version, I use a SQL window function — ROW_NUMBER —
to rank each assignment within its category from lowest normalized score
to highest. Then I exclude rank 1, but only if the category has more than
one assignment. That prevents a student's only test from getting dropped.
For Bob Qureshi, dropping his lowest homework raises his overall grade slightly."

---

## CLOSING  (20 seconds)

"That covers the full system — the design, the data, all nine required queries,
and both grade computation modes. The source code, SQL scripts, ER diagram,
and test cases are all in the GitHub repository.

Happy to answer any questions."

---

## LIKELY QUESTIONS

---

**Q: Why a separate Score table instead of storing scores on Assignment?**

"If scores were on Assignment, I'd need a column per student — that breaks
normalization. The Score table gives me one row per student-assignment pair.
I can add or remove students without touching the Assignment table at all."

---

**Q: What if category weights don't add up to 100?**

"The Python function checks the total before saving. If the sum isn't 100,
it raises an error and rolls back. The SQL schema enforces that individual
weights are between 0 and 100, but the sum-to-100 rule needs Python because
SQL CHECK constraints can't span multiple rows in SQLite."

---

**Q: What happens if a student hasn't submitted an assignment?**

"The Score table only has a row when a score exists. The grade query uses
an inner join, so missing assignments simply aren't counted. If a professor
wants a missing submission to count as zero, they insert a Score row with
score equals zero. That's a policy decision — the database doesn't assume
either way."

---

**Q: Is this third normal form?**

"Yes. Every non-key attribute depends only on its table's primary key.
Student data is stored once. Category weights are stored once. No transitive
dependencies — for example, Assignment stores a foreign key to Category,
not the category name itself."

---

> **Three things to practice out loud before you present:**
> 1. The six-table walkthrough — know the names and relationships cold
> 2. Alice's grade math — write the numbers on paper and say them slowly
> 3. The Score table question — it comes up almost every time
