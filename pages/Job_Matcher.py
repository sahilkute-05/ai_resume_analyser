# Job_Matcher.py (Finalized with Score Sorting)

import streamlit as st
from backend.job_scraper import scrape_all_jobs
from backend.match_engine import compute_match
import operator # New import for efficient sorting

def main():
    st.title("💼 Job Matcher")

    if "resume_text" not in st.session_state or st.session_state.resume_text is None:
        st.warning("Please upload and analyze your resume in the **Resume Analyzer** page first.")
        return 

    role = st.text_input("Enter job role (e.g., Data Analyst, ML Engineer)")

    if role:
        st.write("Fetching live jobs...")
        jobs = scrape_all_jobs(role)

        if not jobs:
            st.info("No jobs found or failed to scrape. Try a different role or check connection.")
            return

        # --- Step 1: Calculate Scores and Store ---
        scored_jobs = []
        with st.spinner('Calculating Match Scores...'):
            for job in jobs:
                # Compute match score using the job description text
                score = compute_match(job["description"], st.session_state.resume_text)
                
                # Add the score to the job dictionary
                job["match_score"] = score 
                scored_jobs.append(job)

        # --- Step 2: Sort Jobs ---
        # Sort the jobs by 'match_score' in descending order (highest score first)
        sorted_jobs = sorted(scored_jobs, key=operator.itemgetter('match_score'), reverse=True)

        st.subheader(f"Matched Jobs for '{role}' ({len(sorted_jobs)} total found, sorted by Match Score)")
        
        # --- Step 3: Display Sorted Jobs ---
        for job in sorted_jobs:
            score = job["match_score"]
            
            st.markdown(f"### {job['title']} - Match Score: {score}%")
            
            # Display New Fields
            st.markdown(f"**Company:** {job.get('company', 'N/A')} | **Source:** **{job.get('source', 'N/A')}** | **Posted:** {job.get('posted_on', 'N/A')}")
            st.markdown(f"**Experience:** {job.get('experience', 'N/A')} | **Location:** {job.get('location', 'N/A')} | **Salary:** {job.get('salary', 'N/A')}")
            
            # Link to the job
            st.write(f"[Read Full JD / Apply]({job['link']})")
            st.markdown("---") 

if __name__ == "__main__":
    main()