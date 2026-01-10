import streamlit as st
import PyPDF2

st.set_page_config(page_title="AI Resume Screening", layout="wide")

st.title("🤖 Intelligent Resume Screening System")
st.caption("Explainable AI – Selection with Clear Reasons")

# ---------------- Job Role Skill Map ----------------
ROLE_SKILLS = {
    "Software Developer": ["python", "java", "sql", "data structures", "oops"],
    "Data Scientist": ["python", "machine learning", "statistics", "pandas", "sql"],
    "AI Engineer": ["python", "deep learning", "tensorflow", "nlp"],
    "Web Developer": ["html", "css", "javascript", "react"],
    "Java Developer":["java"]
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

    if decision == "SELECT":
        reason = "Candidate meets most of the required skills for the role."
        improvement = "No major improvement required."
    else:
        reason = "Candidate lacks important skills required for this role."
        improvement = "Learn and improve: " + ", ".join(missing)

    return score, decision, matched, missing, reason, improvement

# ---------------- UI ----------------
st.subheader("🧑 Candidate Details")

name = st.text_input("Candidate Name")
role = st.selectbox("Job Role", ROLE_SKILLS.keys())
skills = st.text_input("Your Skills (comma separated)")
experience = st.slider("Experience (Years)", 0, 20, 1)

resume_file = st.file_uploader("Upload Resume (PDF or TXT)", type=["pdf", "txt"])

if st.button("🚀 Screen Resume"):

    if not name:
        st.warning("Please enter candidate name")
        st.stop()

    resume_text = ""
    if resume_file:
        if resume_file.type == "application/pdf":
            resume_text = read_pdf(resume_file)
        else:
            resume_text = resume_file.read().decode("utf-8").lower()

    combined_text = resume_text + " " + skills.lower() + " " + str(experience)

    score, decision, matched, missing, reason, improvement = evaluate(combined_text, role)

    st.markdown("## 📊 Screening Result")

    st.metric("AI Score", f"{score} / 100")
    st.progress(score / 100)

    st.markdown(f"### 🧾 Decision: **{decision}**")

    st.markdown("### 🔍 Reason")
    st.info(reason)

    st.markdown("### ✅ Matched Skills")
    st.success(", ".join(matched) if matched else "No skills matched")

    if decision == "REJECT":
        st.markdown("### ❌ Missing Skills")
        st.error(", ".join(missing))

        st.markdown("### 📈 What You Need to Improve")
        st.warning(improvement)
    else:
        st.markdown("### 🎯 Recommendation")
        st.success("You are a strong fit for this role!")



