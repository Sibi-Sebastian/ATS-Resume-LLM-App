from dotenv import load_dotenv

load_dotenv()

import streamlit as st
import base64
import os
import io
from PIL import Image
import pdf2image
import google.generativeai as genai

# Fetch API key from environment variables
api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    st.error("API key is not set. Please check your environment variables.")
else:
    genai.configure(api_key=api_key)

def get_gemini_response(input, pdf_content, prompt):
    try:
        model = genai.GenerativeModel('gemini-1.5-flash')  # Corrected model name
        response = model.generate_content([input, pdf_content[0], prompt])
        return response.text
    except Exception as e:
        st.error(f"An unexpected error occurred: {e}")

def input_pdf_setup(uploaded_file):
    if uploaded_file is not None:
        images = pdf2image.convert_from_bytes(uploaded_file.read())
        
        first_page = images[0]
        
        img_byte_arr = io.BytesIO()
        first_page.save(img_byte_arr, format='JPEG')
        img_byte_arr = img_byte_arr.getvalue()
        
        pdf_parts = [
            {
                "mime_type": "image/jpeg",
                "data": base64.b64encode(img_byte_arr).decode()
            }
        ]
        return pdf_parts
    else:
        raise FileNotFoundError("No file uploaded")

## Streamlit App
st.set_page_config(page_title="ATS Resume Expert")
st.header("ATS Tracking System")
input_text = st.text_area("Job Description: ", key="input")
uploaded_file = st.file_uploader("Upload your resume (PDF)...", type=["pdf"])

if uploaded_file is not None:
    st.write("PDF Uploaded Successfully")

submit1 = st.button("Tell Me About the Resume")
submit2 = st.button("How can I improvise my Skills?")
submit3 = st.button("Percentage match")

input_prompt1 = """
You are an experienced Technical Human Resource manager with expertise in hiring for [target job title/s]. Given the provided resume and the following job description:

[Paste the target job description here]

Please provide your professional evaluation of the candidate's profile. How well does their overall background align with the requirements and responsibilities outlined in the job description?

Specifically, highlight the following aspects:

Key strengths and skills demonstrated in the resume that are directly relevant to the job.
Areas where the candidate's experience or skills seem to fall short of the job requirements.
Any potential concerns or red flags that you identify based on the information provided.
Remember, your analysis should be objective and unbiased, focusing solely on the information presented in the resume and job description.
"""

input_prompt2 = """
Based on the provided resume and the target job description for [target job title/s]:

[Paste the target job description here]

Please identify areas where the candidate's skills and experience could be further improved to better align with the job requirements. Offer specific and actionable recommendations for enhancing the candidate's profile, focusing on:

Skills or knowledge that are explicitly mentioned in the job description but seem lacking in the resume.
Areas where the candidate's experience could be showcased more effectively to highlight its relevance to the desired role.
General soft skills or competencies that would be valuable assets for the position.
Your suggestions should be practical and tailored to the individual's background and career goals. Remember, the aim is to provide constructive feedback that empowers the candidate to take concrete steps towards improving their job prospects.
"""

input_prompt3 = """
You are an skilled ATS (Applicant Tracking System) scanner with a deep understanding in the field of any one job role from Data Science, Full Stack Web Development, Big Data Engineering, DEVOPS, Data Analyst and deep ATS functionality, 
your task is to evaluate the resume against the provided job description. give me the percentage of match if the resume matches
the job description. First the output should come as percentage and then keywords missing and last final thoughts.

Analyzing the provided resume and the target job description for [target job title/s]:

[Paste the target job description here]

Identify key skills, keywords, and terms that are frequently mentioned in the job description but appear to be missing or underrepresented in the candidate's resume. Focus on:

Specific technical skills, industry-specific terminology, and software proficiency requirements mentioned in the job description.
Soft skills, qualifications, and personal attributes that are emphasized as desirable or essential.
Action verbs and strong adjectives that can enhance the impact of the resume's content.
Remember, including relevant keywords can help improve the resume's visibility and searchability by Applicant Tracking Systems (ATS). However, avoid keyword stuffing or artificial manipulation of the content.
"""

if submit1:
    if uploaded_file is not None:
        try:
            pdf_content = input_pdf_setup(uploaded_file)
            response = get_gemini_response(input_prompt1, pdf_content, input_text)
            if response:
                st.subheader("The Response is")
                st.write(response)
            else:
                st.error("No response received from the API.")
        except Exception as e:
            st.error(f"An error occurred: {e}")
    else:
        st.write("Please upload the resume")

elif submit2:
    if uploaded_file is not None:
        try:
            pdf_content = input_pdf_setup(uploaded_file)
            response = get_gemini_response(input_prompt2, pdf_content, input_text)
            if response:
                st.subheader("The Response is")
                st.write(response)
            else:
                st.error("No response received from the API.")
        except Exception as e:
            st.error(f"An error occurred: {e}")
    else:
        st.write("Please upload the resume")

elif submit3:
    if uploaded_file is not None:
        try:
            pdf_content = input_pdf_setup(uploaded_file)
            response = get_gemini_response(input_prompt3, pdf_content, input_text)
            if response:
                st.subheader("The Response is")
                st.write(response)
            else:
                st.error("No response received from the API.")
        except Exception as e:
            st.error(f"An error occurred: {e}")
    else:
        st.write("Please upload the resume")
