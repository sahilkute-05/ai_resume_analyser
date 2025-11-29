# Resume_Analyzer.py

import streamlit as st
import pdfplumber
from backend.resume_parser import extract_text_from_pdf, extract_skills
from backend.ats_engine import compute_ats_score # [New Import]
from backend.llm_matcher import detect_candidate_seniority # [Seniority Detection]

def main():
    st.title("📄 Resume Analyzer")

    # Initialize session state keys for reliable access on other pages
    if 'resume_text' not in st.session_state:
        st.session_state.resume_text = None
    if 'ats_score' not in st.session_state:
        st.session_state.ats_score = None
    if 'ats_details' not in st.session_state:
        st.session_state.ats_details = None
    if 'seniority_level' not in st.session_state:
        st.session_state.seniority_level = "Unknown"

    uploaded_file = st.file_uploader("Upload your resume (PDF)", type=["pdf"])

    if uploaded_file:
        text = extract_text_from_pdf(uploaded_file)
        # Store text immediately for Job Matcher
        st.session_state.resume_text = text 

        st.subheader("Extracted Resume Text")
        st.write(text)

        skills = extract_skills(text)
        st.subheader("Detected Skills")
        st.write(skills)
        
        # --- ATS Analysis and Storage --- [New Logic]
        score, details = compute_ats_score(text)
        
        # Store ATS results for ATS_Score.py and Suggestions.py
        st.session_state.ats_score = score
        st.session_state.ats_details = details
        
        # --- Seniority Detection --- [New Logic]
        seniority = detect_candidate_seniority(text)
        st.session_state.seniority_level = seniority

        st.success("✅ Resume successfully analyzed! Check your score and suggestions using the sidebar.")

if __name__ == "__main__":
    main()