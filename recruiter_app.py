import streamlit as st
import PyPDF2

# ---------------- Page Config ----------------
st.set_page_config(page_title="Recruiter ATS", layout="centered")

st.title("🧑‍💼 Recruiter ATS Resume Screening")

# ---------------- Role Skills ----------------
ROLE_SKILLS = {
    "Java Developer": {
        "main": "java",
        "skills": ["java", "spring", "sql", "oops", "data structures"]
    },
    "Python Developer": {
        "main": "python",
        "skills": ["python", "django", "flask", "sql", "oops"]
    },
    "Machine Learning Engineer": {
        "main": "machine learning",
        "skills": ["python", "machine learning", "pandas", "numpy", "scikit-learn"]
    }
}

# ---------------- PDF Reader ----------------
def read_pdf(file):
    reader = PyPDF2.PdfReader(file)
    text = ""
    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text
    return text.lower()

# ---------------- Resume Evaluation ----------------
def evaluate_resume(text, role):
    main_skill = ROLE_SKILLS[role]["main"]
    skills = ROLE_SKILLS[role]["skills"]

    matched = []
    for skill in skills:
        if skill in text:
            matched.append(skill)

    missing = []
    for skill in skills:
        if skill not in text:
            missing.append(skill)

    score = int((len(matched) / len(skills)) * 100)

    if (main_skill in text) or (len(matched) >= 2) or (score >= 50):
        decision = "SELECTED"
    else:
        decision = "REJECTED"

    return score, decision, matched, missing, skills

# ---------------- App UI ----------------
role = st.selectbox("Select Job Role", list(ROLE_SKILLS.keys()))
resume = st.file_uploader("Upload Resume", type=["pdf", "txt"])

if st.button("Evaluate Resume"):
    if resume is None:
        st.warning("Please upload a resume file")
    else:
        if resume.type == "application/pdf":
            resume_text = read_pdf(resume)
        else:
            resume_text = resume.read().decode("utf-8").lower()

        score, decision, matched, missing, skills = evaluate_resume(resume_text, role)

        st.subheader("📊 Screening Result")
        st.metric("Skill Match Percentage", f"{score}%")
        st.progress(score / 100)

        if decision == "SELECTED":
            st.success("🟢 Candidate SELECTED")
        else:
            st.error("🔴 Candidate REJECTED")

        st.markdown("### Required Skills")
        st.write(", ".join(skills))

        st.markdown("### Matched Skills")
        st.write(", ".join(matched) if matched else "None")

        st.markdown("### Missing Skills")
        st.write(", ".join(missing) if missing else "None")
