import re


def extract_resume_features(text):

    features = {}

    text_lower = text.lower()

    # ---------- Experience ----------

    experience = 0

    exp_pattern = re.search(
        r'(\d+)\+?\s*(year|years)',
        text_lower
    )

    if exp_pattern:
        experience = int(exp_pattern.group(1))

    # ---------- Projects ----------

    project_keywords = [
        "project",
        "projects"
    ]

    project_count = 0

    for word in project_keywords:

        project_count += text_lower.count(word)

    # ---------- CGPA ----------

    cgpa = 8.0

    cgpa_match = re.search(
        r'cgpa[:\s]*([0-9]+\.[0-9]+)',
        text_lower
    )

    if cgpa_match:
        cgpa = float(cgpa_match.group(1))

    # ---------- Certifications ----------

    certification_count = (
        text_lower.count("certificate")
        +
        text_lower.count("certification")
    )

    # ---------- Internships ----------

    internship_count = (
        text_lower.count("internship")
    )

    features["experience"] = experience

    features["projects"] = project_count

    features["cgpa"] = cgpa

    features["certifications"] = certification_count

    features["internships"] = internship_count

    return features