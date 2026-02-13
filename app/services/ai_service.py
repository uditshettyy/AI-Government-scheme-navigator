def generate_ai_explaination(user,scheme):
    score=0
    reasons=[]

    score+=4
    reasons.append("Your occupation matches this scheme.")
    income_gap=scheme["income_limit"] - user.income

    if income_gap > 200000:
        score+=3
        reasons.append("Your income is well within the eligiblity range.")

    elif income_gap > 0:
        score+=1
        reasons.append("Your income falls within the eligibility limit")
    benefit_weight=min(scheme["benefit_amount"]//100000,5)
    score+= benefit_weight

    if benefit_weight >= 3:
        reasons.append("This scheme offers a high financial benefit.")
    
    score+=scheme["priority_weight"]


    simple_explaination={
        f"The scheme '{scheme['name']}' offers {scheme['benefit']}."
        f"under the {scheme['category']} category."
    }

    return{
        "simple_explanation": simple_explaination,
        "steps_to_apply": scheme["required_documents"],
        "why_you_qualify": " ".join(reasons),
        "score": score
    }