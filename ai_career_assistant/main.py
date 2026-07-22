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
  "seniority": "Entry-level, Junior, Mid-level, Senior, Lead, Manager, or Unknown",
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

        st.subheader("Job Seniority")
        st.write(data.get("seniority", "Unknown"))

        st.subheader("Match Score")
        if not os.path.exists("profile.json"):
            st.write("Create and save a profile to calculate your match score.")
        else:
            try:
                with open("profile.json", "r") as f:
                    profile_data = json.load(f)

                match_score_prompt = f"""
Compare this candidate with the job requirements.

Candidate experience:
{profile_data.get("experience", "")}

Candidate skills:
{profile_data.get("skills", [])}

Required job skills:
{data["core_skills"]}

Preferred job skills:
{data["preferred_skills"]}

Recognize exact skill matches and closely related, transferable skills. Do not treat an
unrelated skill as a match. Give core skills 70% of the score and preferred skills 30%.
If only one group of job skills is present, use that group for 100% of the score.

Return your response in valid JSON format.
Do not include markdown.
Do not include code blocks.
Return JSON only.

Use this structure:

{{
  "match_score": 0,
  "match_explanation": "",
  "transferable_skills": []
}}
"""

                with st.spinner("Calculating match score..."):
                    response = client.chat.completions.create(
                        model="gpt-4.1-mini",
                        messages=[
                            {
                                "role": "user",
                                "content": match_score_prompt
                            }
                        ]
                    )

                    match_score_result = response.choices[0].message.content
                    match_score_data = json.loads(match_score_result)

                st.write(f"{round(match_score_data['match_score'])}%")
                st.write(match_score_data["match_explanation"])

                if match_score_data["transferable_skills"]:
                    st.write("Transferable Skills Considered")
                    for skill in match_score_data["transferable_skills"]:
                        st.write(f"- {skill}")

            except Exception as e:
                st.error(f"Match score could not be calculated: {e}")

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

    if "generated_profile" not in st.session_state:
        st.session_state.generated_profile = None

    if os.path.exists("profile.json"):
        try:
            with open("profile.json", "r") as f:
                saved_profile = json.load(f)

            st.subheader("Saved Profile")
            st.subheader("Name")
            st.write(saved_profile.get("name", "No name recorded."))
            st.subheader("Experience")
            st.write(saved_profile.get("experience", "No experience recorded."))

            st.subheader("Skills")
            if saved_profile.get("skills"):
                for skill in saved_profile["skills"]:
                    st.write(f"- {skill}")
            else:
                st.write("No skills recorded.")

            st.subheader("Languages")
            if saved_profile.get("languages"):
                for language in saved_profile["languages"]:
                    st.write(f"- {language}")
            else:
                st.write("No languages recorded.")

            st.subheader("Education")
            if saved_profile.get("education"):
                for edu in saved_profile["education"]:
                    st.write(edu.get("degree", "No degree recorded."))
                    st.write(edu.get("institution", "No institution recorded."))
                    st.write(edu.get("period", ""))
            else:
                st.write("No education recorded.")

            st.subheader("Preferred Roles")
            if saved_profile.get("preferred_roles"):
                for role in saved_profile["preferred_roles"]:
                    st.write(f"- {role}")
            else:
                st.write("No preferred roles recorded.")

        except Exception as e:
            st.error(f"Saved profile could not be loaded: {e}")
    else:
        st.info("No saved profile yet. Upload a CV or paste CV text below to create one.")

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
        st.session_state.generated_profile = data

    if st.session_state.generated_profile is not None:
        data = st.session_state.generated_profile
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
