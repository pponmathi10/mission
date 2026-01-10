import streamlit as st
import PyPDF2

st.set_page_config(page_title="AI Resume Screening", layout="wide")

st.title("🤖 Intelligent Resume Screening System")
st.caption("Candidate View & Recruiter View")

# ---------------- Job Role Skills ----------------
ROLE_SKILLS = {
    "Software Developer": ["python", "java", "sql", "data structures", "oops"],
    "Data Scientist": ["python", "machine learning", "statistics", "pandas", "sql"],
    "AI Engineer": ["python", "deep learning", "tensorflow", "nlp"],
    "Web Developer": ["html", "css", "javascript", "react"],
    "Java Developer":["java","java full stack"],
    "Python Developer":["python"]
}

# ---------------- PDF Reader ----------------
def read_pdf(file):
    reader = PyPDF2.PdfReader(file)
    text = ""
    for page in reader.pages:
        if page.extract_text():
            text += page.extract_text()
    return text.lower()

# ---------------- Evaluation Logic ----------------
def evaluate(text, role):
    required = ROLE_SKILLS[role]
    matched = [s for s in required if s in text]
    missing = [s for s in required if s not in text]

    score = int((len(matched) / len(required)) * 100)
    decision = "SELECT" if score >= 60 else "REJECT"

    return score, decision, matched, missing, required

# ---------------- Tabs ----------------
candidate_tab, recruiter_tab = st.tabs(["🧑 Candidate View", "🧑‍💼 Recruiter View"])

# ==================================================
# 🧑 CANDIDATE VIEW
# ==================================================
with candidate_tab:
    st.subheader("Candidate Resume Screening")

    name = st.text_input("Candidate Name")
    role = st.selectbox("Job Role", ROLE_SKILLS.keys())
    skills = st.text_input("Your Skills (comma separated)")
    resume_file = st.file_uploader("Upload Resume (Optional)", type=["pdf", "txt"])

    if st.button("🚀 Evaluate (Candidate)"):

        if not name:
            st.warning("Please enter your name")
            st.stop()

        resume_text = ""
        if resume_file:
            if resume_file.type == "application/pdf":
                resume_text = read_pdf(resume_file)
            else:
                resume_text = resume_file.read().decode("utf-8").lower()

        combined_text = resume_text + " " + skills.lower()

        score, decision, matched, missing, required = evaluate(combined_text, role)

        st.markdown("## 📊 Result")
        st.metric("AI Score", f"{score}/100")
        st.progress(score / 100)

        st.markdown(f"### 🧾 Decision: **{decision}**")

        if decision == "SELECT":
            st.success("You are suitable for this role.")
            st.info("Reason: You match most of the required skills.")
        else:
            st.error("You are not suitable for this role.")
            st.warning("Reason: Important skills are missing.")

            st.markdown("### ❌ Missing Skills")
            st.write(", ".join(missing))

            st.markdown("### 📈 What You Need to Improve")
            st.info("Learn and practice: " + ", ".join(missing))

# ==================================================
# 🧑‍💼 RECRUITER VIEW
# ==================================================
with recruiter_tab:
    st.subheader("Recruiter Resume Screening")

    role = st.selectbox("Job Role (Recruiter)", ROLE_SKILLS.keys())
    resume_file = st.file_uploader("Upload Candidate Resume", type=["pdf", "txt"], key="recruiter")

    if st.button("🚀 Evaluate (Recruiter)"):

        if not resume_file:
            st.warning("Please upload a resume")
            st.stop()

        if resume_file.type == "application/pdf":
            resume_text = read_pdf(resume_file)
        else:
            resume_text = resume_file.read().decode("utf-8").lower()

        score, decision, matched, missing, required = evaluate(resume_text, role)

        st.markdown("## 📊 Screening Summary")

        st.metric("AI Score", f"{score}/100")
        st.progress(score / 100)

        st.markdown(f"### 🧾 Decision: **{decision}**")

        st.markdown("### 📌 Required Skills")
        st.write(", ".join(required))

        st.markdown("### ✅ Matched Skills")
        st.success(", ".join(matched) if matched else "No skills matched")

        st.markdown("### ❌ Missing Skills")
        st.error(", ".join(missing) if missing else "No missing skills")




