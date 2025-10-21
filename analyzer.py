import PyPDF2
import json
import re
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

def extract_text_from_pdf(uploaded_file):
    pdf_reader = PyPDF2.PdfReader(uploaded_file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text.lower()

def clean_text(text):
    stop_words = set(stopwords.words('english'))
    words = word_tokenize(text)
    return [w for w in words if w.isalnum() and w not in stop_words]

def analyze_resume(text, job_role):
    with open("skills.json", "r") as f:
        data = json.load(f)

    job_role = job_role.lower()
    required_skills = data.get(job_role, [])
    found = []
    for skill in required_skills:
        if re.search(r'\b' + re.escape(skill.lower()) + r'\b', text):
            found.append(skill)
    missing = list(set(required_skills) - set(found))
    score = int((len(found) / len(required_skills)) * 100) if required_skills else 0
    return found, missing, score