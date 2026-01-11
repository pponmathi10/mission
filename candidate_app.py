import streamlit as st
import PyPDF2

st.set_page_config(page_title="Candidate Resume Screening", layout="centered")

st.title("🧑 Candidate Resume Screening")


# ==================================================
# 🧠 Job Roles & Skills
# ==================================================
ROLE_SKILLS = {
    "Java Developer": [
        "java", "spring", "spring boot", "hibernate",
        "sql", "mysql", "oops", "data structures"
    ],
    "Python Developer": [
        "python", "django", "flask", "sql", "oops"
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

    return score, decision, matched, missing

# ==================================================
# 🧑 Candidate UI
# ==================================================
candidate_name = st.text_input("Candidate Name")
role = st.selectbox("Job Role", ROLE_SKILLS.keys())
resume_file = st.file_uploader("Upload Resume", type=["pdf", "txt"])

if st.button("🚀 Screen Resume"):
    if not candidate_name or not resume_file:
        st.warning("Please enter your name and upload resume")
        st.stop()

    resume_text = (
        read_pdf(resume_file)
        if resume_file.type == "application/pdf"
        else resume_file.read().decode("utf-8").lower()
    )

    score, decision, matched, missing = evaluate_resume(resume_text, role)

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


