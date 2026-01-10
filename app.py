import streamlit as st
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
import PyPDF2

# ---------------- PAGE SETUP ----------------
st.set_page_config(page_title="Resume Screening", layout="centered")
st.title("📄 Intelligent Resume Screening System")

# ---------------- LOAD DATA ----------------
df = pd.read_csv("AI_Resume_Screening.csv")

# Safe column handling
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
vectorizer = TfidfVectorizer(stop_words="english")
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
st.subheader("🧑 Enter Your Details")

skills = st.text_input("Skills")
education = st.selectbox("Education", ["B.Sc", "B.Tech", "M.Sc", "MBA", "PhD"])
certifications = st.text_input("Certifications")
experience = st.number_input("Experience (Years)", 0, 40, 0)
job_role = st.text_input("Job Role Applied For")

st.subheader("📤 Upload Resume (Optional)")
uploaded_file = st.file_uploader("Upload PDF or TXT", type=["pdf", "txt"])

# ---------------- SCREEN BUTTON ----------------
if st.button("🚀 Screen Resume"):

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
        st.warning("Please enter details or upload resume")
    else:
        vector = vectorizer.transform([combined_text])
        result = model.predict(vector)[0]
        confidence = max(model.predict_proba(vector)[0]) * 100

        st.success(f"Decision: {result}")
        st.info(f"Confidence Score: {confidence:.2f}%")
