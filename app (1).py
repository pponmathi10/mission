import streamlit as st
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
import PyPDF2

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="Resume Screening System", layout="centered")
st.title("📄 Intelligent Resume Screening System")
st.subheader("Using NLP and Machine Learning")

# ---------------- LOAD DATA ----------------
df = pd.read_csv("AI_Resume_Screening.csv")

# Combine dataset text columns
df["resume_text"] = (
    df["Skills"].fillna("") + " " +
    df["Education"].fillna("") + " " +
    df["Certifications"].fillna("") + " " +
    df["Job Role"].fillna("") + " " +
    df["Experience (Years)"].astype(str)
)

X = df["resume_text"]
y = df["Recruiter Decision"]

# ---------------- TRAIN MODEL ----------------
vectorizer = TfidfVectorizer(stop_words="english", max_features=5000)
X_vec = vectorizer.fit_transform(X)

model = LogisticRegression(max_iter=1000)
model.fit(X_vec, y)

# ---------------- PDF TEXT EXTRACTION ----------------
def extract_text_from_pdf(uploaded_file):
    reader = PyPDF2.PdfReader(uploaded_file)
    text = ""
    for page in reader.pages:
        if page.extract_text():
            text += page.extract_text()
    return text

# ---------------- USER INPUT SECTION ----------------
st.markdown("## 🧑 Candidate Details")

skills = st.text_input("Skills (comma separated)")
education = st.selectbox(
    "Education",
    ["B.Sc", "B.Tech", "M.Sc", "MBA", "PhD"]
)
certifications = st.text_input("Certifications")
experience = st.slider("Experience (Years)", 0, 20, 1)

job_role = st.text_input("Job Role Applied For")

st.markdown("## 📤 Upload Resume")
uploaded_file = st.file_uploader(
    "Upload Resume (PDF or TXT)",
    type=["pdf", "txt"]
)

manual_resume = st.text_area(
    "OR paste resume text (optional)",
    height=150
)

# ---------------- PREDICTION ----------------
if st.button("🚀 Screen My Resume"):

    resume_text = ""

    # Priority: uploaded resume
    if uploaded_file is not None:
        if uploaded_file.type == "application/pdf":
            resume_text = extract_text_from_pdf(uploaded_file)
        else:
            resume_text = uploaded_file.read().decode("utf-8")

    # Else manual resume
    elif manual_resume.strip() != "":
        resume_text = manual_resume

    # Combine resume + form details
    final_text = (
        resume_text + " " +
        skills + " " +
        education + " " +
        certifications + " " +
        job_role + " " +
        str(experience)
    )

    resume_vec = vectorizer.transform([final_text])
    prediction = model.predict(resume_vec)[0]
    confidence = max(model.predict_proba(resume_vec)[0]) * 100

    st.markdown("## 📊 Screening Result")
    st.markdown(f"### ✅ Decision: **{prediction}**")
    st.markdown(f"### 🔍 Confidence Score: **{confidence:.2f}%**")

    if prediction == "Hire":
        st.success("🎯 You are suitable for this role!")
    else:
        st.error("❌ Profile does not match current requirements.")
