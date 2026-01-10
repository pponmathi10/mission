import streamlit as st
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
import PyPDF2

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="AI Resume Screening", layout="centered")

st.markdown("<h1 style='text-align:center;'>🤖 Intelligent Resume Screening System</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center;'>NLP & Machine Learning Based Candidate Evaluation</p>", unsafe_allow_html=True)
st.markdown("---")

# ---------------- LOAD DATA ----------------
df = pd.read_csv("AI_Resume_Screening.csv")

df["Skills"] = df["Skills"].fillna("")
df["Education"] = df["Education"].fillna("")
df["Certifications"] = df["Certifications"].fillna("")
df["Job Role"] = df["Job Role"].fillna("")
df["Experience (Years)"] = df["Experience (Years)"].fillna(0)

df["text"] = (
    df["Skills"] + " " +
    df["Education"] + " " +
    df["Certifications"] + " " +
    df["Job Role"] + " " +
    df["Experience (Years)"].astype(str)
)

X = df["text"]
y = df["Recruiter Decision"]

# ---------------- TRAIN MODEL ----------------
vectorizer = TfidfVectorizer(stop_words="english", max_features=5000)
X_vec = vectorizer.fit_transform(X)

model = LogisticRegression(max_iter=1000)
model.fit(X_vec, y)

# ---------------- PDF READER ----------------
def read_pdf(file):
    reader = PyPDF2.PdfReader(file)
    text = ""
    for page in reader.pages:
        content = page.extract_text()
        if content:
            text += content
    return text

# ---------------- USER INPUT ----------------
st.subheader("🧑 Candidate Profile")

skills = st.text_input("🔹 Skills (comma separated)")
education = st.selectbox("🎓 Education", ["B.Sc", "B.Tech", "M.Sc", "MBA", "PhD"])
certifications = st.text_input("📜 Certifications")
experience = st.slider("🕒 Experience (Years)", 0, 30, 1)
job_role = st.text_input("💼 Job Role Applied For")

st.subheader("📤 Resume Upload (Optional)")
uploaded_file = st.file_uploader("Upload Resume (PDF or TXT)", type=["pdf", "txt"])

st.markdown("---")

# ---------------- SCREEN BUTTON ----------------
if st.button("🚀 Evaluate Resume"):

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

    if combined_text.strip() == "":
        st.warning("⚠️ Please enter details or upload a resume")
        st.stop()

    vector = vectorizer.transform([combined_text])
    prediction = model.predict(vector)[0]
    confidence = max(model.predict_proba(vector)[0]) * 100

    # AI Score
    ai_score = int(confidence)

    st.markdown("## 📊 Screening Result")

    col1, col2 = st.columns(2)

    with col1:
        st.metric("AI Confidence", f"{confidence:.2f}%")

    with col2:
        st.metric("AI Score", f"{ai_score} / 100")

    if prediction == "Hire":
        st.success("✅ **Recruiter Decision: HIRE**")
        st.markdown("🎯 *Candidate profile strongly matches job requirements.*")
    else:
        st.error("❌ **Recruiter Decision: REJECT**")
        st.markdown("⚠️ *Candidate profile does not sufficiently match requirements.*")

    # Skill Match Indicator
    skill_count = len(skills.split(",")) if skills else 0

    st.markdown("### 🔍 Profile Summary")
    st.write(f"• **Skills Provided:** {skill_count}")
    st.write(f"• **Education Level:** {education}")
    st.write(f"• **Experience:** {experience} years")
    st.write(f"• **Applied Role:** {job_role}")

    st.progress(min(ai_score / 100, 1.0))
