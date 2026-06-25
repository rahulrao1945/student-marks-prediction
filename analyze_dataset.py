#!/usr/bin/env python3
import csv
import argparse
import statistics
from collections import Counter

NUMERIC_FIELDS = [
    'age','family_income','study_time_hours_per_week','absences','health',
    'alcohol_weekend','alcohol_weekday','free_time','failures','past_grade_avg','final_score'
]

CAT_FIELDS = [
    'gender','parental_education','extracurricular','internet_access','final_result'
]


def safe_float(x):
    try:
        return float(x)
    except:
        return None


def summarize(infile, outfile=None, top_k=5):
    counts = 0
    numeric_vals = {f: [] for f in NUMERIC_FIELDS}
    cat_counts = {f: Counter() for f in CAT_FIELDS}

    with open(infile, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for r in reader:
            counts += 1
            for f in NUMERIC_FIELDS:
                v = safe_float(r.get(f, ''))
                if v is not None:
                    numeric_vals[f].append(v)
            for f in CAT_FIELDS:
                v = r.get(f, None)
                if v is not None:
                    cat_counts[f][v] += 1

    lines = []
    lines.append(f"Total records: {counts}")
    lines.append("")
    lines.append("Numeric fields:")
    for f, vals in numeric_vals.items():
        if not vals:
            lines.append(f"- {f}: no data")
            continue
        mean = statistics.mean(vals)
        med = statistics.median(vals)
        mn = min(vals)
        mx = max(vals)
        try:
            sd = statistics.stdev(vals)
        except:
            sd = 0.0
        lines.append(f"- {f}: count={len(vals)}, mean={mean:.3f}, median={med:.3f}, sd={sd:.3f}, min={mn}, max={mx}")
    lines.append("")
    lines.append("Categorical fields (top values):")
    for f, ctr in cat_counts.items():
        lines.append(f"- {f}:")
        for val, c in ctr.most_common(top_k):
            pct = (c / counts) * 100 if counts else 0
            lines.append(f"    {val}: {c} ({pct:.2f}%)")
    out_text = "\n".join(lines)
    if outfile:
        with open(outfile, 'w', encoding='utf-8') as of:
            of.write(out_text)
    print(out_text)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Analyze dataset and print summary statistics')
    parser.add_argument('--in', dest='infile', required=True, help='Input CSV file')
    parser.add_argument('--out', dest='outfile', default='analysis_summary.txt', help='Output summary file')
    args = parser.parse_args()
    summarize(args.infile, args.outfile)
