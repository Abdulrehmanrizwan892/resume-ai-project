import streamlit as st
from analyzer import extract_text_from_pdf, analyze_resume

st.set_page_config(page_title="Smart Resume Analyzer", page_icon="🤖", layout="centered")

st.title("🤖 Smart Resume Analyzer")
st.write("Upload your resume and get an instant AI analysis for your dream job!")

uploaded_file = st.file_uploader("📄 Upload Resume (PDF)", type=["pdf"])
job_role = st.selectbox("🎯 Select Job Role", ["Data Scientist", "Web Developer", "Android Developer", "AI Engineer"])

if uploaded_file and st.button("Analyze"):
    with st.spinner("Analyzing your resume..."):
        text = extract_text_from_pdf(uploaded_file)
        found, missing, score = analyze_resume(text, job_role)

    st.success("✅ Analysis Complete!")
    st.subheader("Results:")
    st.write(f"*Job Role:* {job_role}")
    st.write(f"*Match Score:* {score}%")

    st.write("✅ *Found Skills:*", ", ".join(found) if found else "None")
    st.write("❌ *Missing Skills:*", ", ".join(missing) if missing else "None")

    if score > 70:
        st.balloons()
        st.success("Great! Your resume fits this role quite well 🎯")
    else:
        st.info("Try improving your resume with the missing skills.")