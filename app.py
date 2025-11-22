# app.py (Updated to Manually Build Sidebar Navigation)

import streamlit as st

st.set_page_config(
    page_title="AI Resume Analyzer",
    page_icon="📄",
    layout="wide"
)

# --- Main Page Content ---
st.title("AI Resume Analyzer + Job Matcher")
st.write("Use the sidebar links below to navigate between tools.")
st.write("Welcome to the AI-powered Resume Analyzer + Job Matcher platform!") # Content from original Home.py

# --- Custom Sidebar Navigation ---
st.sidebar.title("🛠️ Application Tools")
st.sidebar.markdown("---")

# Use st.page_link to link to the page files (now in the 'pages' directory)
st.sidebar.page_link("pages/Resume_Analyzer.py", label="📄 Resume Analyzer")
st.sidebar.page_link("pages/ATS_Score.py", label="📊 ATS Score Checker")
st.sidebar.page_link("pages/Suggestions.py", label="✨ Resume Improvement Suggestions")
st.sidebar.page_link("pages/Job_Matcher.py", label="💼 Job Matcher")

st.sidebar.markdown("---")
st.sidebar.info("Upload your resume on the Analyzer page to begin!")