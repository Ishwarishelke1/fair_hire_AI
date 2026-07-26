import joblib

model = joblib.load(
    "models/candidate_rank_model.pkl"
)

def predict_score(
    semantic_score,
    skill_count,
    experience_years,
    project_count,
    education_score
):

    prediction = model.predict([[
        semantic_score,
        skill_count,
        experience_years,
        project_count,
        education_score
    ]])

    return round(
        prediction[0],
        2
    )