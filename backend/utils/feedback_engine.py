KNOWN_SKILLS = [
    "python",
    "java",
    "react",
    "mongodb",
    "mysql",
    "docker",
    "aws",
    "git",
    "flask",
    "node.js",
    "machine learning",
    "sql",
    "rest api"
]

def generate_feedback(candidate_skills, job_description):

    jd = job_description.lower()

    print("\n==========================")
    print("JOB DESCRIPTION:")
    print(jd)

    required_skills = []

    for skill in KNOWN_SKILLS:
        if skill in jd:
            required_skills.append(skill)

    print("Required Skills:", required_skills)

    candidate_lower = [
        skill.lower().strip()
        for skill in candidate_skills
    ]

    print("Candidate Skills:", candidate_lower)

    missing_skills = []

    for skill in required_skills:
        if skill not in candidate_lower:
            missing_skills.append(skill)

    print("Missing Skills:", missing_skills)
    print("==========================\n")

    feedback = []

    if len(missing_skills) == 0:
        feedback.append("Excellent match with job requirements.")
    else:
        feedback.append("Learn the missing skills to improve your profile.")

    if len(candidate_skills) < 5:
        feedback.append("Add more technical skills to your resume.")

    feedback.append("Include measurable project achievements.")
    feedback.append("Add certifications if available.")

    return {
        "missing_skills": missing_skills,
        "feedback": feedback
    }