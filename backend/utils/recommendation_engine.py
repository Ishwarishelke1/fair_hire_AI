def recommend_candidate(
    skills,
    final_score
):

    recommendations = []

    reasons = []

    skill_set = [
        s.lower()
        for s in skills
    ]

    if (
        "machine learning" in skill_set
        or
        "python" in skill_set
    ):

        recommendations.append(
            "AI Engineer"
        )

        recommendations.append(
            "Data Scientist"
        )

        reasons.append(
            "Strong AI programming skills."
        )

    if (
        "react" in skill_set
        or
        "node.js" in skill_set
    ):

        recommendations.append(
            "Full Stack Developer"
        )

        reasons.append(
            "Modern web development skills."
        )

    if "java" in skill_set:

        recommendations.append(
            "Backend Developer"
        )

        reasons.append(
            "Java backend development detected."
        )

    if final_score >= 80:

        decision = "Shortlist"

    elif final_score >= 70:

        decision = "Hold"

    else:

        decision = "Reject"

    return {

        "recommended_roles":
        list(set(recommendations)),

        "decision":
        decision,

        "reasons":
        reasons

    }