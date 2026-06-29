from openai import OpenAI
import streamlit as st
from dotenv import load_dotenv
import os

# Load API Key
load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)

# --------------------------
# Title
# --------------------------

st.title("AI Career Assistant")
st.subheader("Analyze job descriptions with AI")

# --------------------------
# Sidebar
# --------------------------

page = st.sidebar.radio(
    "Navigation",
    [
        "Job Analyzer",
        "My Profile"
    ]
)

# ============================================================
# Job Analyzer
# ============================================================

if page == "Job Analyzer":

    st.header("Job Analyzer")

    job_description = st.text_area(
        "Job Description",
        placeholder="Paste a job description here..."
    )

    if st.button("Analyze Job"):

        prompt = f"""
You are an experienced technical recruiter.

Analyze this job description.

Please provide:

1. Job Summary

2. Core Skills

3. Nice-to-have Skills

4. Soft Skills

5. Career Advice

Job Description:

{job_description}
"""

        response = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        result = response.choices[0].message.content

        st.markdown(result)

# ============================================================
# My Profile
# ============================================================

elif page == "My Profile":

    st.header("My Profile")

    uploaded_file = st.file_uploader(
        "Upload CV PDF",
        type=["pdf"]
    )

    resume = st.text_area(
        "Or Paste CV Text"
    )

    if st.button("Save Profile"):

        st.success("Coming Soon 🚀")