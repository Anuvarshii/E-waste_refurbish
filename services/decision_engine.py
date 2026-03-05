def generate_decision(physical_score, refurbish_value, damage_score):

    adjusted_damage = 10 - damage_score

    final_score = (
        0.4 * refurbish_value +
        0.2 * physical_score +
        0.4 * adjusted_damage
    )

    # 🔴 Strong damage override
    if damage_score >= 5:
        recommendation = "RECYCLE"
        risk = "High"

    elif final_score >= 6:
        recommendation = "REFURBISH"
        risk = "Low"

    elif final_score >= 4.5:
        recommendation = "MANUAL REVIEW"
        risk = "Medium"

    else:
        recommendation = "RECYCLE"
        risk = "High"

    return recommendation, risk, round(final_score, 2)