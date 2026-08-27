from flask import Flask, request, jsonify
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash

from utils.nlp_processor import preprocess_text, extract_skills
from utils.semantic_matcher import calculate_similarity
from utils.entity_extractor import extract_entities
from utils.bias_detector import anonymize_resume
from utils.explanation_engine import generate_explanation
from db import candidates, users

import os
from utils.interview_generator import generate_questions
from utils.resume_parser import extract_text_from_pdf
from utils.feedback_engine import generate_feedback
from utils.ml_predictor import predict_score
from utils.feature_extractor import extract_resume_features
from utils.recommendation_engine import recommend_candidate
app = Flask(__name__)
CORS(
    app,
    resources={
        r"/*": {
            "origins": [
                "http://localhost:3000",
                "http://127.0.0.1:3000"
            ]
        }
    }
)
UPLOAD_FOLDER = "uploads"

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route("/signup", methods=["POST"])
def signup():

    data = request.get_json()

    if not data:
        return jsonify({
            "error": "No data received"
        }), 400

    name = data.get("name", "").strip()
    email = data.get("email", "").strip().lower()
    password = data.get("password", "")

    if not name or not email or not password:
        return jsonify({
            "error": "Name, email and password are required"
        }), 400

    existing_user = users.find_one({
        "email": email
    })

    if existing_user:
        return jsonify({
            "error": "Email already registered"
        }), 409

    hashed_password = generate_password_hash(password)

    user = {
        "name": name,
        "email": email,
        "password": hashed_password
    }

    users.insert_one(user)

    return jsonify({
        "message": "Account created successfully"
    }), 201

@app.route("/login", methods=["POST"])
def login():

    data = request.get_json()

    if not data:
        return jsonify({
            "error": "No data received"
        }), 400

    email = data.get("email", "").strip().lower()
    password = data.get("password", "")

    user = users.find_one({
        "email": email
    })

    if not user:
        return jsonify({
            "error": "Invalid email or password"
        }), 401

    if not check_password_hash(
        user["password"],
        password
    ):
        return jsonify({
            "error": "Invalid email or password"
        }), 401

    return jsonify({
        "success": True,
        "message": "Login successful",
        "user": {
            "name": user["name"],
            "email": user["email"]
        }
    }), 200

@app.route("/")
def home():
    return {"message": "Backend Running"}


@app.route("/upload", methods=["POST"])
def upload_resume():

    if "resume" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files["resume"]
    job_description = request.form.get("job_description", "").strip()

    if file.filename == "":
        return jsonify({"error": "No resume selected"}), 400

    try:

        # =====================================================
        # 1. SAVE RESUME
        # =====================================================

        file_path = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(file_path)

        # =====================================================
        # 2. EXTRACT RESUME TEXT
        # =====================================================

        extracted_text = extract_text_from_pdf(file_path)

        if not extracted_text:
            return jsonify({
                "error": "Could not extract text from resume"
            }), 400

        # =====================================================
        # 3. ENTITY EXTRACTION
        # =====================================================

        entities = extract_entities(extracted_text)

        print("\n========== Extracted Entities ==========")
        print(entities)
        print("========================================\n")

        # =====================================================
        # 4. ANONYMIZE RESUME
        # =====================================================

        anonymous_text, removed_items, fairness_score = anonymize_resume(
            extracted_text,
            entities
        )

        # =====================================================
        # 5. EXTRACT CANDIDATE SKILLS
        # =====================================================

        tokens = preprocess_text(extracted_text)

        skills = extract_skills(tokens)

        # Normalize skills
        candidate_skills = [
            str(skill).strip().lower()
            for skill in skills
            if skill
        ]

        # Remove duplicates
        candidate_skills = list(dict.fromkeys(candidate_skills))

        print("Candidate Skills:", candidate_skills)

        # =====================================================
        # 6. EXTRACT REQUIRED SKILLS FROM JOB DESCRIPTION
        # =====================================================

        job_tokens = preprocess_text(job_description)

        required_skills = extract_skills(job_tokens)

        required_skills = [
            str(skill).strip().lower()
            for skill in required_skills
            if skill
        ]

        required_skills = list(dict.fromkeys(required_skills))

        print("Required Skills:", required_skills)

        # =====================================================
        # 7. CALCULATE MISSING SKILLS
        # =====================================================

        missing_skills = [
            skill
            for skill in required_skills
            if skill not in candidate_skills
        ]

        print("Missing Skills:", missing_skills)

        # =====================================================
        # 8. RESUME FEATURES
        # =====================================================

        features = extract_resume_features(extracted_text)

        print("Resume Features:", features)

        # =====================================================
        # 9. RESUME FEEDBACK
        # =====================================================

        feedback_result = generate_feedback(
            candidate_skills,
            job_description
        )

        print("Feedback Result:", feedback_result)

        # Use our calculated missing skills
        # instead of depending completely on feedback_engine
        resume_feedback = feedback_result.get(
            "feedback",
            []
        )

        # If feedback engine returns no suggestions,
        # provide useful suggestions.
        if not resume_feedback:

            resume_feedback = []

            if missing_skills:
                resume_feedback.append(
                    "Consider adding these missing skills: "
                    + ", ".join(missing_skills)
                )

            resume_feedback.append(
                "Include measurable achievements in your projects."
            )

            resume_feedback.append(
                "Add relevant certifications if available."
            )

        # =====================================================
        # 10. INTERVIEW QUESTIONS
        # =====================================================

        questions = generate_questions(candidate_skills)

        # =====================================================
        # 11. SEMANTIC MATCHING
        # =====================================================

        match_score = calculate_similarity(
            anonymous_text,
            job_description
        )

        # =====================================================
        # 12. ML FEATURES
        # =====================================================

        skill_count = len(candidate_skills)

        experience_years = features.get(
            "experience",
            0
        )

        project_count = features.get(
            "projects",
            0
        )

        education_score = features.get(
            "cgpa",
            0
        )

        # =====================================================
        # 13. FINAL SCORE
        # =====================================================

        final_score = predict_score(
            match_score,
            skill_count,
            experience_years,
            project_count,
            education_score
        )

        match_score = float(match_score)
        final_score = float(final_score)
        fairness_score = float(fairness_score)

        # =====================================================
        # 14. RECOMMENDATION
        # =====================================================

        recommendation = recommend_candidate(
            candidate_skills,
            final_score
        )

        # =====================================================
        # 15. EXPLAINABLE AI
        # =====================================================

        explanations = generate_explanation(
            match_score,
            candidate_skills
        )

        # =====================================================
        # 16. CANDIDATE DATA
        # =====================================================

        candidate_data = {

            "name": entities.get(
                "name",
                ""
            ),

            "skills": candidate_skills,

            "required_skills": required_skills,

            "missing_skills": missing_skills,

            "match_score": match_score,

            "final_score": final_score,

            "emails": entities.get(
                "emails",
                []
            ),

            "phones": entities.get(
                "phones",
                []
            ),

            "locations": entities.get(
                "locations",
                []
            ),

            "organizations": entities.get(
                "organizations",
                []
            ),

            # Job description
            "job_description": job_description,

            # Resume analysis
            "resume_features": features,

            "resume_feedback": resume_feedback,

            # Fairness
            "fairness_score": fairness_score,

            "removed_items": removed_items,

            "anonymous_resume": anonymous_text,

            # AI results
            "recommended_roles": recommendation.get(
                "recommended_roles",
                []
            ),

            "hiring_decision": recommendation.get(
                "decision",
                ""
            ),

            "recommendation_reasons": recommendation.get(
                "reasons",
                []
            ),

            "explanations": explanations,

            # Interview
            "interview_questions": questions
        }

        # =====================================================
        # 17. DUPLICATE CANDIDATE UPDATE
        # =====================================================

        existing_candidate = candidates.find_one({

            "name": candidate_data["name"],

            "emails": candidate_data["emails"]

        })

        if existing_candidate:

            candidates.update_one(

                {
                    "name": candidate_data["name"],
                    "emails": candidate_data["emails"]
                },

                {
                    "$set": candidate_data
                }

            )

            print("Existing candidate updated.")

        else:

            candidates.insert_one(
                candidate_data
            )

            print("New candidate inserted.")

        # =====================================================
        # 18. RETURN RESPONSE TO REACT
        # =====================================================

        return jsonify({

            "filename": file.filename,

            "resume_text": extracted_text,

            "skills": candidate_skills,

            "required_skills": required_skills,

            "missing_skills": missing_skills,

            "match_score": match_score,

            "final_score": final_score,

            "resume_features": features,

            "resume_feedback": resume_feedback,

            "recommended_roles":
                recommendation.get(
                    "recommended_roles",
                    []
                ),

            "hiring_decision":
                recommendation.get(
                    "decision",
                    ""
                ),

            "recommendation_reasons":
                recommendation.get(
                    "reasons",
                    []
                ),

            "interview_questions": questions,

            "entities": entities,

            "anonymous_resume": anonymous_text,

            "removed_items": removed_items,

            "fairness_score": fairness_score,

            "explanations": explanations

        })

    except Exception as e:

        print("\n========== UPLOAD ERROR ==========")
        print(str(e))
        print("==================================\n")

        return jsonify({
            "error": str(e)
        }), 500

@app.route("/dashboard")
def dashboard():

    data = list(
        candidates.find(
            {},
            {"_id": 0}
        )
    )

    return jsonify(data)
@app.route("/resume-analysis", methods=["GET"])
def resume_analysis():

    candidate = candidates.find_one(
        {},
        {"_id": 0},
        sort=[
            ("_id", -1)
        ]
    )

    if not candidate:

        return jsonify({
            "error": "No resume analysis found"
        }), 404

    return jsonify({

        "name": candidate.get(
            "name",
            ""
        ),

        "skills": candidate.get(
            "skills",
            []
        ),

        "required_skills": candidate.get(
            "required_skills",
            []
        ),

        "missing_skills": candidate.get(
            "missing_skills",
            []
        ),

        "resume_feedback": candidate.get(
            "resume_feedback",
            []
        ),

        "match_score": candidate.get(
            "match_score",
            0
        ),

        "final_score": candidate.get(
            "final_score",
            0
        ),

        "resume_features": candidate.get(
            "resume_features",
            {}
        ),

        "recommended_roles": candidate.get(
            "recommended_roles",
            []
        ),

        "recommendation_reasons": candidate.get(
            "recommendation_reasons",
            []
        ),

        "hiring_decision": candidate.get(
            "hiring_decision",
            ""
        ),

        "explanations": candidate.get(
            "explanations",
            []
        ),

        "fairness_score": candidate.get(
            "fairness_score",
            0
        ),

        "removed_items": candidate.get(
            "removed_items",
            []
        ),

        "anonymous_resume": candidate.get(
            "anonymous_resume",
            ""
        )

    })

@app.route("/ranking")
def ranking():

    data = list(
        candidates.find({}, {"_id": 0})
        .sort("final_score", -1)
    )

    for i, candidate in enumerate(data):
        candidate["rank"] = i + 1

    return jsonify(data)

if __name__ == "__main__":
    app.run(debug=True)

