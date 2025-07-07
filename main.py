# main.py
import pandas as pd
from modules.parser import parse_criteria
from modules.matcher import is_eligible
from modules.recommender import score_match

trials = pd.read_csv("data/trials.csv")
patients = pd.read_csv("data/patients.csv")

for _, p in patients.iterrows():
    print(f"\nMatching for Patient {p['patient_id']} with conditions: {p['conditions']}")
    matches = []

    for _, t in trials.iterrows():
        inc = parse_criteria(t["inclusion_criteria"])
        exc = parse_criteria(t["exclusion_criteria"])

        if is_eligible(p, inc, exc):
            score = score_match(p, t)
            matches.append((t["trial_id"], t["condition"], score))

    matches.sort(key=lambda x: x[2], reverse=True)
    for m in matches:
        print(f"  Trial: {m[0]}, Condition: {m[1]}, Score: {m[2]}")
