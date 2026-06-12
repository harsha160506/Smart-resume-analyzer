import re

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


# -------------------------------------
# Skills Database
# -------------------------------------

SKILLS = [
    "python",
    "java",
    "c++",
    "machine learning",
    "deep learning",
    "data science",
    "sql",
    "html",
    "css",
    "javascript",
    "react",
    "node",
    "flask",
    "django",
    "power bi",
    "tableau",
    "nlp",
    "tensorflow",
    "pytorch",
    "git",
    "github",
    "pandas",
    "numpy",
    "scikit-learn"
]


# -------------------------------------
# Clean Text
# -------------------------------------

def extract_text(text):

    text = re.sub(r"\s+", " ", text)

    return text.lower()


# -------------------------------------
# Extract Skills From Resume
# -------------------------------------

def extract_skills(text):

    text = text.lower()

    found_skills = set()

    for skill in SKILLS:

        if skill.lower() in text:
            found_skills.add(skill)

    return sorted(list(found_skills))


# -------------------------------------
# Analyze Resume
# -------------------------------------

def analyze_resume(text):

    clean_text = extract_text(text)

    skills = extract_skills(clean_text)

    return {
        "skills_found": skills,
        "skills_count": len(skills)
    }


# -------------------------------------
# Extract Skills From JD
# -------------------------------------

def extract_jd_skills(jd_text):

    clean_text = extract_text(jd_text)

    required_skills = []

    for skill in SKILLS:

        if skill.lower() in clean_text:
            required_skills.append(skill)

    return sorted(list(set(required_skills)))


# -------------------------------------
# ATS Score
# -------------------------------------

def ats_score(found_skills, required_skills):

    if len(required_skills) == 0:
        return 0, []

    matched = set(found_skills).intersection(
        set(required_skills)
    )

    score = (
        len(matched) /
        len(required_skills)
    ) * 100

    return round(score, 2), sorted(list(matched))


# -------------------------------------
# Improvement Tips
# -------------------------------------

def generate_improvement_tips(
        found_skills,
        required_skills
):

    missing = list(
        set(required_skills)
        - set(found_skills)
    )

    tips = []

    if missing:

        tips.append(
            f"Add missing skills: {', '.join(missing)}"
        )

    tips.append(
        "Add at least 2 real-world projects."
    )

    tips.append(
        "Use action verbs like Built, Developed, Designed, Implemented."
    )

    tips.append(
        "Mention tools, frameworks and libraries clearly."
    )

    tips.append(
        "Quantify achievements with percentages and numbers."
    )

    tips.append(
        "Keep resume ATS-friendly with clear section headings."
    )

    return sorted(missing), tips


# -------------------------------------
# Resume Section Analysis
# -------------------------------------

def analyze_sections(text):

    text = text.lower()

    sections = {
        "Education": False,
        "Skills": False,
        "Projects": False,
        "Experience": False,
        "Certifications": False
    }

    if "education" in text:
        sections["Education"] = True

    if "skills" in text:
        sections["Skills"] = True

    if "project" in text:
        sections["Projects"] = True

    if "experience" in text:
        sections["Experience"] = True

    if (
        "certification" in text
        or
        "certifications" in text
    ):
        sections["Certifications"] = True

    return sections


# -------------------------------------
# Skill Recommendation Engine
# -------------------------------------

def recommend_skills(found_skills):

    recommendations = {

        "python": [
            "flask",
            "django"
        ],

        "machine learning": [
            "tensorflow",
            "pytorch"
        ],

        "sql": [
            "power bi",
            "tableau"
        ],

        "javascript": [
            "react",
            "node"
        ],

        "nlp": [
            "tensorflow",
            "pytorch"
        ]
    }

    suggested = []

    for skill in found_skills:

        if skill in recommendations:

            suggested.extend(
                recommendations[skill]
            )

    return sorted(
        list(set(suggested))
    )


# -------------------------------------
# Resume Ranking
# -------------------------------------

def rank_resume(
        resume_skills,
        required_skills
):

    score, matched = ats_score(
        resume_skills,
        required_skills
    )

    return {
        "score": score,
        "matched_skills": matched
    }


# -------------------------------------
# Resume vs JD Similarity Score
# -------------------------------------

def calculate_similarity(
        resume_text,
        jd_text
):

    documents = [
        resume_text,
        jd_text
    ]

    vectorizer = TfidfVectorizer()

    matrix = vectorizer.fit_transform(
        documents
    )

    similarity = cosine_similarity(
        matrix[0:1],
        matrix[1:2]
    )[0][0]

    return round(
        similarity * 100,
        2
    )


# -------------------------------------
# Resume Strength Meter
# -------------------------------------

def get_resume_strength(score):

    if score >= 85:
        return "Excellent"

    elif score >= 70:
        return "Good"

    elif score >= 50:
        return "Average"

    else:
        return "Weak"


# -------------------------------------
# Project Recommendation Engine
# -------------------------------------

def recommend_projects(
        missing_skills
):

    skill_projects = {

        "tensorflow":
            "Image Classification using CNN",

        "pytorch":
            "Object Detection System",

        "nlp":
            "Sentiment Analysis Application",

        "sql":
            "Student Database Management System",

        "machine learning":
            "House Price Prediction",

        "deep learning":
            "Face Recognition System",

        "power bi":
            "Business Analytics Dashboard",

        "react":
            "E-Commerce Website",

        "node":
            "Real-Time Chat Application"
    }

    projects = []

    for skill in missing_skills:

        if skill in skill_projects:

            projects.append(
                skill_projects[skill]
            )

    return sorted(
        list(set(projects))
    )