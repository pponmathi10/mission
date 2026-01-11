import streamlit as st
import PyPDF2

st.set_page_config(page_title="AI Resume Screening", layout="wide")

st.title("🤖 Intelligent Resume Screening System")
st.caption("Candidate Portal | Recruiter Portal (Authenticated)")

# ==================================================
# 🧠 Job Roles & Skills
# ==================================================
ROLE_SKILLS = {
    "Java Developer": [
        "java", "spring", "spring boot", "hibernate",
        "sql", "mysql", "oops", "data structures"
    ],
    "Python Developer": [
        "python"
    ],
    "Machine Learning Engineer": [
        "python", "machine learning", "scikit-learn",
        "pandas", "numpy", "statistics"
    ],
    "Data Scientist": [
        "python", "machine learning", "statistics",
        "pandas", "sql", "data visualization"
    ],
    "Web Developer": [
        "html", "css", "javascript", "react", "bootstrap"
    ],
    "Full Stack Developer": [
        "html", "css", "javascript", "react",
        "node", "express", "python", "sql"
    ]
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
# 📊 Resume Evaluation
# ==================================================
def evaluate_resume(text, role):
    required = ROLE_SKILLS[role]
    matched = [s for s in required if s in text]
    missing = [s for s in required if s not in text]

    score = int((len(matched) / len(required)) * 100)
    decision = "SELECTED" if score >= 50 else "REJECTED"

    return score, decision, matched, missing, required

# ==================================================
# 🧠 Session State
# ==================================================
if "recruiter_logged_in" not in st.session_state:
    st.session_state.recruiter_logged_in = False

# ==================================================
# 🧑 Tabs
# ==================================================
candidate_tab, recruiter_tab = st.tabs(["🧑 Candidate Portal", "🧑‍💼 Recruiter Portal"])

# ==================================================
# 🧑 CANDIDATE PORTAL
# ==================================================
with candidate_tab:
    st.subheader("Candidate Resume Screening")

    candidate_name = st.text_input("Candidate Name")
    role = st.selectbox("Job Role", ROLE_SKILLS.keys())
    resume_file = st.file_uploader("Upload Resume", type=["pdf", "txt"])

    if st.button("🚀 Screen Resume"):
        if not candidate_name or not resume_file:
            st.warning("Please enter name and upload resume")
            st.stop()

        resume_text = read_pdf(resume_file) if resume_file.type == "application/pdf" else resume_file.read().decode("utf-8").lower()

        score, decision, matched, missing, _ = evaluate_resume(resume_text, role)

        st.markdown("## 📊 Screening Result")
        st.metric("AI Score", f"{score}%")
        st.progress(score / 100)

        st.markdown(f"### 🧾 Decision: **{decision}**")

        if decision == "SELECTED":
            st.success("🎉 Your resume matches the role requirements")
            st.info("Matched Skills: " + ", ".join(matched))
        else:
            st.error("❌ Resume does not meet minimum criteria")
            st.warning("Missing Skills: " + ", ".join(missing))
            st.markdown("### 📈 Skills to Improve")
            st.info(", ".join(missing))

# ==================================================
# 🧑‍💼 RECRUITER PORTAL (NO COMPANY NAME)
# ==================================================
with recruiter_tab:
    st.subheader("Recruiter Login")

    if not st.session_state.recruiter_logged_in:
        recruiter_name = st.text_input("Recruiter Name")
        password = st.text_input("Password", type="password")

        if st.button("🔐 Login"):
            if recruiter_name and password:
                st.session_state.recruiter_logged_in = True
                st.session_state.recruiter_name = recruiter_name
                st.success(f"Welcome Recruiter {recruiter_name}")
            else:
                st.error("Please enter name and password")

    else:
        st.subheader("📊 ATS Resume Evaluation Dashboard")

        role = st.selectbox("Target Job Role", ROLE_SKILLS.keys())
        resume_file = st.file_uploader("Upload Candidate Resume (Anonymous)", type=["pdf", "txt"], key="recruiter")

        if st.button("🔍 Run ATS Evaluation"):
            if not resume_file:
                st.warning("Upload resume to evaluate")
                st.stop()

            resume_text = read_pdf(resume_file) if resume_file.type == "application/pdf" else resume_file.read().decode("utf-8").lower()

            score, decision, matched, missing, required = evaluate_resume(resume_text, role)

import streamlit as st
import PyPDF2

st.set_page_config(page_title="Candidate Resume Screening", layout="centered")

st.title("🧑 Candidate Resume Screening")
st.caption("AI-based resume evaluation")

# ==================================================
# Job Roles & Skills
# ==================================================
ROLE_SKILLS = {
    "Java Developer": ["java", "spring", "sql", "oops", "data structures"],
    "Python Developer": ["python", "django", "flask", "sql"],
    "Machine Learning Engineer": ["python", "machine learning", "pandas", "scikit-learn"],
    "Data Scientist": ["python", "statistics", "sql", "machine learning"],
    "Web Developer": ["html", "css", "javascript", "react"]
}

# ==================================================
# PDF Reader
# ==================================================
def read_pdf(file):
    reader = PyPDF2.PdfReader(file)
    text = ""
    for page in reader.pages:
        if page.extract_text():
            text += page.extract_text()
    return text.lower()

# ==================================================
# Resume Evaluation
# ==================================================
def evaluate_resume(text, role):
    required = ROLE_SKILLS[role]
    matched = [skill for skill in required if skill in text]
    missing = [skill for skill in required if skill not in text]

    score = int((len(matched) / len(required)) * 100)
    decision = "SELECTED" if score >= 50 else "REJECTED"

    return score, decision, matched, missing

# ==================================================
# UI
# ==================================================
name = st.text_input("Candidate Name")
role = st.selectbox("Select Job Role", ROLE_SKILLS.keys())
resume_file = st.file_uploader("Upload Resume (PDF / TXT)", type=["pdf", "txt"])

if st.button("🚀 Screen Resume"):
    if not name or not resume_file:
        st.warning("Please enter your name and upload resume")
        st.stop()

    resume_text = (
        read_pdf(resume_file)
        if resume_file.type == "application/pdf"
        else resume_file.read().decode("utf-8").lower()
    )

    score, decision, matched, missing = evaluate_resume(resume_text, role)

    st.markdown("## 📊 Screening Result")
    st.metric("AI Match Score", f"{score}%")
    st.progress(score / 100)

    st.markdown(f"### 🧾 Decision: **{decision}**")

    if decision == "SELECTED":
        st.success("🎉 Congratulations! Your profile matches the role.")
        st.info("Matched Skills: " + ", ".join(matched))
    else:
        st.error("❌ Your resume does not meet the minimum requirements.")
        st.warning("Missing Skills: " + ", ".join(missing))
        st.markdown("### 📈 Skills to Improve")
        st.info(", ".join(missing))
