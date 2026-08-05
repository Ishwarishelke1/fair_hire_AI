# 🚀 FAIR-HIRE AI
### AI-Based Smart Resume Screening & Candidate Ranking System

FAIR-HIRE AI is an intelligent recruitment platform that automates resume screening using Artificial Intelligence and Machine Learning. The system analyzes resumes, compares them with job descriptions, extracts candidate information, generates interview questions, detects missing skills, ensures fairness through resume anonymization, and ranks candidates based on their suitability.

---

## 📌 Features

### 📄 Resume Upload
- Upload resumes in PDF format
- Automatic resume parsing
- Resume text extraction

### 🧠 AI Resume Screening
- NLP-based resume preprocessing
- Semantic similarity matching with Job Description
- Skill extraction
- Resume feature extraction

### 🤖 Candidate Ranking
- AI Match Score calculation
- Final ML-based Candidate Score
- Automatic hiring recommendation
- Leaderboard of ranked candidates

### 🎯 Recommendation Engine
- Recommended job roles
- Hiring decision
- Recommendation reasons

### 💬 AI Interview Question Generator
- Generates technical interview questions
- Difficulty-wise questions

### 📊 Resume Feedback
- Missing skill detection
- Resume improvement suggestions

### ⚖️ Fair Hiring
- Resume anonymization
- Personal information removal
- Fairness Score generation

### 👤 Candidate Information Extraction
- Name
- Email
- Phone Number
- Organizations
- Location

### 📈 Recruiter Dashboard
- Total Candidates
- Average Candidate Score
- Candidate Ranking Table
- Search Candidate by Skill
- Export Candidate Data to CSV

---

# 🏗️ System Architecture

```
                Resume PDF
                     │
                     ▼
              Resume Parser
                     │
                     ▼
           NLP Preprocessing
                     │
                     ▼
        Skill & Entity Extraction
                     │
                     ▼
       Semantic Matching (BERT)
                     │
                     ▼
          Feature Extraction
                     │
                     ▼
         ML Score Prediction
                     │
                     ▼
 Recommendation + Fairness Check
                     │
                     ▼
        MongoDB Database Storage
                     │
                     ▼
          Recruiter Dashboard
```

---

# 🛠 Tech Stack

## Frontend
- React.js
- JavaScript
- Tailwind CSS
- Axios
- React Toastify

## Backend
- Flask
- Python

## AI / Machine Learning
- Sentence Transformers
- Scikit-Learn
- SpaCy
- NLTK

## Database
- MongoDB

## Other Libraries
- Flask-CORS
- PyPDF2
- pdfplumber
- Pandas
- NumPy

---

# 📂 Project Structure

```
fair_hire_AI

│
├── backend
│   ├── app.py
│   ├── db.py
│   ├── uploads
│   ├── models
│   └── utils
│       ├── bias_detector.py
│       ├── entity_extractor.py
│       ├── explanation_engine.py
│       ├── feature_extractor.py
│       ├── feedback_engine.py
│       ├── interview_generator.py
│       ├── ml_predictor.py
│       ├── nlp_processor.py
│       ├── recommendation_engine.py
│       ├── resume_parser.py
│       └── semantic_matcher.py
│
├── frontend
│   ├── public
│   ├── src
│   │   ├── components
│   │   ├── App.js
│   │   └── index.js
│
└── README.md
```

---

# ⚙️ Installation

## Clone Repository

```bash
git clone https://github.com/Ishwarishelke1/fair_hire_AI.git

cd fair_hire_AI
```

---

## Backend Setup

```bash
cd backend

python -m venv venv
```

Activate virtual environment

Windows

```bash
venv\Scripts\activate
```

Linux/Mac

```bash
source venv/bin/activate
```

Install dependencies

```bash
pip install -r requirements.txt
```

Run Backend

```bash
python app.py
```

Backend runs on

```
http://127.0.0.1:5000
```

---

## Frontend Setup

```bash
cd frontend

npm install
```

Run React App

```bash
npm start
```

Frontend runs on

```
http://localhost:3000
```

---

# 📊 AI Workflow

1. Upload Resume
2. Extract Resume Text
3. Extract Skills
4. Extract Candidate Information
5. Remove Personal Information
6. Compare Resume with Job Description
7. Calculate Semantic Similarity
8. Predict Final Candidate Score
9. Recommend Job Roles
10. Generate Interview Questions
11. Generate Resume Feedback
12. Store Candidate Data in MongoDB
13. Display Candidate Ranking Dashboard

---

# 📸 Screenshots

Add screenshots of:

- Home Page
- Resume Upload
- AI Results
- Candidate Information
- Resume Feedback
- Recruiter Dashboard
- Candidate Ranking

---

# 🚀 Future Enhancements

- Multi Resume Upload
- Resume OCR
- LinkedIn Profile Analysis
- GitHub Repository Analysis
- AI Chatbot for Recruiters
- Email Notifications
- Authentication System
- Admin Panel
- Advanced Candidate Ranking
- Resume History
- PDF Report Generation

---

# 🎯 Project Highlights

✅ Resume Parsing

✅ AI Resume Screening

✅ Candidate Ranking

✅ Semantic Resume Matching

✅ Resume Anonymization

✅ Explainable AI

✅ Skill Gap Detection

✅ Interview Question Generator

✅ Recommendation Engine

✅ Recruiter Dashboard

✅ MongoDB Integration

---

# 👩‍💻 Author

**Ishwari Shelke**

Computer Engineering Student

GitHub:
https://github.com/Ishwarishelke1

LinkedIn:
(Add your LinkedIn URL)

---

# ⭐ If you like this project

Please give this repository a ⭐ on GitHub!
