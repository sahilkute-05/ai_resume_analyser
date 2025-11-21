# backend/job_scraper.py (FINAL Orchestrator)

import streamlit as st
from backend.job_scrapers.naukri_scraper import scrape_naukri_jobs 
from backend.job_scrapers.indeed_scraper import scrape_indeed_jobs 
from backend.job_scrapers.internshala_scraper import scrape_internshala_jobs 

def scrape_all_jobs(role):
    """
    Calls all individual scraper functions and combines the results.
    """
    all_jobs = []

    st.subheader("🌐 Scraping Jobs from Multiple Platforms...")

    # 1. Scrape Naukri Jobs
    with st.spinner('Scraping Naukri...'):
        naukri_jobs = scrape_naukri_jobs(role)
    st.info(f"✅ Found {len(naukri_jobs)} jobs from Naukri.com")
    all_jobs.extend(naukri_jobs)

    # 2. Scrape Indeed Jobs
    with st.spinner('Scraping Indeed...'):
        indeed_jobs = scrape_indeed_jobs(role)
    st.info(f"✅ Found {len(indeed_jobs)} jobs from Indeed.com")
    all_jobs.extend(indeed_jobs)

    # 3. Scrape Internshala Jobs
    with st.spinner('Scraping Internshala...'):
        internshala_jobs = scrape_internshala_jobs(role)
    st.info(f"✅ Found {len(internshala_jobs)} jobs from Internshala.com")
    all_jobs.extend(internshala_jobs)
    
    # Shuffle the list so the job sources are mixed when displayed
    import random
    random.shuffle(all_jobs)
    
    return all_jobs