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
        "My Profile",
        "Market Intelligence",
        "Job Recommendation"
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
You are an experienced technical recruiter, hiring manager, and career advisor specializing in the technology industry.

Analyze the following job description.

Return your response in Markdown format.

Use the following structure.

# Job Summary

Summarize the role in 3-5 sentences.

---

# Core Skills

List the most important technical skills.

---

# Preferred Skills

List optional or bonus skills.

---

# Soft Skills

List important communication or business skills.

---

# Skill Gap

This feature is not implemented yet.

Output exactly:

Coming Soon

---

# Suggested Learning

This feature is not implemented yet.

Output exactly:

Coming Soon

---

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

    CV = st.text_area(
        "Or Paste CV Text"
    )

    if st.button("Save Profile"):

        st.success("Coming Soon")

elif page == "Market Intelligence":
    st.header("Market Intelligence")


elif page == "Job Recommendation":
    st.header("Job Recommendation")