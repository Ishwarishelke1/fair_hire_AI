QUESTION_BANK = {

    "python": [
        "Explain Python decorators.",
        "What is the difference between List and Tuple?",
        "Explain generators in Python."
    ],

    "react": [
        "What is Virtual DOM?",
        "Difference between useState and useEffect?",
        "Explain React component lifecycle."
    ],

    "machine learning": [
        "Explain bias-variance tradeoff.",
        "Difference between supervised and unsupervised learning.",
        "Explain Random Forest."
    ],

    "sql": [
        "Difference between DELETE and TRUNCATE.",
        "Explain normalization.",
        "Write a JOIN query."
    ],

    "java": [
        "Explain JVM.",
        "Difference between Interface and Abstract Class.",
        "What is Multithreading?"
    ]
}


def generate_questions(skills):

    questions = []

    for skill in skills:

        skill = skill.lower()

        if skill in QUESTION_BANK:

            for question in QUESTION_BANK[skill]:

                questions.append({

                    "question": question,

                    "difficulty": "Medium"

                })

    return questions