from openai import OpenAI
import streamlit as st

from dotenv import load_dotenv
import os

load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)
st.title("AI Career Assistant")
st.subheader("Analyze job descriptions with AI")

# User input
job_description = st.text_area(
    "Job Description:",
    "Please enter your job description"
)
# Resume Upload
uploaded_file = st.file_uploader(
    "Upload Resume PDF",
    type=["pdf"]
)

# OR Paste Resume
resume = st.text_area(
    label="Or Paste Resume Text:",
    value=""
)
# Button
if st.button("Compare this resume with the job description."):

    prompt = f"""
Analyze this job description.

Give:

1. Match Score
2. Matching skills
3. Missing skills
4. Suggestions for improvement

JD:

{job_description}


Resume:
{resume}

"""
    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    result = response.choices[0].message.content

    st.markdown(result)