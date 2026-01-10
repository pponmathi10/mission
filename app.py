import streamlit as st
import PyPDF2

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="AI Resume Screening", layout="wide")

st.markdown("<h1 style='text-align:center;'>🤖 Intelligent Resume Screening System</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center;'>Skill & Role Based Candidate Selection</p>", unsafe_allow_html=True)
st.markdown("---")

# ---------------- SESSION STORAGE ----------------
if "candidates" not in st.session_state:
    st.session_state.candidates = []

# ---------------- JOB ROLE REQUIREMENTS ----------------
JOB_SKILLS = {
    "Data Scientist": ["python", "machine learning", "sql", "statistics", "pandas"],
    "AI Engineer": ["python", "deep learning", "tensorflow", "pytorch", "nlp"],
    "Software Developer": ["java", "python", "sql", "oops", "data structures"],
    "Web Developer": ["html", "css", "javascript", "react"],
    "Cybersecurity Analyst": ["network security", "linux", "ethical hacking"]
}

# ---------------- PDF TEXT EXTRACTION ----------------
def read_pdf(file):
    reader = PyPDF2.PdfReader(file)
    text = ""
    for page in reader.pages:
        if page.extract_text():
            text += page.extract_text()
    return text.lower()

# ---------------- AI SCORING FUNCTION ----------------
def calculate_ai_score(candidate_text, role):
    required_skills = JOB_SKILLS.get(role, [])
    if not required_skills:
        return 0

    matched = sum(1 for skill in required_skills if skill in candidate_text)
    score = int((matched / len(required_skills)) * 100)
    return score

# ---------------- TABS ----------------
candidate_tab, recruiter_tab = st.tabs(["🧑 Candidate View", "🧑‍💼 Recruiter View"])

# =====================================================
# 🧑 CANDIDATE VIEW
# =====================================================
with candidate_tab:
    st.subheader("Candidate Profile")

    name = st.text_input("Candidate Name")
    role = st.selectbox("Job Role Applied For", list(JOB_SKILLS.keys()))
    skills = st.text_input("Skills (comma separated)")
    education = st.selectbox("Education", ["B.E","B.Sc", "B.Tech", "MBA", "M.Sc", "PhD"])
    experience = st.slider("Experience (Years)", 0, 30, 1)

    uploaded_file = st.file_uploader("Upload Resume (Optional)", type=["pdf", "txt"])

    if st.button("🚀 Submit & Evaluate"):

        resume_text = ""
        if uploaded_file:
            if uploaded_file.type == "application/pdf":
                resume_text = read_pdf(uploaded_file)
            else:
                resume_text = uploaded_file.read().decode("utf-8").lower()

        combined_text = (
            resume_text + " " +
            skills.lower() + " " +
            education.lower() + " " +
            str(experience)
        )

        if name.strip() == "":
            st.warning("Please enter candidate name")
            st.stop()

        ai_score = calculate_ai_score(combined_text, role)
        decision = "SELECT" if ai_score >= 60 else "REJECT"

        st.session_state.candidates.append({
            "Name": name,
            "Role": role,
            "Skills": skills,
            "Experience": experience,
            "AI Score": ai_score,
            "Decision": decision
        })

        st.success(f"Decision: {decision}")
        st.info(f"AI Score: {ai_score} / 100")
        st.progress(ai_score / 100)

# =====================================================
# 🧑‍💼 RECRUITER VIEW
# =====================================================
with recruiter_tab:
    st.subheader("Recruiter Dashboard")

    if not st.session_state.candidates:
        st.warning("No candidates submitted yet")
    else:
        total = len(st.session_state.candidates)
        selected = sum(1 for c in st.session_state.candidates if c["Decision"] == "SELECT")
        rejected = total - selected

        col1, col2, col3 = st.columns(3)
        col1.metric("Total Candidates", total)
        col2.metric("Selected", selected)
        col3.metric("Rejected", rejected)

        st.markdown("### ✅ Selected Candidates")
        selected_list = [c for c in st.session_state.candidates if c["Decision"] == "SELECT"]
        st.dataframe(selected_list, use_container_width=True)

        st.markdown("### ❌ Rejected Candidates")
        rejected_list = [c for c in st.session_state.candidates if c["Decision"] == "REJECT"]
        st.dataframe(rejected_list, use_container_width=True)

        st.markdown("### 🏆 Top Candidates (By AI Score)")
        ranked = sorted(
            st.session_state.candidates,
            key=lambda x: x["AI Score"],
            reverse=True
        )
        st.dataframe(ranked, use_container_width=True)

