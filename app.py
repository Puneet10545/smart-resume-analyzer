import streamlit as st
import PyPDF2
import re

# ---------------- PAGE CONFIG ----------------

st.set_page_config(
    page_title="Smart Resume Analyzer",
    page_icon="📄",
    layout="wide"
)

# ---------------- CUSTOM CSS ----------------

st.markdown("""
<style>

[data-testid="stMetric"] {
    background: #1e293b;
    padding: 20px;
    border-radius: 15px;
    border: 1px solid #334155;
}

[data-testid="stMetricLabel"] {
    font-size: 16px;
}

[data-testid="stMetricValue"] {
    font-size: 32px;
    font-weight: 700;
}

</style>
""", unsafe_allow_html=True)


# ---------------- TITLE ----------------

st.markdown(
    """
    <div style="
        padding: 25px;
        border-radius: 18px;
        background: linear-gradient(135deg, #1e293b, #0f172a);
        border: 1px solid #334155;
        margin-bottom: 25px;
    ">
        <h1 style="margin: 0; font-size: 42px;">
            📄 Smart Resume Analyzer
        </h1>
        <p style="margin: 8px 0 0 0; font-size: 18px; color: #94a3b8;">
            AI-powered resume analysis, ATS scoring & career insights
        </p>
    </div>
    """,
    unsafe_allow_html=True
)


# ---------------- RESUME UPLOAD ----------------

uploaded_file = st.file_uploader(
    "Upload Your Resume (PDF)",
    type=["pdf"],
    key="resume_upload"
)


# ---------------- ANALYSIS ----------------

if uploaded_file is not None:

    # Extract text from PDF
    reader = PyPDF2.PdfReader(uploaded_file)

    resume_text = ""

    for page in reader.pages:
        text = page.extract_text()

        if text:
            resume_text += text + "\n"

    resume_text = resume_text.lower()

    st.success("✅ Resume uploaded successfully!")


    # ---------------- BASIC INFORMATION ----------------

    st.subheader("🔍 Resume Analysis")

    col1, col2, col3 = st.columns(3)


    # ---------------- WORD COUNT ----------------

    words = resume_text.split()
    word_count = len(words)


    # ---------------- EMAIL DETECTION ----------------

    email = re.findall(
        r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}",
        resume_text
    )


    # ---------------- PHONE DETECTION ----------------

    phone = re.findall(
        r"\b\d{10}\b",
        resume_text
    )


    # ---------------- SKILLS ----------------

    skills = [
        "python",
        "java",
        "c++",
        "html",
        "css",
        "javascript",
        "sql",
        "machine learning",
        "artificial intelligence",
        "data analysis",
        "excel",
        "power bi",
        "communication",
        "leadership",
        "teamwork",
        "canva",
        "recruitment",
        "human resources",
        "hr",
        "management",
        "problem solving"
    ]

    found_skills = []

    for skill in skills:
        if skill in resume_text:
            found_skills.append(skill.title())


    # ---------------- SECTIONS ----------------

    sections = {
        "Education": ["education", "qualification", "academic"],
        "Experience": ["experience", "work experience", "employment"],
        "Projects": ["projects", "project"],
        "Skills": ["skills", "technical skills"],
        "Certifications": ["certification", "certifications"],
        "Achievements": ["achievement", "achievements", "awards"]
    }

    found_sections = []

    for section, keywords in sections.items():

        if any(keyword in resume_text for keyword in keywords):
            found_sections.append(section)


    # ---------------- SCORE ----------------

    st.subheader("📊 Resume Overview")

    score = 0

    if word_count >= 250:
        score += 20

    elif word_count >= 150:
        score += 15

    else:
        score += 10


    if email:
        score += 10


    if phone:
        score += 10


    score += min(len(found_skills) * 2, 20)

    score += min(len(found_sections) * 5, 30)

    score = min(score, 100)


    # ---------------- DISPLAY SCORE ----------------

    with col1:

        st.metric(
            "Resume Score",
            f"{score}/100"
        )

        st.progress(score / 100)


    with col2:

        st.metric(
            "Word Count",
            word_count
        )


    with col3:

        st.metric(
            "Skills Found",
            len(found_skills)
        )


    st.divider()


    # ---------------- SKILLS DETECTED ----------------

    st.subheader("💡 Skills Detected")

    if found_skills:

        skill_text = " ".join(
            [f"`{skill}`" for skill in found_skills]
        )

        st.markdown(skill_text)

    else:

        st.warning("No major skills detected.")


    # ---------------- CONTACT ----------------

    st.subheader("📞 Contact Information")

    if email:

        st.success(
            f"Email detected: {email[0]}"
        )

    else:

        st.warning(
            "⚠️ Email address not detected."
        )


    if phone:

        st.success(
            "Phone number detected."
        )

    else:

        st.warning(
            "⚠️ Phone number not detected."
        )


    # ---------------- SUGGESTIONS ----------------

    st.subheader("🚀 Suggestions to Improve Your Resume")

    suggestions = []


    if word_count < 250:

        suggestions.append(
            "Add more relevant details about your education, experience and projects."
        )


    if not found_skills:

        suggestions.append(
            "Add a dedicated Skills section with job-relevant technical and soft skills."
        )


    if "Experience" not in found_sections:

        suggestions.append(
            "Add your internship, work experience or practical experience."
        )


    if "Projects" not in found_sections:

        suggestions.append(
            "Add 2–3 projects and briefly explain your contribution and results."
        )


    if "Certifications" not in found_sections:

        suggestions.append(
            "Consider adding relevant certifications or online courses."
        )


    if "Achievements" not in found_sections:

        suggestions.append(
            "Add important achievements, awards or extracurricular activities."
        )


    if not suggestions:

        suggestions.append(
            "Your resume looks well structured. Keep the content targeted to the job description."
        )


    for suggestion in suggestions:

        st.info("💡 " + suggestion)


    # ==========================================================
    #                 JOB DESCRIPTION MATCHING
    # ==========================================================

    st.subheader("🎯 Job Description Matching")

    st.write(
        "Paste the job description below to check how well your resume matches the job."
    )


    job_description = st.text_area(
        "📋 Paste Job Description",
        height=220,
        placeholder="Example: We are looking for an HR Executive with communication, recruitment, Excel and leadership skills..."
    )


    # ---------------- ANALYZE MATCH ----------------

    if st.button(
        "🔍 Analyze Match",
        use_container_width=True
    ):

        if not job_description.strip():

            st.warning(
                "⚠️ Please paste a job description first."
            )

        else:

            job_text = job_description.lower()


            # ---------------- REQUIRED SKILLS ----------------

            required_skills = []

            for skill in skills:

                if skill in job_text:

                    required_skills.append(
                        skill.title()
                    )


            # ---------------- MATCHING SKILLS ----------------

            matching_skills = []

            for skill in required_skills:

                if skill.lower() in resume_text:

                    matching_skills.append(skill)


            # ---------------- MISSING SKILLS ----------------

            missing_skills = []

            for skill in required_skills:

                if skill.lower() not in resume_text:

                    missing_skills.append(skill)


            # ---------------- ATS MATCH SCORE ----------------

            if len(required_skills) > 0:

                match_score = int(
                    (len(matching_skills) / len(required_skills)) * 100
                )

            else:

                match_score = 0


            # ---------------- RESULT ----------------

            st.divider()

            st.subheader("📊 Job Match Result")

            result_col1, result_col2, result_col3 = st.columns(3)


            # ---------------- ATS MATCH ----------------

            with result_col1:

                st.metric(
                    "🎯 ATS Match",
                    f"{match_score}%"
                )

                st.progress(
                    match_score / 100
                )


            # ---------------- MATCHING SKILLS COUNT ----------------

            with result_col2:

                st.metric(
                    "✅ Matching Skills",
                    len(matching_skills)
                )


            # ---------------- MISSING SKILLS COUNT ----------------

            with result_col3:

                st.metric(
                    "❌ Missing Skills",
                    len(missing_skills)
                )


            # ---------------- MATCHING SKILLS ----------------

            st.subheader("✅ Matching Skills")

            if matching_skills:

                skill_text = " ".join(
                    [f"`{skill}`" for skill in matching_skills]
                )

                st.markdown(skill_text)

            else:

                st.warning(
                    "No matching skills were detected."
                )


            # ---------------- MISSING SKILLS ----------------

            st.subheader("❌ Missing Skills")

            if missing_skills:

                for skill in missing_skills:

                    st.error(skill)

            else:

                st.success(
                    "🎉 Great! No major required skills are missing."
                )


            # ---------------- RECOMMENDED ROLE ----------------

            st.subheader("💼 Recommended Job Role")


            if (
                "human resources" in job_text
                or "hr" in job_text
                or "recruitment" in job_text
            ):

                recommended_role = "👩‍💼 HR Executive / HR Recruiter"

            elif (
                "data analyst" in job_text
                or "data analysis" in job_text
            ):

                recommended_role = "📊 Data Analyst"

            elif (
                "python" in job_text
                or "machine learning" in job_text
            ):

                recommended_role = "🤖 Python / AI-ML Developer"

            elif (
                "web developer" in job_text
                or "javascript" in job_text
            ):

                recommended_role = "💻 Web Developer"

            else:

                recommended_role = "💼 General Professional Role"


            st.info(recommended_role)


            # ---------------- JOB-SPECIFIC SUGGESTIONS ----------------

            st.subheader("💡 Job-Specific Suggestions")

            job_suggestions = []


            if missing_skills:

                job_suggestions.append(
                    "Add relevant missing skills to your resume if you genuinely have them."
                )


            if match_score < 50:

                job_suggestions.append(
                    "Your resume has a low match with this job. Highlight experience and skills relevant to the job description."
                )

            elif match_score < 75:

                job_suggestions.append(
                    "Your resume has a moderate match. Add more relevant keywords and measurable achievements."
                )

            else:

                job_suggestions.append(
                    "Your resume has a strong match. Keep the important job-specific keywords visible."
                )


            if "Experience" not in found_sections:

                job_suggestions.append(
                    "Add relevant internship, work or practical experience."
                )


            if "Projects" not in found_sections:

                job_suggestions.append(
                    "Add projects related to the target job."
                )


            for suggestion in job_suggestions:

                st.info(
                    "💡 " + suggestion
                )


            # ---------------- DOWNLOAD ATS REPORT ----------------

            report_text = f"""
SMART RESUME ANALYZER - ATS REPORT

Resume Score: {score}/100

Word Count: {word_count}

Skills Found: {len(found_skills)}

ATS Match Score: {match_score}%

Matching Skills:
{", ".join(matching_skills) if matching_skills else "None"}

Missing Skills:
{", ".join(missing_skills) if missing_skills else "None"}

Recommended Role:
{recommended_role}

Job Suggestions:
{chr(10).join(job_suggestions)}
"""


            st.download_button(
                label="📥 Download ATS Report",
                data=report_text,
                file_name="ATS_Resume_Report.txt",
                mime="text/plain",
                use_container_width=True
            )


# ---------------- RESUME TEXT ----------------

if "resume_text" in locals() and resume_text:

    with st.expander("📄 View Extracted Resume Text"):

        st.text(resume_text)