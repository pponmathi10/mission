import streamlit as st


# ---------------- Page Setup ----------------
st.set_page_config(page_title="Simple Recruiter ATS", layout="centered")

st.title("📄 Simple Recruiter Resume Screening")
st.caption("Lightweight ATS Logic (Error-Free Version)")

# ---------------- Roles & Skills ----------------
ROLE_SKILLS = {
    "Java Developer": {
        "main": "java",
        "skills": ["java", "spring", "sql", "oops"]
    },
    "Python Developer": {
        "main": "python",
        "skills": ["python", "django", "flask", "sql"]
    },
    "Machine Learning Engineer": {
        "main": "machine learning",
        "skills": ["python", "machine learning", "pandas", "numpy"]
    }
}

# ---------------- Resume Reader ----------------
def extract_text(file):
    if file.type == "application/pdf":
        reader = PyPDF2.PdfReader(file)
        text = ""
        for page in reader.pages:
            if page.extract_text():
                text += page.extract_text()
        return text.lower()
    else:
        return file.read().decode("utf-8").lower()

# ---------------- Evaluation ----------------
def screen_resume(text, role):
    main_skill = ROLE_SKILLS[role]["main"]
    skills = ROLE_SKILLS[role]["skills"]

    matched = [s for s in skills if s in text]
    missing = [s for s in skills if s not in text]

    score = int((len(matched) / len(skills)) * 100)

    if main_skill in text or len(matched) >= 2 or score >= 50:
        result = "SELECTED"
    else:
        result = "REJECTED"

    return score, result, matched, missing, skills

# ---------------- UI ----------------
role = st.selectbox("Choose Job Role", ROLE_SKILLS.keys())
resume = st.file_uploader("Upload Resume", type=["pdf", "txt"])

if st.button("Screen Resume"):
    if resume is None:
        st.warning("Please upload resume")
    else:
        text = extract_text(resume)
        score, result, matched, missing, skills = screen_resume(text, role)

        st.subheader("📊 Screening Outcome")
        st.metric("Skill Match (%)", score)
        st.progress(score / 100)

        if result == "SELECTED":
            st.success("🟢 Candidate SELECTED")
        else:
            st.error("🔴 Candidate REJECTED")

        st.markdown("### Required Skills")
        st.write(", ".join(skills))

        st.markdown("### Matched Skills")
        st.write(", ".join(matched) if matched else "None")

        st.markdown("### Missing Skills")
        st.write(", ".join(missing) if missing else "None")
