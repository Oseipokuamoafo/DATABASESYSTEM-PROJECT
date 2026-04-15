# Grade Book Database System

## Project Title
University Grade Book Database System

## Description
This project implements a comprehensive grade book database system for university professors to track student grades across multiple courses. The system supports dynamic assignment categories, weighted grading, and various query operations for grade management.

### Key Features
- Multi-course support with enrollment tracking
- Dynamic categories (Participation, Homework, Tests, Projects, etc.)
- Weighted grade calculations
- Assignment management with due dates
- Student score tracking
- Advanced queries for statistics and grade computation

## Tools Required
- SQLite 3 (or any SQL database supporting foreign keys)
- Python 3.8+ (for running the provided scripts)
- Any SQL client (e.g., SQLite CLI, DBeaver, or VS Code SQL extensions)

## How to Run the SQL

### Option 1: Using SQLite CLI
1. Open terminal in the project directory
2. Run: `sqlite3 gradebook.db`
3. Execute: `.read schema.sql`
4. Execute: `.read seed.sql`
5. Execute queries from `queries.sql`

### Option 2: Using Python Script
1. Ensure Python 3.8+ is installed
2. Run: `python3 gradebook.py --init-db gradebook.db`
3. Run: `python3 gradebook.py --seed-db gradebook.db`
4. Run: `python3 gradebook.py --demo gradebook.db`

### Option 3: Using Any SQL Client
1. Create a new SQLite database file
2. Execute `schema.sql` to create tables
3. Execute `seed.sql` to insert sample data
4. Execute individual queries from `queries.sql`

## Step-by-Step Execution Instructions

1. **Setup Database Schema**
   ```sql
   -- Run in SQL client
   .read schema.sql
   ```

2. **Insert Sample Data**
   ```sql
   -- Run in SQL client
   .read seed.sql
   ```

3. **Verify Data Insertion**
   ```sql
   SELECT * FROM Course;
   SELECT * FROM Student;
   -- etc.
   ```

4. **Run Required Queries**
   - Copy and execute queries from `queries.sql`
   - Modify parameters as needed (e.g., course_id, student_id)

5. **Run Tests**
   ```bash
   python3 -m pytest tests/test_gradebook.py
   ```

## Test Cases

### Test Case 1: Assignment Statistics
**Input:** Course ID = 1, Assignment Name = 'Discussion 1'  
**Query:** See queries.sql section a)  
**Expected Output:**
| assignment_name | average_score | highest_score | lowest_score |
|----------------:|--------------:|--------------:|-------------:|
| Discussion 1    | 8.8           | 10            | 7            |

**Explanation:** Calculates aggregate statistics for the specified assignment across all enrolled students.

### Test Case 2: Student List
**Input:** Course ID = 1  
**Query:** See queries.sql section b)  
**Expected Output:** List of 5 students sorted by last name  
**Explanation:** Retrieves all students enrolled in the specified course.

### Test Case 3: Student Scores
**Input:** Course ID = 1  
**Query:** See queries.sql section c)  
**Expected Output:** 45 rows (5 students × 9 assignments) with scores and max scores  
**Explanation:** Shows complete grade breakdown for all students in a course.

### Test Case 4: Add Assignment
**Input:** Course ID = 1, Category = 'Homework', Name = 'Homework 4', Max Score = 20  
**Query:** See queries.sql section d)  
**Expected Output:** New assignment inserted successfully  
**Explanation:** Dynamically adds assignments to existing categories.

### Test Case 5: Update Weights
**Input:** Course ID = 1, shift 5% from Participation (10→5%) to Homework (20→25%)  
**Query:** See queries.sql section e)  
**Expected Output:** Participation=5, Homework=25, Tests=50, Projects=20 — total = 100%  
**Explanation:** Demonstrates that category weights can be redistributed while keeping the sum at 100%.

### Test Case 6: Add Points to All
**Input:** Assignment ID for 'Homework 1', Points = 2  
**Query:** See queries.sql section f)  
**Expected Output:** All student scores for that assignment increased by 2  
**Explanation:** Bulk grade adjustment for curve or bonus points.

### Test Case 7: Add Points to Q Names
**Input:** Assignment ID for 'Homework 1', Points = 2, Last Name contains 'Q'  
**Query:** See queries.sql section g)  
**Expected Output:** Only Bob Qureshi and David Quinn scores increased  
**Explanation:** Targeted grade adjustment based on name criteria.

### Test Case 8: Compute Final Grade
**Input:** Student ID = 1, Course ID = 1  
**Query:** See queries.sql section h)  
**Expected Output:** Final grade ≈ 87.5%  
**Explanation:** Weighted average across all categories.

### Test Case 9: Compute Grade with Drop
**Input:** Student ID = 1 (Alice Smith), Course ID = 1  
**Query:** See queries.sql section i)  
**Expected Output:** 90.9 — the lowest assignment in *each* category is dropped:
- Participation: drop 8/10, keep 9/10 → 9.0 pts
- Homework: drop 17/20, keep 18 & 19 → 18.5 pts
- Tests: drop 82/100, keep 90/100 → 45.0 pts
- Projects: drop 88/100, keep 92/100 → 18.4 pts

**Python variant** (`compute_student_grade_drop_lowest(..., 'Homework')`): drops lowest only in the named category → 88.0%  
**Explanation:** Demonstrates two drop-lowest policies: per-category SQL and targeted Python.

## Files Structure
- `schema.sql`: Database schema creation
- `seed.sql`: Sample data insertion
- `queries.sql`: All required query implementations
- `gradebook.py`: Python utility script
- `tests/test_gradebook.py`: Automated tests
- `ER_diagram.md`: Entity-relationship design
- `sample_output.md`: Expected query results
- `README.md`: This documentation

## Grading Notes
This submission includes all required components:
- Complete ER diagram with Mermaid visualization
- Normalized 3NF schema with constraints
- Comprehensive sample data (6 students, 2 courses, 17 assignments)
- All 9 required queries implemented
- Test cases with expected outputs
- Clean, documented code ready for submission
