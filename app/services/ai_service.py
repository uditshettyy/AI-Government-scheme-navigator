def generate_ai_explaination(user, scheme):

    score = 0
    reasons = []

    # Occupation match (already filtered in SQL)
    score += 20
    reasons.append(f"As a {user.occupation}, you are directly eligible for this scheme.")

    # Income analysis
    income_gap = scheme["income_limit"] - user.income

    if income_gap > 200000:
        score += 20
        reasons.append("Your income is comfortably within the eligibility limit.")
    elif income_gap > 0:
        score += 15
        reasons.append("Your income meets the eligibility requirement.")
    else:
        score += 5
        reasons.append("Your income is very close to the eligibility threshold.")

    # Age factor (optional intelligence boost)
    if user.age < 35:
        score += 10
        reasons.append("Being in a younger age group may increase long-term benefits.")
    else:
        score += 5

    # Benefit attractiveness
    benefit_score = min((scheme["benefit_amount"] / 500000) * 20, 20)
    score += benefit_score

    if benefit_score > 15:
        reasons.append("This scheme provides significant financial support.")

    # Government priority weight
    priority_score = (scheme["priority_weight"] / 5) * 15
    score += priority_score

    score = round(score)

    # Improved explanation tone
    simple_explanation = (
        f"Based on your profile as a {user.age}-year-old {user.occupation} "
        f"from {user.state} with annual income ₹{user.income}, "
        f"the scheme '{scheme['name']}' is a strong match. "
        f"It offers {scheme['benefit']} under the {scheme['category']} category."
    )

    # Convert documents into list safely
    documents = [
        doc.strip() 
        for doc in scheme["required_documents"].split(",")
    ] if scheme["required_documents"] else []

    return {
        "simple_explanation": simple_explanation,
        "steps_to_apply": documents,
        "why_you_qualify": " ".join(reasons),
        "score": score
    }
