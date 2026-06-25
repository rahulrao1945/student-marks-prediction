#!/usr/bin/env python3
import csv
import random
import argparse

GENDERS = ["Male", "Female", "Other"]
PARENT_EDU = ["none", "primary", "secondary", "associate", "bachelor", "master", "doctorate"]

def clamp(x, lo, hi):
    return max(lo, min(hi, x))

def parental_edu_score(level):
    scores = {
        "none": 0,
        "primary": 1,
        "secondary": 2,
        "associate": 3,
        "bachelor": 4,
        "master": 5,
        "doctorate": 6,
    }
    return scores.get(level, 2)

def generate_record(i, rng):
    age = int(rng.normalvariate(18, 2))
    age = clamp(age, 15, 23)
    gender = rng.choice(GENDERS)
    parent_edu = rng.choices(PARENT_EDU, weights=[1,5,25,20,30,15,4])[0]
    family_income = int(max(0, rng.normalvariate(50000, 20000)))
    study_time = round(abs(rng.normalvariate(10, 5)), 1)  # hours/week
    absences = int(rng.expovariate(1/3))  # mean ~3
    extracurricular = "Yes" if rng.random() < 0.4 else "No"
    internet = "Yes" if rng.random() < 0.85 else "No"
    health = rng.randint(1,5)
    alcohol_weekend = round(abs(rng.normalvariate(2,1.5)),1)  # scale 0-10
    alcohol_weekday = round(abs(rng.normalvariate(0.5,0.7)),1)
    free_time = rng.randint(1,5)
    failures = rng.choices([0,1,2,3], weights=[85,10,4,1])[0]
    past_avg = round(clamp(rng.normalvariate(70 - failures*8, 10), 0, 100),1)

    # Simple generative model for final score
    study_score = clamp((study_time / 20) * 100, 0, 100)
    income_factor = clamp((family_income / 100000) * 10, 0, 10)
    edu_factor = parental_edu_score(parent_edu) * 2
    health_factor = (health - 3) * 1.5
    absences_penalty = absences * 1.5
    extra_bonus = 3 if extracurricular == "Yes" else 0

    raw = (0.5 * past_avg) + (0.25 * study_score) + (0.08 * edu_factor) + (0.05 * income_factor) + (0.02 * extra_bonus) + health_factor - absences_penalty
    noise = rng.normalvariate(0, 6)
    final_score = clamp(round(raw + noise,1), 0, 100)
    pass_fail = "Pass" if final_score >= 50 else "Fail"

    return {
        "student_id": f"S{i:06d}",
        "age": age,
        "gender": gender,
        "parental_education": parent_edu,
        "family_income": family_income,
        "study_time_hours_per_week": study_time,
        "absences": absences,
        "extracurricular": extracurricular,
        "internet_access": internet,
        "health": health,
        "alcohol_weekend": alcohol_weekend,
        "alcohol_weekday": alcohol_weekday,
        "free_time": free_time,
        "failures": failures,
        "past_grade_avg": past_avg,
        "final_score": final_score,
        "final_result": pass_fail
    }

def main():
    parser = argparse.ArgumentParser(description="Generate synthetic student performance dataset")
    parser.add_argument("--n", type=int, default=100000, help="Number of records to generate (default 100000)")
    parser.add_argument("--out", type=str, default="student_performance.csv", help="Output CSV file")
    parser.add_argument("--seed", type=int, default=42, help="Random seed for reproducibility")
    args = parser.parse_args()

    rng = random.Random(args.seed)

    fieldnames = [
        "student_id",
        "age",
        "gender",
        "parental_education",
        "family_income",
        "study_time_hours_per_week",
        "absences",
        "extracurricular",
        "internet_access",
        "health",
        "alcohol_weekend",
        "alcohol_weekday",
        "free_time",
        "failures",
        "past_grade_avg",
        "final_score",
        "final_result",
    ]

    with open(args.out, "w", newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for i in range(1, args.n + 1):
            writer.writerow(generate_record(i, rng))

    print(f"Wrote {args.n} records to {args.out}")

if __name__ == "__main__":
    main()
