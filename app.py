import streamlit as st
from skills_list import skills_data
from PyPDF2 import PdfReader
import re

# 📄 Function to extract text from PDF
def extract_text_from_pdf(uploaded_file):
    text = ""
    pdf_reader = PdfReader(uploaded_file)
    for page in pdf_reader.pages:
        text += page.extract_text() or ""
    return text.lower()

# 🤖 Analyze resume function (Improved + Emoji Style)
def analyze_resume(resume_text, job_role):
    required_skills = skills_data.get(job_role, [])
    found = []
    missing = []

    # 🔎 Exact skill matching using regex
    for skill in required_skills:
        if re.search(r'\b' + re.escape(skill.lower()) + r'\b', resume_text):
            found.append(skill)
        else:
            missing.append(skill)

    total = len(required_skills)
    score = int((len(found) / total) * 100) if total > 0 else 0
    return found, missing, score


# 🎨 Streamlit UI
st.set_page_config(page_title="🧠 Resume Skill Matcher", page_icon="🚀", layout="centered")

st.title("🧠 AI Resume Skill Matcher")
st.write("📥 *Upload your resume* and see how well it matches your desired job role!")

# 🧑‍💻 Select job role
job_role = st.selectbox("💼 Select Job Role", list(skills_data.keys()))

# 📤 Upload file
uploaded_file = st.file_uploader("📄 Upload your Resume (PDF only)", type=["pdf"])

if uploaded_file is not None:
    with st.spinner("⏳ Analyzing your resume... Please wait 🧾"):
        resume_text = extract_text_from_pdf(uploaded_file)
        found, missing, score = analyze_resume(resume_text, job_role)

    st.subheader(f"💼 Job Role: {job_role}")
    st.write(f"📈 Match Score: {score}%")

    if found:
        st.success(f"✅ Found Skills: {', '.join(found)}")
    else:
        st.warning("⚠️ No relevant skills found in your resume.")

    if missing:
        st.error(f"❌ Missing Skills: {', '.join(missing)}")
    else:
        st.info("🎯 Missing Skills: None (Perfect Match!)")

    if score >= 80:
        st.balloons()
        st.success("🎉 Great! Your resume fits this role very well!")
    elif score >= 50:
        st.info("👍 Good! Add a few missing skills to improve your match.")
    else:
        st.warning("🚀 Try adding more relevant skills to your resume.")