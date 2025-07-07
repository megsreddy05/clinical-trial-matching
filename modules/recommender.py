# modules/recommender.py
"""
Very simple ranking: +2 pts if the trial’s main condition matches one of the
patient’s conditions, +1 pt if they live in the same city.
You can extend this later with distance, phase, keywords, etc.
"""

def score_match(patient, trial):
    score = 0

    # condition overlap
    if trial["condition"].lower() in patient["conditions"].lower():
        score += 2

    # geographic proximity (exact city match)
    if patient["location"].lower() == trial["location"].lower():
        score += 1

    return score
