# backend/ats_engine.py (Updated for dynamic scoring)

import json
import os
import streamlit as st # Added st to use caching for the keywords

# --- Helper Function to Load Keywords (Cached) ---
# Use st.cache_data to load the file only once, improving performance
@st.cache_data
def get_ats_keywords(category="CORE_SKILLS"):
    # Path logic remains the same
    keyword_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data', 'keywords.json')
    
    try:
        with open(keyword_path, 'r') as f:
            data = json.load(f)
            # Return the keywords for the specific category
            # Use data.keys() to return all categories if we need them in the dropdown
            if category == "ALL_CATEGORIES":
                return data
            else:
                return [kw.lower() for kw in data.get(category, [])]
    except FileNotFoundError:
        st.error(f"Error: Keyword file not found at {keyword_path}. Using fallback list.")
        return ["python", "sql", "excel"]

# ----------------------------------------

# Modified to accept target_category as an argument
def compute_ats_score(resume_text, target_category="CORE_SKILLS"):
    # Load keywords based on the selected target_category
    keywords = get_ats_keywords(target_category)
    missing = []
    
    resume_text = resume_text.lower()

    for kw in keywords:
        # Check for keyword presence
        if kw not in resume_text:
            missing.append(kw)

    num_keywords = len(keywords)
    
    # Avoid division by zero if the keyword list is empty
    if num_keywords == 0:
        score = 0
        penalty_per_word = 0
    else:
        # Calculate penalty dynamically based on the number of keywords in the category
        penalty_per_word = 100 // num_keywords
        score = max(0, 100 - (len(missing) * penalty_per_word))

    return score, {"missing_keywords": missing, "target_category": target_category}