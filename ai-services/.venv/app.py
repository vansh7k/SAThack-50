from flask import Flask, request, jsonify
import spacy
import PyPDF2
from io import BytesIO

ROLE_SKILLS = {
    "web_developer": ["HTML", "CSS", "JavaScript", "React", "Node.js", "MongoDB"],
    "data_analyst": ["Python", "SQL", "Excel", "Power BI", "Machine Learning"]
}
COURSES = {
    "React": "https://www.udemy.com/course/react-redux/",
    "MongoDB": "https://www.coursera.org/learn/mongodb-database",
    "Node.js": "https://www.udemy.com/course/nodejs-express-mongodb-bootcamp/",
    # Add more links as needed
}

nlp = spacy.load("en_core_web_sm")
app = Flask(__name__)

def extract_text(pdf_bytes):
    reader = PyPDF2.PdfReader(BytesIO(pdf_bytes))
    full_text = ""
    for page in reader.pages:
        full_text += page.extract_text() or ""
    return full_text

def detect_skills(text, role):
    doc = nlp(text)
    tokens = set([token.text for token in doc if token.is_alpha or token.is_title])
    target_skills = ROLE_SKILLS.get(role, [])
    found = [skill for skill in target_skills if skill in tokens]
    missing = [skill for skill in target_skills if skill not in found]
    suggestions = {skill: COURSES.get(skill, "") for skill in missing}
    return found, missing, suggestions

@app.route("/analyze", methods=["POST"])
def analyze():
    file = request.files['file']
    role = request.form['role']
    text = extract_text(file.read())
    found, missing, suggestions = detect_skills(text, role)
    return jsonify({
        "found_skills": found,
        "missing_skills": missing,
        "suggestions": suggestions
    })

if __name__ == "__main__":
    app.run(port=5001)
