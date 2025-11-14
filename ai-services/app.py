from flask import Flask, request, jsonify
from flask_cors import CORS
import io
from PyPDF2 import PdfReader
import spacy
import json

app = Flask(__name__)
CORS(app)

# Load spaCy model for NLP
try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    print("Downloading spaCy model...")
    import subprocess
    subprocess.run(["python", "-m", "spacy", "download", "en_core_web_sm"])
    nlp = spacy.load("en_core_web_sm")

# Define skill categories
SKILL_DATABASE = {
    "frontend": ["react", "vue", "angular", "html", "css", "javascript", "typescript", "tailwindcss", "bootstrap"],
    "backend": ["python", "node.js", "express", "django", "fastapi", "java", "spring", "golang", "rust"],
    "data": ["pandas", "numpy", "scikit-learn", "tensorflow", "pytorch", "sql", "spark", "tableau", "power bi"],
    "devops": ["docker", "kubernetes", "aws", "gcp", "azure", "jenkins", "gitlab", "terraform", "ansible"],
    "mobile": ["react native", "flutter", "swift", "kotlin", "xamarin"],
}

# Course recommendations with links
COURSE_RECOMMENDATIONS = {
    "react": {
        "skill": "React",
        "udemy": "https://www.udemy.com/course/react-the-complete-guide-incl-redux/",
        "unacademy": "https://unacademy.com/goal/react-js-beginners",
        "description": "Learn React from basics to advanced patterns",
        "difficulty": "Intermediate",
        "duration": "40 hours"
    },
    "vue": {
        "skill": "Vue.js",
        "udemy": "https://www.udemy.com/course/vue-js-2-the-complete-guide/",
        "unacademy": "https://unacademy.com/goal/vue-js",
        "description": "Complete Vue.js development course",
        "difficulty": "Intermediate",
        "duration": "30 hours"
    },
    "angular": {
        "skill": "Angular",
        "udemy": "https://www.udemy.com/course/the-complete-angular-course/",
        "unacademy": "https://unacademy.com/goal/angular-js",
        "description": "Angular framework masterclass",
        "difficulty": "Advanced",
        "duration": "45 hours"
    },
    "javascript": {
        "skill": "JavaScript",
        "udemy": "https://www.udemy.com/course/the-complete-javascript-course-2024-from-zero-to-expert/",
        "unacademy": "https://unacademy.com/goal/javascript-basics",
        "description": "JavaScript fundamentals to advanced concepts",
        "difficulty": "Beginner",
        "duration": "35 hours"
    },
    "typescript": {
        "skill": "TypeScript",
        "udemy": "https://www.udemy.com/course/typescript-the-complete-developer-guide/",
        "unacademy": "https://unacademy.com/goal/typescript",
        "description": "Master TypeScript for scalable applications",
        "difficulty": "Intermediate",
        "duration": "20 hours"
    },
    "python": {
        "skill": "Python",
        "udemy": "https://www.udemy.com/course/complete-python-bootcamp/",
        "unacademy": "https://unacademy.com/goal/python-basics",
        "description": "Python programming from basics to advanced",
        "difficulty": "Beginner",
        "duration": "25 hours"
    },
    "django": {
        "skill": "Django",
        "udemy": "https://www.udemy.com/course/python-and-django-full-stack-web-developer-bootcamp/",
        "unacademy": "https://unacademy.com/goal/django-web-framework",
        "description": "Build web applications with Django",
        "difficulty": "Intermediate",
        "duration": "30 hours"
    },
    "fastapi": {
        "skill": "FastAPI",
        "udemy": "https://www.udemy.com/course/fastapi-the-complete-course/",
        "unacademy": "https://unacademy.com/goal/fastapi",
        "description": "Modern API development with FastAPI",
        "difficulty": "Intermediate",
        "duration": "25 hours"
    },
    "express": {
        "skill": "Express.js",
        "udemy": "https://www.udemy.com/course/nodejs-the-complete-guide/",
        "unacademy": "https://unacademy.com/goal/nodejs-basics",
        "description": "Build backend with Node.js and Express",
        "difficulty": "Intermediate",
        "duration": "35 hours"
    },
    "node.js": {
        "skill": "Node.js",
        "udemy": "https://www.udemy.com/course/nodejs-the-complete-guide/",
        "unacademy": "https://unacademy.com/goal/nodejs-basics",
        "description": "JavaScript runtime for backend development",
        "difficulty": "Intermediate",
        "duration": "30 hours"
    },
    "docker": {
        "skill": "Docker",
        "udemy": "https://www.udemy.com/course/docker-and-kubernetes-the-complete-guide/",
        "unacademy": "https://unacademy.com/goal/docker-containers",
        "description": "Containerization with Docker",
        "difficulty": "Intermediate",
        "duration": "20 hours"
    },
    "kubernetes": {
        "skill": "Kubernetes",
        "udemy": "https://www.udemy.com/course/docker-and-kubernetes-the-complete-guide/",
        "unacademy": "https://unacademy.com/goal/kubernetes",
        "description": "Kubernetes orchestration and deployment",
        "difficulty": "Advanced",
        "duration": "25 hours"
    },
    "aws": {
        "skill": "AWS",
        "udemy": "https://www.udemy.com/course/aws-certified-solutions-architect-associate/",
        "unacademy": "https://unacademy.com/goal/aws-cloud",
        "description": "Amazon Web Services cloud platform",
        "difficulty": "Advanced",
        "duration": "40 hours"
    },
    "sql": {
        "skill": "SQL",
        "udemy": "https://www.udemy.com/course/the-complete-sql-bootcamp/",
        "unacademy": "https://unacademy.com/goal/sql-basics",
        "description": "SQL database querying and management",
        "difficulty": "Beginner",
        "duration": "15 hours"
    },
    "tensorflow": {
        "skill": "TensorFlow",
        "udemy": "https://www.udemy.com/course/tensorflow-2-deep-learning-bootcamp/",
        "unacademy": "https://unacademy.com/goal/tensorflow-machine-learning",
        "description": "Deep learning with TensorFlow",
        "difficulty": "Advanced",
        "duration": "45 hours"
    },
    "pandas": {
        "skill": "Pandas",
        "udemy": "https://www.udemy.com/course/data-analysis-with-pandas/",
        "unacademy": "https://unacademy.com/goal/pandas-data-analysis",
        "description": "Data manipulation with Pandas library",
        "difficulty": "Beginner",
        "duration": "15 hours"
    },
    "numpy": {
        "skill": "NumPy",
        "udemy": "https://www.udemy.com/course/numpy-python-tutorial/",
        "unacademy": "https://unacademy.com/goal/numpy-basics",
        "description": "Numerical computing with NumPy",
        "difficulty": "Beginner",
        "duration": "12 hours"
    },
    "scikit-learn": {
        "skill": "Scikit-learn",
        "udemy": "https://www.udemy.com/course/machine-learning-with-scikit-learn/",
        "unacademy": "https://unacademy.com/goal/scikit-learn-ml",
        "description": "Machine learning with Scikit-learn",
        "difficulty": "Intermediate",
        "duration": "25 hours"
    },
    "html": {
        "skill": "HTML",
        "udemy": "https://www.udemy.com/course/web-design-for-beginners-real-coding-in-html-and-css/",
        "unacademy": "https://unacademy.com/goal/html-basics",
        "description": "HTML fundamentals for web development",
        "difficulty": "Beginner",
        "duration": "10 hours"
    },
    "css": {
        "skill": "CSS",
        "udemy": "https://www.udemy.com/course/advanced-css-and-sass/",
        "unacademy": "https://unacademy.com/goal/css-basics",
        "description": "CSS styling and advanced techniques",
        "difficulty": "Beginner",
        "duration": "12 hours"
    },
    "java": {
        "skill": "Java",
        "udemy": "https://www.udemy.com/course/java-the-complete-java-developer-course/",
        "unacademy": "https://unacademy.com/goal/java-programming",
        "description": "Java programming fundamentals and OOP",
        "difficulty": "Beginner",
        "duration": "40 hours"
    },
    "spring": {
        "skill": "Spring Boot",
        "udemy": "https://www.udemy.com/course/spring-boot-microservices-and-restful-web-services/",
        "unacademy": "https://unacademy.com/goal/spring-boot-framework",
        "description": "Spring framework for Java applications",
        "difficulty": "Intermediate",
        "duration": "35 hours"
    },
    "golang": {
        "skill": "Go (Golang)",
        "udemy": "https://www.udemy.com/course/go-the-complete-developers-guide/",
        "unacademy": "https://unacademy.com/goal/golang-programming",
        "description": "Go programming language for backend",
        "difficulty": "Intermediate",
        "duration": "25 hours"
    },
    "rust": {
        "skill": "Rust",
        "udemy": "https://www.udemy.com/course/rust-programming-language/",
        "unacademy": "https://unacademy.com/goal/rust-programming",
        "description": "Systems programming with Rust",
        "difficulty": "Advanced",
        "duration": "30 hours"
    },
}

def extract_text_from_pdf(file_buffer):
    """Extract text from PDF file"""
    try:
        pdf_file = io.BytesIO(file_buffer)
        reader = PdfReader(pdf_file)
        text = ""
        for page in reader.pages:
            extracted = page.extract_text()
            if extracted:
                text += extracted
        if not text.strip():
            print("Warning: No text extracted from PDF")
        return text.lower()
    except Exception as e:
        print(f"Error extracting PDF: {e}")
        import traceback
        traceback.print_exc()
        return ""

def extract_skills(text):
    """Extract skills from resume text using spaCy and keyword matching"""
    found_skills = set()
    
    # Convert text to lowercase for matching
    text_lower = text.lower()
    
    # Search for all skills in the skill database
    for category, skills in SKILL_DATABASE.items():
        for skill in skills:
            if skill in text_lower:
                found_skills.add(skill)
    
    return list(found_skills)

def get_missing_skills(found_skills, role):
    """Determine which skills are missing for the given role"""
    role_lower = role.lower()
    
    # Map role to skill category
    role_to_category = {
        "frontend": "frontend",
        "backend": "backend",
        "data": "data",
        "devops": "devops",
        "mobile": "mobile",
        "full stack": "frontend",  # Frontend skills as primary
    }
    
    target_category = None
    for key, category in role_to_category.items():
        if key in role_lower:
            target_category = category
            break
    
    if not target_category:
        target_category = "backend"  # Default category
    
    required_skills = set(SKILL_DATABASE.get(target_category, []))
    found_set = set(found_skills)
    missing_skills = list(required_skills - found_set)
    
    return missing_skills

def generate_suggestions(found_skills, missing_skills, role):
    """Generate personalized suggestions for the candidate"""
    suggestions = []
    role_lower = role.lower()
    
    # Analyze current skills
    if not found_skills:
        suggestions.append(f"⚠️ No technical skills detected. Ensure your resume includes specific technologies and tools you've used.")
    else:
        suggestions.append(f"✓ Great! You have {len(found_skills)} relevant technical skills mentioned.")
    
    # Priority recommendations based on role
    if "frontend" in role_lower:
        suggestions.append("📌 Frontend Priority: Master React, Vue, or Angular. Build 3-5 projects showcasing UI/UX skills.")
        if "typescript" not in [s.lower() for s in found_skills]:
            suggestions.append("🔧 Add TypeScript to your skill set for better code quality and job prospects.")
    
    elif "backend" in role_lower:
        suggestions.append("📌 Backend Priority: Deepen expertise in Python/Node.js and master Django/Express framework.")
        if "docker" not in [s.lower() for s in found_skills]:
            suggestions.append("🔧 Learn Docker for containerization - highly valued in modern backend roles.")
    
    elif "data" in role_lower:
        suggestions.append("📌 Data Science Priority: Master pandas, NumPy, and scikit-learn for data manipulation.")
        if "sql" not in [s.lower() for s in found_skills]:
            suggestions.append("🔧 SQL is essential for data roles. Focus on complex queries and database optimization.")
    
    elif "devops" in role_lower:
        suggestions.append("📌 DevOps Priority: Master Docker, Kubernetes, and cloud platforms (AWS/GCP/Azure).")
        suggestions.append("🔧 Learn Infrastructure as Code (Terraform) for better automation.")
    
    # Portfolio advice
    suggestions.append("💼 Build 3-5 real-world projects on GitHub showcasing your skills with detailed documentation.")
    suggestions.append("📄 Include quantifiable achievements (\"Reduced load time by 40%\", etc.) in your resume.")
    suggestions.append("🎓 Pursue relevant certifications to boost credibility (AWS, Google Cloud, Azure, etc.).")
    
    if missing_skills:
        top_3_skills = ", ".join(missing_skills[:3])
        suggestions.append(f"🚀 Learning Path: Focus on {top_3_skills} first based on job market demand.")
    
    return suggestions

def get_course_recommendations(missing_skills):
    """Get course recommendations for missing skills"""
    recommendations = []
    skill_mapping = {
        "react": "react",
        "vue": "vue",
        "angular": "angular",
        "javascript": "javascript",
        "js": "javascript",
        "typescript": "typescript",
        "ts": "typescript",
        "python": "python",
        "py": "python",
        "django": "django",
        "fastapi": "fastapi",
        "express": "express",
        "node.js": "node.js",
        "nodejs": "node.js",
        "docker": "docker",
        "kubernetes": "kubernetes",
        "k8s": "kubernetes",
        "aws": "aws",
        "sql": "sql",
        "tensorflow": "tensorflow",
        "pandas": "pandas",
        "numpy": "numpy",
        "scikit-learn": "scikit-learn",
        "sklearn": "scikit-learn",
        "html": "html",
        "css": "css",
        "java": "java",
        "spring": "spring",
        "golang": "golang",
        "go": "golang",
        "rust": "rust",
    }
    
    for skill in missing_skills:
        skill_lower = skill.lower().strip()
        # Try direct mapping first
        if skill_lower in COURSE_RECOMMENDATIONS:
            recommendations.append(COURSE_RECOMMENDATIONS[skill_lower])
        # Try mapped skill
        elif skill_lower in skill_mapping:
            mapped_skill = skill_mapping[skill_lower]
            if mapped_skill in COURSE_RECOMMENDATIONS:
                recommendations.append(COURSE_RECOMMENDATIONS[mapped_skill])
    
    # Return top 8 recommendations
    return recommendations[:8]

def generate_learning_roadmap(role, found_skills, missing_skills):
    """Generate a personalized learning roadmap"""
    role_lower = role.lower()
    
    roadmap = {
        "role": role,
        "phase1": {
            "title": "Foundation Phase (2-4 weeks)",
            "description": "Build core fundamentals",
            "skills": []
        },
        "phase2": {
            "title": "Intermediate Phase (4-8 weeks)",
            "description": "Develop practical applications",
            "skills": []
        },
        "phase3": {
            "title": "Advanced Phase (8-12 weeks)",
            "description": "Mastery and specialization",
            "skills": []
        }
    }
    
    # Define roadmaps based on role
    role_roadmaps = {
        "frontend": {
            "phase1": ["html", "css", "javascript"],
            "phase2": ["react", "typescript"],
            "phase3": ["tailwindcss", "testing"]
        },
        "backend": {
            "phase1": ["python", "sql"],
            "phase2": ["express", "django", "fastapi"],
            "phase3": ["docker", "deployment"]
        },
        "data": {
            "phase1": ["python", "sql"],
            "phase2": ["pandas", "numpy", "scikit-learn"],
            "phase3": ["tensorflow", "pytorch"]
        },
        "devops": {
            "phase1": ["docker", "git"],
            "phase2": ["kubernetes", "aws"],
            "phase3": ["terraform", "jenkins"]
        },
        "full stack": {
            "phase1": ["html", "css", "javascript", "python", "sql"],
            "phase2": ["react", "django", "express"],
            "phase3": ["docker", "aws", "deployment"]
        }
    }
    
    # Get the roadmap for the role
    for key, roadmap_path in role_roadmaps.items():
        if key in role_lower:
            roadmap["phase1"]["skills"] = roadmap_path.get("phase1", [])
            roadmap["phase2"]["skills"] = roadmap_path.get("phase2", [])
            roadmap["phase3"]["skills"] = roadmap_path.get("phase3", [])
            break
    
    # Prioritize missing skills in the roadmap
    for phase in ["phase1", "phase2", "phase3"]:
        phase_skills = roadmap[phase]["skills"]
        roadmap[phase]["skills_to_learn"] = [s for s in phase_skills if s in missing_skills]
        roadmap[phase]["status"] = "PRIORITY" if roadmap[phase]["skills_to_learn"] else "OPTIONAL"
    
    return roadmap

@app.route("/analyze", methods=["POST"])
def analyze_resume():
    """Analyze resume and extract skills"""
    try:
        # Get file from request
        if 'resume' not in request.files:
            print("No resume file in request")
            return jsonify({"error": "No file part"}), 400
        
        file = request.files['resume']
        role = request.form.get('role', 'backend') or 'backend'
        
        print(f"\n=== Analyzing Resume ===")
        print(f"Filename: {file.filename}")
        print(f"Role: {role}")
        
        if file.filename == '':
            return jsonify({"error": "No selected file"}), 400
        
        # Extract text from PDF
        file_content = file.read()
        print(f"File size: {len(file_content)} bytes")
        
        resume_text = extract_text_from_pdf(file_content)
        print(f"Extracted text length: {len(resume_text)} characters")
        
        if not resume_text or len(resume_text.strip()) < 10:
            print("Warning: Very little text extracted from resume")
            return jsonify({
                "found_skills": [],
                "missing_skills": [],
                "suggestions": ["Could not extract text from your resume. Please ensure it's a valid PDF with text (not an image)."],
                "courses": [],
                "roadmap": {}
            })
        
        # Extract skills
        found_skills = extract_skills(resume_text)
        missing_skills = get_missing_skills(found_skills, role)
        suggestions = generate_suggestions(found_skills, missing_skills, role)
        course_recommendations = get_course_recommendations(missing_skills)
        learning_roadmap = generate_learning_roadmap(role, found_skills, missing_skills)
        
        print(f"Found skills: {found_skills}")
        print(f"Missing skills: {missing_skills}")
        print(f"Course recommendations: {len(course_recommendations)}")
        print("=== Analysis Complete ===\n")
        
        return jsonify({
            "found_skills": found_skills,
            "missing_skills": missing_skills,
            "suggestions": suggestions,
            "courses": course_recommendations,
            "roadmap": learning_roadmap
        })
    
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500

@app.route("/health", methods=["GET"])
def health():
    """Health check endpoint"""
    return jsonify({"status": "ok"})

if __name__ == "__main__":
    app.run(host="localhost", port=5001, debug=True)
