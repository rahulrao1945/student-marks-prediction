Student Performance Dataset Generator

This repository includes a small Python script to generate a realistic synthetic Student Performance Prediction Dataset.

Usage:

Generate the full dataset (100,000 records):

```powershell
python generate_student_dataset.py --n 100000 --out student_performance_100k.csv --seed 42
```

Generate a smaller sample (e.g., 100 records):

```powershell
python generate_student_dataset.py --n 100 --out sample_students_100.csv --seed 42
```

Fields produced:
- student_id
- age
- gender
- parental_education
- family_income
- study_time_hours_per_week
- absences
- extracurricular
- internet_access
- health
- alcohol_weekend
- alcohol_weekday
- free_time
- failures
- past_grade_avg
- final_score
- final_result

The generator is deterministic with `--seed` for reproducibility. Adjust distributions or weights in `generate_student_dataset.py` as needed for research or modeling.