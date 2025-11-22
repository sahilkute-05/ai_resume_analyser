# Suggestions.py

import streamlit as st

def main():
    st.title("✨ Resume Improvement Suggestions")
    
    # Ensure session state is initialized and has the required details
    if "ats_details" in st.session_state and st.session_state.ats_details is not None:
        details = st.session_state.ats_details
        # Safely get missing_keywords
        missing_keywords = details.get("missing_keywords", [])

        ## Suggestions Based on ATS/Keywords
        st.subheader("🎯 Keyword Gap Analysis (Based on Generic ATS Check)")
        
        if missing_keywords:
            st.warning("Your resume might be missing some crucial keywords used in generic ATS checks. Incorporating these can improve your score.")
            st.markdown(f"**Missing Keywords:** `{', '.join(missing_keywords)}`")
            st.markdown("* **Action:** Try to incorporate these skills naturally into your experience descriptions, if you possess them.")
        else:
            st.success("Great job! Your resume covers the base keywords for this project's simple check.")

        ## General Suggestions
        st.subheader("💡 General Resume Best Practices")
        st.info("These suggestions are based on general industry standards.")
        st.markdown(
            """
            * **Quantify your achievements:** Use numbers and metrics to describe your impact. For example, instead of 'Managed projects,' write 'Managed 5 projects, leading to a **15%** efficiency gain.'
            * **Keep it concise:** For most roles, aim for a single-page resume if you have less than 10 years of experience.
            * **Tailor to the job:** For a real application, always adjust your skills and experience descriptions to match the job description's language exactly for the best match score.
            """
        )
    else:
        st.write("Please upload and analyze your resume in the **Resume Analyzer** page first to generate suggestions.")

if __name__ == "__main__":
    main()