# pages/Job_Matcher.py (Final LLM Integration)

import streamlit as st
from backend.job_scraper import scrape_all_jobs
from backend.llm_matcher import analyze_and_match_llm # NEW IMPORT
import operator
# Note: No need for compute_match, TfidfVectorizer, or manual keyword extraction imports!

def main():
    st.title("💼 Job Matcher")

    # --- Initial Checks ---
    if 'resume_text' not in st.session_state or st.session_state.resume_text is None:
        st.warning("Please upload and analyze your resume in the **Resume Analyzer** page first.")
        return 
    
    # NOTE: You must calculate seniority in Resume_Analyzer.py first!
    if 'seniority_level' not in st.session_state:
        st.session_state.seniority_level = "Unknown" 
    
    user_seniority = st.session_state.seniority_level

    st.subheader(f"Candidate Seniority: {user_seniority}")
    role = st.text_input("Enter target job role (e.g., Data Scientist, ML Engineer)")

    if role:
        st.write("Fetching live jobs...")
        jobs = scrape_all_jobs(role)

        if not jobs:
            st.info("No jobs found or failed to retrieve from API.")
            return

        scored_jobs = []
        with st.spinner('🤖 Analyzing Profile and Calculating Contextual Match Scores (This may take 10-20 seconds)...'):
            for job in jobs:
                
                # --- LLM MATCHING LOGIC ---
                llm_result = analyze_and_match_llm(
                    st.session_state.resume_text, 
                    job["description"], 
                    user_seniority # Pass user seniority for better analysis
                )
                
                if llm_result is None: continue # Skip if API failed entirely
                
                # Extract structured data from LLM response
                score = llm_result.get("SCORE", 0)
                
                job["match_score"] = score
                job["shared_keywords"] = llm_result.get("SHARED_SKILLS", [])
                job["missing_keywords"] = llm_result.get("MISSING_SKILLS", [])
                job["llm_summary"] = llm_result.get("SUMMARY", "Score reason unavailable.")
                job["llm_seniority"] = llm_result.get("SENIORITY_ESTIMATE", "N/A")

                scored_jobs.append(job)
                # --- END LLM MATCHING ---

        # Sort the jobs by match score
        sorted_jobs = sorted(scored_jobs, key=operator.itemgetter('match_score'), reverse=True)

        st.subheader(f"Matched Jobs for '{role}' ({len(sorted_jobs)} total found, sorted by Match Score)")
        
        for job in sorted_jobs:
            score = job["match_score"]
            
            st.markdown(f"### {job['title']} - Match Score: {score}%")
            
            st.info(f"**Recruiter Analysis:** {job['llm_summary']}")
            st.caption(f"LLM Estimated Job Seniority: {job['llm_seniority']}")
            
            # Display Shared Keywords
            if job["shared_keywords"]:
                st.success(f"**Top Shared Skills:** {', '.join(job['shared_keywords'][:8])}")
            
            # Display Missing Skills
            if job["missing_keywords"]:
                st.warning(f"**🚨 Missing Skills:** {', '.join(job['missing_keywords'][:5])}")
            
            # Display Metadata
            st.markdown(f"**Company:** {job.get('company', 'N/A')} | **Source:** **{job.get('source', 'N/A')}** | **Posted:** {job.get('posted_on', 'N/A')}")
            st.markdown(f"**Experience:** {job.get('experience', 'N/A')} | **Location:** {job.get('location', 'N/A')} | **Salary:** {job.get('salary', 'N/A')}")
            
            st.write(f"[Read Full JD / Apply]({job['link']})")
            st.markdown("---") 

if __name__ == "__main__":
    main()