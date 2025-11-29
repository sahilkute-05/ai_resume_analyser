# backend/job_scraper.py

import streamlit as st
from backend.job_scrapers.api_scraper import scrape_api_jobs 
import random

def scrape_all_jobs(role):
    all_jobs = []

    st.subheader("🌐 Fetching Jobs via JSearch API...")

    with st.spinner('Requesting data from JSearch...'):
        api_jobs = scrape_api_jobs(role)
    st.info(f"✅ Found {len(api_jobs)} jobs from JSearch API.")
    all_jobs.extend(api_jobs)
    
    random.shuffle(all_jobs)
    
    return all_jobs