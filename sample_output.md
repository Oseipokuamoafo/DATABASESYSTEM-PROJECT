# Sample Output

## Table Contents After Seeding

### Course
| course_id | department | course_number | course_name              | semester | year |
|----------:|------------|---------------|--------------------------|----------|-----:|
| 1         | CS         | 101           | Introduction to Databases | Fall     | 2025 |
| 2         | CS         | 201           | Data Structures          | Spring   | 2026 |

### Category
| category_id | course_id | name          | weight_percent |
|-----------:|----------:|---------------|---------------:|
| 1          | 1         | Participation | 10             |
| 2          | 1         | Homework      | 20             |
| 3          | 1         | Tests         | 50             |
| 4          | 1         | Projects      | 20             |
| 5          | 2         | Participation | 15             |
| 6          | 2         | Homework      | 25             |
| 7          | 2         | Tests         | 40             |
| 8          | 2         | Projects      | 20             |

### Student
| student_id | first_name | last_name | email                      |
|----------:|------------|-----------|----------------------------|
| 1         | Alice      | Smith     | alice.smith@example.com    |
| 2         | Bob        | Qureshi   | bob.qureshi@example.com    |
| 3         | Carol      | Diaz      | carol.diaz@example.com     |
| 4         | David      | Quinn     | david.quinn@example.com    |
| 5         | Eve        | Johnson   | eve.johnson@example.com    |
| 6         | Frank      | Williams  | frank.williams@example.com |

### Enrollment
| enrollment_id | student_id | course_id |
|-------------:|-----------:|----------:|
| 1            | 1          | 1         |
| 2            | 2          | 1         |
| 3            | 3          | 1         |
| 4            | 4          | 1         |
| 5            | 5          | 1         |
| 6            | 1          | 2         |
| 7            | 2          | 2         |
| 8            | 3          | 2         |
| 9            | 6          | 2         |

### Assignment
| assignment_id | course_id | category_id | name         | max_score | due_date   |
|-------------:|----------:|------------:|--------------|----------:|------------|
| 1            | 1         | 1           | Discussion 1 | 10        | 2025-09-08 |
| 2            | 1         | 1           | Discussion 2 | 10        | 2025-09-22 |
| 3            | 1         | 2           | Homework 1   | 20        | 2025-09-12 |
| 4            | 1         | 2           | Homework 2   | 20        | 2025-09-26 |
| 5            | 1         | 2           | Homework 3   | 20        | 2025-10-10 |
| 6            | 1         | 3           | Midterm      | 100       | 2025-10-20 |
| 7            | 1         | 3           | Final        | 100       | 2025-12-12 |
| 8            | 1         | 4           | Project 1    | 100       | 2025-11-05 |
| 9            | 1         | 4           | Project 2    | 100       | 2025-12-08 |
| 10           | 2         | 5           | Discussion 1 | 15        | 2026-01-15 |
| 11           | 2         | 5           | Discussion 2 | 15        | 2026-02-01 |
| 12           | 2         | 6           | Homework 1   | 25        | 2026-01-20 |
| 13           | 2         | 6           | Homework 2   | 25        | 2026-02-05 |
| 14           | 2         | 7           | Midterm      | 100       | 2026-02-15 |
| 15           | 2         | 7           | Final        | 100       | 2026-04-30 |
| 16           | 2         | 8           | Project 1    | 100       | 2026-03-10 |
| 17           | 2         | 8           | Project 2    | 100       | 2026-04-20 |

### Score (Sample for Course 1, Alice Smith)
| score_id | student_id | assignment_id | score |
|---------:|-----------:|--------------:|------:|
| 1        | 1          | 1             | 9     |
| 2        | 1          | 2             | 8     |
| 3        | 1          | 3             | 18    |
| 4        | 1          | 4             | 19    |
| 5        | 1          | 5             | 17    |
| 6        | 1          | 6             | 82    |
| 7        | 1          | 7             | 90    |
| 8        | 1          | 8             | 88    |
| 9        | 1          | 9             | 92    |

## Example Query Results

### a) Assignment Stats for 'Discussion 1'
| assignment_name | average_score | highest_score | lowest_score |
|----------------:|--------------:|--------------:|-------------:|
| Discussion 1    | 8.8           | 10            | 7            |

### b) Students in Course 1
| student_id | first_name | last_name | email                      |
|-----------:|------------|-----------|----------------------------|
| 3          | Carol      | Diaz      | carol.diaz@example.com     |
| 5          | Eve        | Johnson   | eve.johnson@example.com    |
| 4          | David      | Quinn     | david.quinn@example.com    |
| 2          | Bob        | Qureshi   | bob.qureshi@example.com    |
| 1          | Alice      | Smith     | alice.smith@example.com    |

### c) Students with All Scores in Course 1 (Partial Sample)
| student_id | first_name | last_name | assignment_name | category_name | score | max_score |
|-----------:|------------|-----------|----------------:|---------------|------:|----------:|
| 1          | Alice      | Smith     | Discussion 1    | Participation | 9     | 10        |
| 1          | Alice      | Smith     | Discussion 2    | Participation | 8     | 10        |
| ...        | ...        | ...       | ...             | ...           | ...   | ...       |

### h) Final Grade for Alice Smith (Course 1)
-- Participation (10%): avg(9/10, 8/10) = 0.85 → 8.5
-- Homework     (20%): avg(18/20, 19/20, 17/20) = 0.90 → 18.0
-- Tests        (50%): avg(82/100, 90/100) = 0.86 → 43.0
-- Projects     (20%): avg(88/100, 92/100) = 0.90 → 18.0
| first_name | last_name | final_grade |
|------------|-----------|------------:|
| Alice      | Smith     | 87.5        |

### i) Final Grade with Lowest Assignment Dropped Per Category (Alice Smith)
-- Participation (10%): 2 assignments → drop 8/10, keep 9/10 → 9.0
-- Homework     (20%): 3 assignments → drop 17/20, keep 18/20 & 19/20 → avg=0.925 → 18.5
-- Tests        (50%): 2 assignments → drop 82/100, keep 90/100 → 45.0
-- Projects     (20%): 2 assignments → drop 88/100, keep 92/100 → 18.4
| student_id | final_grade_drop_lowest |
|-----------:|------------------------:|
| 1          | 90.9                    |
