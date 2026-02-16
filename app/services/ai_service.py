def generate_ai_explaination(user, scheme):

    score = 0
    reasons = []

    score += 25
    reasons.append("Your occupation matches this scheme.")

    income_gap = scheme["income_limit"] - user.income

    if income_gap > 200000:
        score += 25
        reasons.append("Your income is well within the eligibility range.")
    elif income_gap > 0:
        score += 15
        reasons.append("Your income falls within the eligibility limit.")
    else:
        score += 5
        reasons.append("Your income is close to the eligibility limit.")

    benefit_score = min((scheme["benefit_amount"] / 1000000) * 25, 25)
    score += benefit_score

    if benefit_score > 15:
        reasons.append("This scheme offers a high financial benefit.")

    priority_score = (scheme["priority_weight"] / 5) * 25
    score += priority_score

    score = round(score)

    simple_explanation = (
        f"The scheme '{scheme['name']}' offers {scheme['benefit']} "
        f"under the {scheme['category']} category."
    )

    return {
        "simple_explanation": simple_explanation,
        "steps_to_apply": scheme["required_documents"],
        "why_you_qualify": " ".join(reasons),
        "score": score
    }