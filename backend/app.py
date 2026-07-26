from flask import Flask, request, jsonify
from flask_cors import CORS
from utils.nlp_processor import preprocess_text, extract_skills
from utils.semantic_matcher import calculate_similarity
from utils.entity_extractor import extract_entities
from utils.bias_detector import anonymize_resume
from utils.explanation_engine import generate_explanation
from db import candidates

import os
from utils.interview_generator import generate_questions
from utils.resume_parser import extract_text_from_pdf
from utils.feedback_engine import generate_feedback
from utils.ml_predictor import predict_score
from utils.feature_extractor import extract_resume_features
from utils.recommendation_engine import recommend_candidate

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = "uploads"

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)


@app.route("/")
def home():
    return {"message": "Backend Running"}


@app.route("/upload", methods=["POST"])
def upload_resume():

    if "resume" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files["resume"]
    job_description = request.form.get("job_description", "")

    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(file_path)

    # ---------------- Resume Parsing ----------------

    extracted_text = extract_text_from_pdf(file_path)

    entities = extract_entities(extracted_text)
    print("\n========== Extracted Entities ==========")
    print(entities)
    print("========================================\n")
    anonymous_text, removed_items, fairness_score = anonymize_resume(
        extracted_text,
        entities
    )

    tokens = preprocess_text(extracted_text)

    skills = extract_skills(tokens)

    # ---------------- Feature Extraction ----------------

    features = extract_resume_features(extracted_text)

    questions = generate_questions(skills)

    feedback_result = generate_feedback(
        skills,
        job_description
    )
    print("Feedback Result:", feedback_result)
    
    # ---------------- Semantic Matching ----------------

    match_score = calculate_similarity(
        anonymous_text,
        job_description
    )

    # ---------------- ML Features ----------------

    skill_count = len(skills)

    experience_years = features.get("experience", 0)

    project_count = features.get("projects", 0)

    education_score = features.get("cgpa", 0)

    # ---------------- ML Prediction ----------------

    final_score = predict_score(
        match_score,
        skill_count,
        experience_years,
        project_count,
        education_score
    )

    # Convert NumPy values into Python values
    match_score = float(match_score)
    final_score = float(final_score)
    fairness_score = float(fairness_score)

    # ---------------- Recommendation ----------------

    recommendation = recommend_candidate(
        skills,
        final_score
    )

    # ---------------- MongoDB ----------------

    candidate_data = {

        "name": entities.get("name", ""),

        "skills": skills,

        "match_score": match_score,

        "final_score": final_score,

        "emails": entities.get("emails", []),

        "organizations": entities.get("organizations", [])

    }

    candidates.insert_one(candidate_data)

    # ---------------- Explainable AI ----------------

    explanations = generate_explanation(
        match_score,
        skills
    )

    # ---------------- Response ----------------

    return jsonify({

        "filename": file.filename,

        "resume_text": extracted_text,

        "skills": skills,

        "match_score": match_score,

        "resume_features": features,

        "final_score": final_score,

        "recommended_roles":
        recommendation["recommended_roles"],

        "hiring_decision":
        recommendation["decision"],

        "recommendation_reasons":
        recommendation["reasons"],

        "interview_questions": questions,

        "missing_skills":
        feedback_result["missing_skills"],

        "resume_feedback":
        feedback_result["feedback"],

        "entities": entities,

        "anonymous_resume": anonymous_text,

        "removed_items": removed_items,

        "fairness_score": fairness_score,

        "explanations": explanations

    })


@app.route("/dashboard")
def dashboard():

    data = list(
        candidates.find(
            {},
            {"_id": 0}
        )
    )

    return jsonify(data)


if __name__ == "__main__":
    app.run(debug=True)