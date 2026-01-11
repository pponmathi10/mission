import streamlit as st
import PyPDF2

st.set_page_config(page_title="Candidate Resume Screening", layout="wide")

st.title("🧑 Candidate Resume Screening Portal")
st.caption("AI-based Resume Evaluation")

# ==================================================
# 🧠 Job Roles, Main Skill & Required Skills
# ==================================================
ROLE_SKILLS = {
    "Java Developer": {
        "main": "java",
        "skills": ["java", "spring", "spring boot", "sql", "oops", "data structures"]
    },
    "Python Developer": {
        "main": "python",
        "skills": ["python", "django", "flask", "sql", "oops"]
    },
    "Machine Learning Engineer": {
        "main": "machine learning",
        "skills": ["python", "machine learning", "scikit-learn", "pandas", "numpy"]
    },
    "Data Scientist": {
        "main": "python",
        "skills": ["python", "machine learning", "statistics", "pandas", "sql"]
    },
    "Web Developer": {
        "main": "javascript",
        "skills": ["html", "css", "javascript", "react", "bootstrap"]
    }
}

# ==================================================
# 📄 PDF Reader
# ==================================================
def read_pdf(file):
    reader = PyPDF2.PdfReader(file)
    text = ""
    for page in reader.pages:
        if page.extract_text():
            text += page.extract_text()
    return text.lower()

# ==================================================
# 📊 Resume Evaluation Logic (YOUR CONDITIONS)
# ==================================================
def evaluate_resume(text, role):
    role_data = ROLE_SKILLS[role]
    main_skill = role_data["main"]
    required_skills = role_data["skills"]

    matched = [s for s in required_skills if s in text]
    missing = [s for s in required_skills if s not in text]

    score = int((len(matched) / len(required_skills)) * 100)

    # ✅ Selection Conditions
    main_skill_present = main_skill in text
    two_skills_present = len(matched) >= 2
    percentage_pass = score >= 50

    if main_skill_present or two_skills_present or percentage_pass:
        decision = "SELECTED"
    else:
        decision = "REJECTED"

    return score, decision, matched, missing, main_skill_present

# ==================================================
# 🧑 Candidate Input
# ==================================================
st.subheader("📤 Upload Your Resume")

candidate_name = st.text_input("Candidate Name")
role = st.selectbox("Job Role Applying For", ROLE_SKILLS.keys())
resume_file = st.file_uploader("Upload Resume (PDF or TXT)", type=["pdf", "txt"])

if st.button("🚀 Screen My Resume"):
    if not candidate_name or not resume_file:
        st.warning("Please enter your name and upload your resume")
        st.stop()

    if resume_file.type == "application/pdf":
        resume_text = read_pdf(resume_file)
    else:
        resume_text = resume_file.read().decode("utf-8").lower()

    score, decision, matched, missing, main_skill_present = evaluate_resume(resume_text, role)

    # ==================================================
    # 📊 Output
    # ==================================================
    st.markdown("## 📊 Screening Result")
    st.metric("AI Skill Match Score", f"{score}%")
    st.progress(score / 100)

    st.markdown(f"### 🧾 Final Decision: **{decision}**")

    if decision == "SELECTED":
        st.success("🎉 Congratulations! Your resume meets the selection criteria.")

        reasons = []
        if main_skill_present:
            reasons.append("Main skill detected")
        if len(matched) >= 2:
            reasons.append("At least 2 required skills matched")
        if score >= 50:
            reasons.append("Skill match percentage ≥ 50%")

        st.info("✅ Selection Reason(s): " + " | ".join(reasons))
        st.write("**Matched Skills:**", ", ".join(matched))

    else:
        st.error("❌ Unfortunately, your resume does not meet the minimum criteria.")
        st.warning("**Missing Skills:** " + ", ".join(missing))

        st.markdown("### 📈 How You Can Improve")
        st.info(
            f"Focus on learning and adding these skills to your resume: "
            f"{', '.join(missing[:3])}"
    )
