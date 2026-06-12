import streamlit as st
import PyPDF2
import plotly.graph_objects as go
import plotly.express as px

from reportlab.pdfgen import canvas

from resume_analyzer import (
    analyze_resume,
    ats_score,
    generate_improvement_tips,
    extract_jd_skills,
    analyze_sections,
    recommend_skills,
    calculate_similarity,
    get_resume_strength,
    recommend_projects
)

# ----------------------------------
# PAGE CONFIG
# ----------------------------------

st.set_page_config(
    page_title="Smart Resume Analyzer",
    page_icon="📄",
    layout="wide"
)

# ----------------------------------
# DARK THEME
# ----------------------------------

st.markdown("""
<style>

.stApp {
    background-color: #121212;
    color: white;
}

[data-testid="stSidebar"] {
    background-color: #1E1E1E;
}

div.stButton > button:first-child {
    background-color: #00BFA5;
    color: black;
    border-radius: 10px;
    font-weight: bold;
}

</style>
""", unsafe_allow_html=True)

# ----------------------------------
# PDF TEXT EXTRACTION
# ----------------------------------

def extract_text_from_pdf(pdf_file):

    reader = PyPDF2.PdfReader(pdf_file)

    text = ""

    for page in reader.pages:

        page_text = page.extract_text()

        if page_text:
            text += page_text

    return text

# ----------------------------------
# PDF REPORT
# ----------------------------------

def generate_pdf_report(
        score,
        similarity,
        skills
):

    filename = "ATS_Report.pdf"

    c = canvas.Canvas(filename)

    c.setFont("Helvetica-Bold", 16)

    c.drawString(
        100,
        800,
        "Smart Resume Analyzer Report"
    )

    c.setFont(
        "Helvetica",
        12
    )

    c.drawString(
        100,
        760,
        f"ATS Score: {score}%"
    )

    c.drawString(
        100,
        735,
        f"Resume Similarity: {similarity}%"
    )

    c.drawString(
        100,
        700,
        "Skills Found:"
    )

    c.drawString(
        100,
        680,
        ", ".join(skills)
    )

    c.save()

    return filename

# ----------------------------------
# SIDEBAR
# ----------------------------------

st.sidebar.title("📂 Navigation")

menu = [
    "Home",
    "Analyze Resume"
]

choice = st.sidebar.radio(
    "Select Option",
    menu
)

# ----------------------------------
# HOME PAGE
# ----------------------------------

if choice == "Home":

    st.title(
        "📄 Smart Resume Analyzer"
    )

    st.markdown("""
### Features

✅ Resume Upload

✅ Job Description Matching

✅ ATS Score Calculation

✅ Resume Similarity Score

✅ Resume Strength Meter

✅ Skill Gap Analysis

✅ Project Recommendations

✅ PDF Report Generation

✅ Interactive Charts

Built using Python, Streamlit, NLP Concepts and Machine Learning.
""")

# ----------------------------------
# ANALYZE PAGE
# ----------------------------------

elif choice == "Analyze Resume":

    st.title(
        "📄 Smart Resume Analyzer"
    )

    uploaded_resume = st.file_uploader(
        "Upload Resume (PDF)",
        type=["pdf"]
    )

   jd_text = st.text_area(
    "Paste Job Description",
    height=250,
    placeholder="Paste the complete job description here..."
    )

    if uploaded_resume and jd_text:

        resume_text = extract_text_from_pdf(
            uploaded_resume
        )

        # -------------------------
        # ANALYSIS
        # -------------------------

        result = analyze_resume(
            resume_text
        )

        required_skills = extract_jd_skills(
            jd_text
        )

        score, matched_skills = ats_score(
            result["skills_found"],
            required_skills
        )

        similarity_score = calculate_similarity(
            resume_text,
            jd_text
        )

        missing_skills, tips = generate_improvement_tips(
            result["skills_found"],
            required_skills
        )

        # -------------------------
        # METRICS
        # -------------------------

        st.subheader(
            "📊 Resume Metrics"
        )

        col1, col2, col3, col4 = st.columns(4)

        col1.metric(
            "Skills Found",
            len(result["skills_found"])
        )

        col2.metric(
            "Matched Skills",
            len(matched_skills)
        )

        col3.metric(
            "ATS Score",
            f"{score}%"
        )

        col4.metric(
            "Similarity",
            f"{similarity_score}%"
        )

        # -------------------------
        # ATS GAUGE
        # -------------------------

        st.subheader(
            "📈 ATS Score"
        )

        gauge = go.Figure(
            go.Indicator(
                mode="gauge+number",
                value=score,
                title={
                    "text": "ATS Score"
                },
                gauge={
                    "axis": {
                        "range": [0, 100]
                    }
                }
            )
        )

        st.plotly_chart(
            gauge,
            use_container_width=True
        )

        # -------------------------
        # RESUME STRENGTH
        # -------------------------

        strength = get_resume_strength(
            score
        )

        st.subheader(
            "💪 Resume Strength"
        )

        if strength == "Excellent":
            st.success(strength)

        elif strength == "Good":
            st.info(strength)

        elif strength == "Average":
            st.warning(strength)

        else:
            st.error(strength)

        # -------------------------
        # ATS BREAKDOWN
        # -------------------------

        st.subheader(
            "📊 ATS Breakdown"
        )

        sections = analyze_sections(
            resume_text
        )

        section_score = (
            sum(sections.values())
            / len(sections)
        ) * 100

        overall_score = round(
            (
                score +
                similarity_score +
                section_score
            ) / 3,
            2
        )

        breakdown_data = {
            "Category": [
                "Skills Match",
                "Resume Sections",
                "JD Similarity",
                "Overall ATS"
            ],
            "Score": [
                score,
                round(section_score, 2),
                similarity_score,
                overall_score
            ]
        }

        st.table(
            breakdown_data
        )

        # -------------------------
        # PIE CHART
        # -------------------------

        st.subheader(
            "📊 Skill Match Analysis"
        )

        pie_data = {
            "Category": [
                "Matched",
                "Missing"
            ],
            "Count": [
                len(matched_skills),
                len(missing_skills)
            ]
        }

        pie = px.pie(
            pie_data,
            names="Category",
            values="Count"
        )

        st.plotly_chart(
            pie,
            use_container_width=True
        )

        # -------------------------
        # SKILLS FOUND
        # -------------------------

        st.subheader(
            "✅ Skills Found"
        )

        st.write(
            result["skills_found"]
        )

        # -------------------------
        # MATCHED SKILLS
        # -------------------------

        st.subheader(
            "🎯 Matched Skills"
        )

        st.write(
            matched_skills
        )

        # -------------------------
        # MISSING SKILLS
        # -------------------------

        st.subheader(
            "❌ Missing Skills"
        )

        st.write(
            missing_skills
        )

        # -------------------------
        # PROJECT RECOMMENDATIONS
        # -------------------------

        st.subheader(
            "🚀 Suggested Projects"
        )

        projects = recommend_projects(
            missing_skills
        )

        if projects:

            for project in projects:

                st.write(
                    f"• {project}"
                )

        else:

            st.write(
                "No recommendations available."
            )

        # -------------------------
        # SECTION ANALYSIS
        # -------------------------

        st.subheader(
            "📋 Resume Section Analysis"
        )

        for section, status in sections.items():

            if status:
                st.success(
                    f"{section} Found"
                )

            else:
                st.error(
                    f"{section} Missing"
                )

        # -------------------------
        # SKILL RECOMMENDATIONS
        # -------------------------

        st.subheader(
            "🚀 Recommended Skills"
        )

        recommended = recommend_skills(
            result["skills_found"]
        )

        st.write(
            recommended
        )

        # -------------------------
        # IMPROVEMENT TIPS
        # -------------------------

        st.subheader(
            "🧠 Improvement Tips"
        )

        for tip in tips:

            st.write(
                f"• {tip}"
            )

        # -------------------------
        # PDF REPORT
        # -------------------------

        st.subheader(
            "📥 Download Report"
        )

        pdf_file = generate_pdf_report(
            score,
            similarity_score,
            result["skills_found"]
        )

        with open(
            pdf_file,
            "rb"
        ) as f:

            st.download_button(
                label="Download ATS Report",
                data=f,
                file_name="ATS_Report.pdf",
                mime="application/pdf"
            )
