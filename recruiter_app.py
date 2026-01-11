import streamlit as st


st.set_page_config(page_title="Recruiter ATS Screening", layout="wide")

st.title("🧑‍💼 Recruiter ATS Resume Screening")
st.caption("Authenticated Recruiter Portal")

# ==================================================
# 🧠 Job Roles with MAIN SKILL + REQUIRED SKILLS
# ==================================================
ROLE_SKILLS = {
    "Java Developer": {
        "main": "java",
        "skills": ["java", "spring", "spring boot", "hibernate", "sql", "oops", "data structures"]
    },
    "Python Developer": {
        "main": "python",
        "skills": ["python", "django", "flask", "sql", "oops"]
    },
    "Machine Learning Engineer": {
        "main": "machine learning",
        "skills": ["python", "machine learning", "scikit-learn", "pandas", "numpy", "statistics"]
    },
    "Data Scientist": {
        "main": "python",
        "skills": ["python", "machine learning", "statistics", "pandas", "sql"]
    },
    "Web Developer": {
        "main": "javascript",
        "skills": ["html", "css", "javascript", "react", "bootstrap"]
    },
    "Full Stack Developer": {
        "main": "javascript",
        "skills": ["html", "css", "javascript", "react", "node", "express", "python", "sql"]
    }
}

# ==================================================
# 📄 PDF Reader
# ==================================================
def read_pdf(file):
    reader = PyPDF2.PdfReader(file)
    text = ""
    for page in reader.pages:
        if page.extract_text():
            text += page.extract_text()
    return text.lower()

# ==================================================
# 📊 ATS Evaluation Logic (WITH YOUR CONDITIONS)
# ==================================================
def evaluate_resume(text, role):
    role_data = ROLE_SKILLS[role]
    main_skill = role_data["main"]
    required = role_data["skills"]

    matched = [s for s in required if s in text]
    missing = [s for s in required if s not in text]

    score = int((len(matched) / len(required)) * 100)

    # ✅ CONDITIONS
    main_skill_present = main_skill in text
    two_skills_present = len(matched) >= 2
    percentage_pass = score >= 50

    if main_skill_present or two_skills_present or percentage_pass:
        decision = "SELECT"
    else:
        decision = "REJECT"

    return score, decision, matched, missing, required, main_skill_present

# ==================================================
# 🔐 Recruiter Authentication
# ==================================================
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    st.subheader("🔐 Recruiter Login")

    recruiter_name = st.text_input("Recruiter Name")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if recruiter_name and password:
            st.session_state.logged_in = True
            st.success(f"Welcome {recruiter_name}")
        else:
            st.error("Please enter valid credentials")

# ==================================================
# 📊 ATS DASHBOARD
# ==================================================
else:
    st.subheader("📊 ATS Resume Evaluation Dashboard")

    role = st.selectbox("Target Job Role", ROLE_SKILLS.keys())
    resume_file = st.file_uploader(
        "Upload Candidate Resume (Anonymous)",
        type=["pdf", "txt"]
    )

    if st.button("🔍 Run ATS Evaluation"):
        if not resume_file:
            st.warning("Please upload a resume")
            st.stop()

        resume_text = (
            read_pdf(resume_file)
            if resume_file.type == "application/pdf"
            else resume_file.read().decode("utf-8").lower()
        )

        score, decision, matched, missing, required, main_skill_present = evaluate_resume(resume_text, role)

        # ATS Badge
        if decision == "SELECT" and score >= 70:
            fit, badge = "HIGH FIT", "🟢 SHORTLIST"
        elif decision == "SELECT":
            fit, badge = "MODERATE FIT", "🟡 CONSIDER"
        else:
            fit, badge = "LOW FIT", "🔴 REJECT"

        st.markdown("## 🧠 ATS Screening Summary")

        c1, c2, c3 = st.columns(3)
        c1.metric("Skill Match", f"{score}%")
        c2.metric("Matched Skills", len(matched))
        c3.metric("Role Fit", fit)

        st.progress(score / 100)

        st.markdown("### 📌 ATS Recommendation")
        st.success(badge)

        # import streamlit as st
import PyPDF2

# ---------------- Page Config ----------------
st.set_page_config(page_title="Recruiter ATS", layout="wide")

st.title("🧑‍💼 Recruiter ATS Resume Screening")
st.caption("Secure Recruiter Evaluation Portal")

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
        extracted = page.extract_text()
        if extracted:
            text += extracted
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
        decision = "SELECT"
    else:
        decision = "REJECT"

    return score, decision, matched, missing, skills

# ---------------- Login State ----------------
if "login" not in st.session_state:
    st.session_state.login = False

# ---------------- Login Page ----------------
if not st.session_state.login:
    st.subheader("🔐 Recruiter Login")

    name = st.text_input("Recruiter Name")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if name != "" and password != "":
            st.session_state.login = True
            st.success("Login Successful")
        else:
            st.error("Enter both name and password")

# ---------------- ATS Dashboard ----------------
else:
    st.subheader("📊 ATS Resume Screening")

    role = st.selectbox("Select Job Role", ROLE_SKILLS.keys())
    resume = st.file_uploader("Upload Resume", type=["pdf", "txt"])

    if st.button("Evaluate Resume"):
        if resume is None:
            st.warning("Please upload resume")
        else:
            if resume.type == "application/pdf":
                text = read_pdf(resume)
            else:
                text = resume.read().decode("utf-8").lower()

            score, decision, matched, missing, skills = evaluate_resume(text, role)

            st.markdown("## 🧠 Screening Result")
            st.metric("Skill Match %", score)
            st.progress(score / 100)

            if decision == "SELECT":
                st.success("🟢 Candidate Selected")
            else:
                st.error("🔴 Candidate Rejected")

            st.markdown("### Required Skills")
            st.write(", ".join(skills))

            st.markdown("### Matched Skills")
            st.write(", ".join(matched) if matched else "None")

            st.markdown("### Missing Skills")
            st.write(", ".join(missing) if missing else "None")

    if st.button("Logout"):
        st.session_state.login = False
