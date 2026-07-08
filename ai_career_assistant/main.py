from openai import OpenAI
import streamlit as st
from dotenv import load_dotenv
import os
import json


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

Return your response in valid JSON format.

Do not include markdown.
Do not include code blocks.
Return JSON only.

Use the following structure.

Return JSON with this structure:

{{
  "job_summary":"",
  "core_skills":[],
  "preferred_skills": [],
  "soft_skills": [],
  "skill_gap": "Coming Soon",
  "suggested_learning": "Coming Soon"
}}

---

Job Description:

{job_description}
"""
        with st.spinner("Analyzing..."):
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


        data = json.loads(result)

        st.subheader("Job Summary")
        st.write(data["job_summary"])
        st.subheader("Core Skills")
        for skill in data["core_skills"]:
            st.write(f"• {skill}")
        st.subheader("Preferred Skills")

        for skill in data["preferred_skills"]:
            st.write(f"• {skill}")
        st.subheader("Soft Skills")

        for skill in data["soft_skills"]:
            st.write(f"• {skill}")

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