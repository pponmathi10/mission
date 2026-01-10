import streamlit as st
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
import PyPDF2

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="AI Resume Screening", layout="wide")

st.markdown("<h1 style='text-align:center;'>🤖 Intelligent Resume Screening System</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center;'>Candidate & Recruiter View (No CSV)</p>", unsafe_allow_html=True)
st.markdown("---")

# ---------------- SESSION STORAGE ----------------
if "candidates" not in st.session_state:
    st.session_state.candidates = []

# ---------------- SIMPLE TRAINING DATA ----------------
train_texts = [
    "python machine learning data science ai",
    "java sql backend developer",
    "html css javascript frontend",
    "cybersecurity network security",
    "python deep learning nlp ai"
]
train_labels = ["Hire", "Hire", "Reject", "Reject", "Hire"]

vectorizer = TfidfVectorizer(stop_words="english")
X_train = vectorizer.fit_transform(train_texts)

model = LogisticRegression()
model.fit(X_train, train_labels)

# ---------------- PDF TEXT EXTRACTION ----------------
def read_pdf(file):
    reader = PyPDF2.PdfReader(file)
    text = ""
    for page in reader.pages:
        if page.extract_text():
            text += page.extract_text()
    return text

# ---------------- TABS ----------------
candidate_tab, recruiter_tab = st.tabs(["🧑 Candidate View", "🧑‍💼 Recruiter View"])

# ===================================================
# 🧑 CANDIDATE VIEW
# ===================================================
with candidate_tab:
    st.subheader("Candidate Profile")

    name = st.text_input("Candidate Name")
    skills = st.text_input("Skills")
    education = st.selectbox("Education", ["B.E","B.Sc", "B.Tech", "MBA", "M.Sc", "PhD"])
    certifications = st.text_input("Certifications")
    experience = st.slider("Experience (Years)", 0, 30, 1)
    job_role = st.text_input("Job Role Applied For")

    uploaded_file = st.file_uploader("Upload Resume (PDF or TXT)", type=["pdf", "txt"])

    if st.button("🚀 Submit Resume"):

        resume_text = ""
        if uploaded_file:
            if uploaded_file.type == "application/pdf":
                resume_text = read_pdf(uploaded_file)
            else:
                resume_text = uploaded_file.read().decode("utf-8")

        combined_text = (
            resume_text + " " +
            skills + " " +
            education + " " +
            certifications + " " +
            job_role + " " +
            str(experience)
        )

        if combined_text.strip() == "" or name.strip() == "":
            st.warning("Please enter name and details")
            st.stop()

        vec = vectorizer.transform([combined_text])
        decision = model.predict(vec)[0]
        confidence = max(model.predict_proba(vec)[0]) * 100
        ai_score = int(confidence)

        # Save candidate data (NO CSV)
        st.session_state.candidates.append({
            "Name": name,
            "Skills": skills,
            "Education": education,
            "Experience": experience,
            "Job Role": job_role,
            "Decision": decision,
            "AI Score": ai_score
        })

        st.success(f"Decision: {decision}")
        st.info(f"AI Score: {ai_score}/100")

# ===================================================
# 🧑‍💼 RECRUITER VIEW
# ===================================================
with recruiter_tab:
    st.subheader("Recruiter Dashboard (Live Candidate Data)")

    if len(st.session_state.candidates) == 0:
        st.warning("No candidates submitted yet")
    else:
        total = len(st.session_state.candidates)
        hired = sum(1 for c in st.session_state.candidates if c["Decision"] == "Hire")
        rejected = total - hired

        col1, col2, col3 = st.columns(3)
        col1.metric("Total Candidates", total)
        col2.metric("Hired", hired)
        col3.metric("Rejected", rejected)

        st.markdown("### Candidate List")
        st.dataframe(st.session_state.candidates, use_container_width=True)

        st.markdown("### Top Candidates")
        ranked = sorted(
            st.session_state.candidates,
            key=lambda x: x["AI Score"],
            reverse=True
        )
        st.dataframe(ranked[:5], use_container_width=True)


