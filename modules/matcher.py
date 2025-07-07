# modules/matcher.py

def is_eligible(patient, inclusion_rules, exclusion_rules):
    """
    Return True if the patient satisfies ALL inclusion_rules and NONE of the exclusion_rules.
    Both rule lists are lower‑case strings such as:
        "age > 40"  |  "has diabetes"
    """
    age = int(patient["age"])
    # turn "diabetes, hypertension" → ["diabetes", "hypertension"]
    conditions = [c.strip() for c in patient["conditions"].lower().split(",")]

    # ---------- inclusion ----------
    for rule in inclusion_rules:
        if "age" in rule:
            if ">" in rule:
                threshold = int(rule.split(">")[1].strip())
                if not age > threshold:
                    return False
            elif "<" in rule:
                threshold = int(rule.split("<")[1].strip())
                if not age < threshold:
                    return False
        else:
            # need at least one keyword from the rule inside patient conditions
            if not any(word in conditions for word in rule.split()):
                return False

    # ---------- exclusion ----------
    for rule in exclusion_rules:
        if "age" in rule:
            if ">" in rule and age > int(rule.split(">")[1].strip()):
                return False
            if "<" in rule and age < int(rule.split("<")[1].strip()):
                return False
        else:
            if any(word in conditions for word in rule.split()):
                return False

    return True
