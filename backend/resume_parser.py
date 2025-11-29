# backend/resume_parser.py

import pdfplumber
import re
import json
import os
import streamlit as st

# --- Helper Function to Load Keywords (Cached) ---
@st.cache_data
def load_keywords():
    # Correctly construct the path to the keywords file
    # Navigates up from backend/ to the root, then into data/
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    keyword_path = os.path.join(base_dir, 'data', 'keywords.json')
    
    try:
        with open(keyword_path, 'r') as f:
            data = json.load(f)
            # Combine all skills from all categories into one flat list for comprehensive extraction
            all_skills = []
            for category in data.values():
                all_skills.extend(category)
            # Ensure skills are lowercase for matching
            return [skill.lower() for skill in all_skills]
    except FileNotFoundError:
        st.error(f"Error: Keyword file not found at {keyword_path}. Cannot extract skills.")
        return []

# Load the comprehensive skills list globally
ALL_SKILLS = load_keywords()

def extract_text_from_pdf(uploaded_file):
    text = ""
    with pdfplumber.open(uploaded_file) as pdf:
        for page in pdf.pages:
            text += page.extract_text() + "\n"
    return text

def extract_skills(text):
    text = text.lower()
    found = []
    
    for skill in ALL_SKILLS:
        # Use a regex pattern with word boundaries (\b) to find the skill 
        # anywhere in the document, regardless of the section heading.
        pattern = r'\b' + re.escape(skill) + r'\b' 
        if re.search(pattern, text):
            found.append(skill)
            
    return found