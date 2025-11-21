# ATS_Score.py (Updated to allow target role selection)

import streamlit as st
from backend.ats_engine import compute_ats_score, get_ats_keywords # Import both functions

def main():
    st.title("📊 ATS Score Checker")

    if "resume_text" not in st.session_state or st.session_state.resume_text is None:
        st.write("Upload and analyze your resume first in the **Resume Analyzer** page.")
        return

    # Load all keyword categories to populate the dropdown
    all_categories = get_ats_keywords("ALL_CATEGORIES")
    category_names = list(all_categories.keys())

    # Create the dropdown for the user to select the job role/category
    st.markdown("---")
    st.subheader("Select Target Job Category")
    target_category = st.selectbox(
        "Choose a category to calculate a score specific to those keywords:",
        options=category_names,
        index=category_names.index("CORE_SKILLS") if "CORE_SKILLS" in category_names else 0
    )
    st.markdown("---")

    # Get the resume text from session state
    resume_text = st.session_state.resume_text

    # Compute the targeted ATS score
    score, details = compute_ats_score(resume_text, target_category=target_category)

    # Display Results
    st.write(f"### ATS Score for **{target_category.replace('_', ' ').title()}** Role: {score}/100")
    
    # Optional: Visual display of score
    st.progress(score / 100)
    
    st.markdown("---")
    st.subheader("Analysis Details")
    
    # Display missing keywords
    missing = details.get("missing_keywords", [])
    if missing:
        st.warning(f"### ⚠️ Missing Keywords ({len(missing)})")
        st.write("Your resume is missing the following key terms for this category:")
        st.code(', '.join(missing))
    else:
        st.success("🎉 You've covered all the core keywords for this category!")


if __name__ == "__main__":
    main()