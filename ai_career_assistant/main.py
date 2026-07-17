from openai import OpenAI
import streamlit as st
from dotenv import load_dotenv
import os
import json
from pypdf import PdfReader


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
    include_skill_gap = st.checkbox(
        "Include Skill Gap Analysis"
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
  "soft_skills": []
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

        if include_skill_gap:
            if not os.path.exists("profile.json"):
                st.warning(
                    "Please create and save your profile first before using Skill Gap Analysis."
                )
            else:
                try:
                    with open("profile.json", "r") as f:
                        profile_data = json.load(f)

                    skill_gap_prompt = f"""
Compare this candidate's skills with the skills needed for this job.

Candidate skills:
{profile_data["skills"]}

Required job skills:
{data["core_skills"]}

Preferred job skills:
{data["preferred_skills"]}

Return your response in valid JSON format.
Do not include markdown.
Do not include code blocks.
Return JSON only.

Use this structure:

{{
  "matched_skills": [],
  "missing_required_skills": [],
  "missing_preferred_skills": []
}}
"""

                    with st.spinner("Checking skill gaps..."):
                        response = client.chat.completions.create(
                            model="gpt-4.1-mini",
                            messages=[
                                {
                                    "role": "user",
                                    "content": skill_gap_prompt
                                }
                            ]
                        )

                        skill_gap_result = response.choices[0].message.content
                        skill_gap_data = json.loads(skill_gap_result)

                    st.subheader("Skill Gap Analysis")
                    st.write("Matched Skills")
                    for skill in skill_gap_data["matched_skills"]:
                        st.write(f"- {skill}")

                    st.write("Missing Required Skills")
                    for skill in skill_gap_data["missing_required_skills"]:
                        st.write(f"- {skill}")

                    st.write("Missing Preferred Skills")
                    for skill in skill_gap_data["missing_preferred_skills"]:
                        st.write(f"- {skill}")

                except Exception as e:
                    st.error(f"Skill Gap Analysis failed: {e}")

# ============================================================
# My Profile
# ============================================================

elif page == "My Profile":

    st.header("My Profile")

    uploaded_file = st.file_uploader(
        "Upload CV PDF",
        type=["pdf"]
    )

    cv_text = st.text_area(
        "Or Paste CV Text"
    )


    if st.button("Generate Profile"):
        if uploaded_file is not None:

            reader = PdfReader(uploaded_file)

            pdf_text = ""

            for page in reader.pages:
                pdf_text += page.extract_text()

            resume_text = pdf_text

        else:

            resume_text = cv_text

        prompt = f"""
        Analyze the following CV.

        Return your response in valid JSON format.
        
        Do not include markdown.
        Do not include code blocks.
        Return JSON only.
        
        Use the following structure.
        
        Return JSON with this structure:

        {{
            "name": "",
            "experience": "",
            "skills": [],
            "languages": [],
            "education": [],
            "preferred_roles": []
        }}
        Resume:

        {resume_text}"""
        with st.spinner("Generating profile..."):

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

        st.subheader("AI Extracted Profile")

        st.subheader("Name")
        st.write(data["name"])
        st.subheader("Experience")
        st.write(data["experience"])
        st.subheader("Skills")
        for skill in data["skills"]:
            st.write(f"• {skill}")
        st.subheader("Languages")

        for language in data["languages"]:
            st.write(f"• {language}")
        st.subheader("Education")

        for edu in data["education"]:
            st.write(edu["degree"])
            st.write(edu["institution"])

        if st.button("Save Profile"):
            try:
                with open("profile.json", "w") as f:
                    json.dump(data, f, indent=4)

                st.success("Profile saved successfully!")

            except Exception as e:
                st.error(f"Failed to save profile: {e}")


elif page == "Market Intelligence":
    st.header("Market Intelligence")


elif page == "Job Recommendation":
    st.header("Job Recommendation")
