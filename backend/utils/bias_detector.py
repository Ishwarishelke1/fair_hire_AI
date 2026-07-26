import re

GENDER_WORDS = [
    "male",
    "female",
    "mr",
    "mrs",
    "miss",
    "ms",
    "he",
    "she",
    "him",
    "her"
]

# These words should NEVER be anonymized even if spaCy
# incorrectly detects them as locations.

IGNORE_LOCATIONS = {
    "react",
    "react.js",
    "node",
    "node.js",
    "flask",
    "numpy",
    "pandas",
    "python",
    "java",
    "javascript",
    "mongodb",
    "mysql",
    "docker",
    "aws",
    "rest",
    "rest api",
    "github",
    "linkedin",
    "india",
    "smart india hackathon",
    "leetcode",
    "power bi",
    "scikit-learn"
}


def anonymize_resume(text, entities):

    anonymous_text = text

    removed_items = []

    # ---------------- Name ----------------

    if entities.get("name"):

        anonymous_text = anonymous_text.replace(
            entities["name"],
            "[NAME]"
        )

        removed_items.append("Candidate Name")

    # ---------------- Email ----------------

    for email in entities.get("emails", []):

        anonymous_text = anonymous_text.replace(
            email,
            "[EMAIL]"
        )

        removed_items.append("Email")

    # ---------------- Phone ----------------

    for phone in entities.get("phones", []):

        anonymous_text = anonymous_text.replace(
            phone,
            "[PHONE]"
        )

        removed_items.append("Phone")

    # ---------------- LinkedIn ----------------

    anonymous_text = re.sub(
        r"https?://(www\.)?linkedin\.com/[^\s]+",
        "[LINKEDIN]",
        anonymous_text,
        flags=re.IGNORECASE
    )

    # ---------------- GitHub ----------------

    anonymous_text = re.sub(
        r"https?://(www\.)?github\.com/[^\s]+",
        "[GITHUB]",
        anonymous_text,
        flags=re.IGNORECASE
    )

    # ---------------- Locations ----------------

    for location in entities.get("locations", []):

        location = location.strip()

        if len(location) < 3:
            continue

        if location.lower() in IGNORE_LOCATIONS:
            continue

        anonymous_text = re.sub(
            r"\b" + re.escape(location) + r"\b",
            "[LOCATION]",
            anonymous_text
        )

        removed_items.append("Location")

    # ---------------- Gender ----------------

    words = anonymous_text.split()

    cleaned_words = []

    for word in words:

        if word.lower().strip(".,") not in GENDER_WORDS:
            cleaned_words.append(word)

    anonymous_text = " ".join(cleaned_words)

    fairness_score = max(0, 100 - len(set(removed_items)) * 5)

    return anonymous_text, list(set(removed_items)), fairness_score