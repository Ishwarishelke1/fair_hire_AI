import re


def extract_required_skills(job_description):

    job_description = job_description.lower()

    known_skills = [
        "python",
        "java",
        "javascript",
        "react",
        "node",
        "node.js",
        "mongodb",
        "sql",
        "mysql",
        "html",
        "css",
        "machine learning",
        "data science",
        "nlp",
        "git",
        "flask",
        "django",
        "spring boot",
        "c++",
        "c#",
        "aws",
        "docker",
        "kubernetes",
        "excel",
        "power bi",
        "tensorflow",
        "pytorch"
    ]

    required_skills = []

    for skill in known_skills:

        if skill in job_description:

            required_skills.append(skill)

    return list(set(required_skills))


def generate_feedback(candidate_skills, job_description):

    candidate_skills = [
        str(skill).lower().strip()
        for skill in candidate_skills
    ]

    required_skills = extract_required_skills(
        job_description
    )

    missing_skills = [
        skill
        for skill in required_skills
        if skill not in candidate_skills
    ]

    feedback = []

    if missing_skills:

        feedback.append(
            "Consider improving the following skills: "
            + ", ".join(missing_skills)
        )

    else:

        feedback.append(
            "Excellent match with job requirements."
        )

    feedback.append(
        "Include measurable project achievements."
    )

    feedback.append(
        "Add certifications if available."
    )

    return {
        "missing_skills": missing_skills,
        "feedback": feedback
    }