import re

def extract_entities(text):

    entities = {
        "name": "",
        "emails": [],
        "phones": [],
        "education": [],
        "experience": []
    }

    # ---------------- Email ----------------

    email_pattern = r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}"

    entities["emails"] = re.findall(email_pattern, text)

    # ---------------- Phone ----------------

    phone_pattern = r"\+?\d[\d\s\-]{8,15}"

    entities["phones"] = re.findall(phone_pattern, text)

    # ---------------- Name ----------------

    lines = [line.strip() for line in text.split("\n") if line.strip()]

    if len(lines) > 0:
        entities["name"] = lines[0]

    # ---------------- Education ----------------

    education_keywords = [
        "University",
        "College",
        "Institute",
        "School",
        "SPPU",
        "Savitribai"
    ]

    for line in lines:

        for keyword in education_keywords:

            if keyword.lower() in line.lower():

                if line not in entities["education"]:
                    entities["education"].append(line)

    # ---------------- Experience ----------------

    company_keywords = [
        "Intern",
        "Foundation",
        "NITS",
        "Infosys",
        "TCS",
        "Capgemini",
        "Cognizant",
        "Google",
        "Microsoft",
        "Amazon",
        "Wipro"
    ]

    for line in lines:

        for keyword in company_keywords:

            if keyword.lower() in line.lower():

                if line not in entities["experience"]:
                    entities["experience"].append(line)

    return entities