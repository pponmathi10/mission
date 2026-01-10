import streamlit as st
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
import PyPDF2

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="AI Resume Screening", layout="wide")

st.markdown(
    "<h1 style='text-align:center;'>🤖 Intelligent Resume Screening System</h1>",
    unsafe_allow_html=True
)
st.markdown(
    "<p style='text-align:center;'>Candidate & Recruiter Dashboard using NLP and ML</p>",
    unsafe_allow_html=True
)
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

# ---------------- TABS ----------------
candidate_tab, recruiter_tab = st.tabs(["🧑 Candidate View", "🧑‍💼 Recruiter View"])

# =========================================================
# 🧑 CANDIDATE VIEW
# =========================================================
with candidate_tab:
    st.subheader("Candidate Profile")

    skills = st.text_input("Skills (comma separated)")
    education = st.selectbox("Education", ["B.Sc", "B.Tech", "M.Sc", "MBA", "PhD"])
    certifications = st.text_input("Certifications")
    experience = st.slider("Experience (Years)", 0, 30, 1)
    job_role = st.text_input("Job Role Applied For")

    st.markdown("### Upload Resume (Optional)")
    uploaded_file = st.file_uploader("PDF or TXT", type=["pdf", "txt"])

    if st.button("🚀 Evaluate My Resume"):

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
            st.stop()

        vector = vectorizer.transform([combined_text])
        prediction = model.predict(vector)[0]
        confidence = max(model.predict_proba(vector)[0]) * 100
        ai_score = int(confidence)

        st.markdown("## 📊 Screening Result")

        col1, col2 = st.columns(2)
        col1.metric("AI Confidence", f"{confidence:.2f}%")
        col2.metric("AI Score", f"{ai_score}/100")

        if prediction == "Hire":
            st.success("✅ Recruiter Decision: HIRE")
        else:
            st.error("❌ Recruiter Decision: REJECT")

        st.progress(ai_score / 100)

# =========================================================
# 🧑‍💼 RECRUITER VIEW
# =========================================================
with recruiter_tab:
    st.subheader("Recruiter Dashboard")

    col1, col2, col3 = st.columns(3)

    col1.metric("Total Candidates", len(df))
    col2.metric("Hired", (df["Recruiter Decision"] == "Hire").sum())
    col3.metric("Rejected", (df["Recruiter Decision"] == "Reject").sum())

    st.markdown("### Filter Candidates")

    selected_role = st.selectbox(
        "Filter by Job Role",
        ["All"] + sorted(df["Job Role"].unique().tolist())
    )

    filtered_df = df.copy()
    if selected_role != "All":
        filtered_df = filtered_df[filtered_df["Job Role"] == selected_role]

    st.markdown("### Candidate List")
    st.dataframe(filtered_df, use_container_width=True)

    st.markdown("### Top Candidates (Based on AI Score)")
    if "AI Score (0-100)" in filtered_df.columns:
        ranked = filtered_df.sort_values("AI Score (0-100)", ascending=False)
        st.dataframe(ranked.head(5), use_container_width=True)
    else:
        st.info("AI Score column not available in dataset")

