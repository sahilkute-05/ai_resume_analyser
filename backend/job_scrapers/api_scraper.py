# backend/job_scrapers/api_scraper.py (FINAL, STABLE VERSION)

import requests
import streamlit as st
import json
import re
import os # CRITICAL: For accessing environment variables
from requests.exceptions import RequestException
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
try:
    from llm_matcher import extract_job_details_llm
except ImportError:
    # Fallback if import fails (e.g. path issues)
    def extract_job_details_llm(desc): return None

# --- CONSTANTS FOR FALLBACK ---
METRO_CITIES = [
    "Mumbai", "Delhi", "Bangalore", "Hyderabad", "Ahmedabad", 
    "Chennai", "Kolkata", "Pune", "Gurgaon", "Noida", "Coimbatore"
]

LOCATION_LABELS = [
    "Job Location", "Work Location", "City", "Place", "Address", "On-site Location",
    "Workplace Type", "Work Type", "Location Type", "Work Mode", "Remote", "Hybrid", 
    "On-site", "Preferred Location", "Internship Location", "Work from home"
]

# --- HELPER FUNCTIONS ---

def extract_exp_from_text(description):
    """Searches job description text for common experience patterns."""
    # Improved regex to handle "to" (e.g., "0 to 4 Yrs")
    match = re.search(r'(\d[-+]?\s*(?:-|to)\s*\d|\d+)\s*(?:years|yrs|year|Yr|exp)', description, re.IGNORECASE)
    if match:
        return match.group(0).strip()
    return "N/A"

def extract_metro_location(text):
    """Searches text for major city names."""
    for city in METRO_CITIES:
        if re.search(r'\b' + re.escape(city) + r'\b', text, re.IGNORECASE):
            return city
    return "N/A"

def extract_labeled_location(text):
    """Searches text for explicit location labels."""
    sorted_labels = sorted(LOCATION_LABELS, key=len, reverse=True)
    pattern = r'(' + '|'.join([re.escape(label) for label in sorted_labels]) + r')\s*[:\s]\s*([a-zA-Z\s]{5,25})'
    
    match = re.search(pattern, text, re.IGNORECASE)
    if match:
        result = match.group(2).strip()
        if len(result.split()) <= 4 and result.lower() not in ["requirements", "responsibilities", "experience", "qualifications"]:
            return result
    return "N/A"


# --- MAIN SCRAPING FUNCTION ---
def scrape_api_jobs(role):
    
    # CRITICAL FIX: Prioritize direct OS environment check for deployment reliability
    # The key is stored as an environment variable (best practice)
    rapidapi_key = os.environ.get("RAPIDAPI_API_KEY_LITERAL")
    
    if not rapidapi_key:
        # Fallback 1: Check if the key was set via the simpler st.secrets method
        try:
            rapidapi_key = st.secrets["RAPIDAPI_API_KEY_LITERAL"]
        except KeyError:
            st.error("Error: RAPIDAPI key not found. Please set RAPIDAPI_API_KEY_LITERAL as an Environment Variable in your cloud host or in st.secrets.")
            return []

    url = "https://jsearch.p.rapidapi.com/search"

    querystring = {
        "query": role,
        "num_pages": "1",
        "date_posted": "week",
        "country": "IN"
    }

    # Authentication headers use the retrieved environment key
    headers = {
        "X-RapidAPI-Key": rapidapi_key,
        "X-RapidAPI-Host": "jsearch.p.rapidapi.com"
    }

    jobs = []

    try:
        response = requests.get(url, headers=headers, params=querystring, timeout=15)
        response.raise_for_status() 
        data = response.json()

        if data.get("status") == "OK" and data.get("data"):
            for job_data in data["data"][:10]:
                
                job_description = job_data.get("job_description", "")
                job_title = job_data.get("job_title", "")
                full_search_text = job_title + " " + job_description
                
                
                # --- EXPERIENCE EXTRACTION ---
                experience_api = job_data.get("job_required_experience", "N/A")
                
                if experience_api in ["N/A", "", None]:
                    experience_final = extract_exp_from_text(job_description)
                else:
                    experience_final = experience_api
                
                
                # --- LOCATION EXTRACTION ---
                # Fix: Handle None explicitly to avoid "None" string
                city_val = job_data.get("job_city")
                state_val = job_data.get("job_state")
                
                city = str(city_val).strip() if city_val else "N/A"
                state = str(state_val).strip() if state_val else "N/A"
                
                location_components = [c for c in [city, state] if c and c.upper() not in ["N/A", "NONE"]]
                primary_location = ", ".join(location_components) or "N/A"
                
                location_final = primary_location
                
                if primary_location == "N/A":
                    job_title = job_data.get("job_title", "")
                    full_search_text = job_title + " " + job_description
                    
                    labeled_location = extract_labeled_location(full_search_text)
                    if labeled_location != "N/A":
                        location_final = labeled_location
                    else:
                        location_final = extract_metro_location(full_search_text)

                # --- LLM FALLBACK FOR MISSING DATA ---
                # Check for various forms of missing data
                is_exp_missing = experience_final in ["N/A", "None", ""]
                is_loc_missing = location_final in ["N/A", "None", "None, None", ""]
                
                if is_exp_missing or is_loc_missing:
                    llm_data = extract_job_details_llm(job_description)
                    if llm_data:
                        if is_exp_missing:
                            experience_final = llm_data.get("EXPERIENCE", "N/A")
                        if is_loc_missing:
                            location_final = llm_data.get("LOCATION", "N/A")

                # --- APPEND JOB DATA ---
                jobs.append({
                    "title": job_data.get("job_title", "N/A"),
                    "link": job_data.get("job_apply_link", "#"), 
                    "description": job_data.get("job_description", "N/A"), 
                    "company": job_data.get("employer_name", "N/A"),
                    "experience": experience_final,
                    "location": location_final,
                    "salary": job_data.get("job_salary", "N/A"),
                    "posted_on": str(job_data.get("job_posted_at_datetime_utc", "N/A"))[:10],
                    "source": "JSearch API",
                })
            return jobs
        else:
            st.error(f"API Error: {data.get('message', 'No data or error message returned.')}")
            return []

    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 401:
            st.error("API Request Failed (401 Unauthorized): Check your RapidAPI Key validity or Quota.")
        else:
            st.error(f"API Request Failed (Network/Timeout): {e}")
        return []
    except Exception as e:
        st.error(f"An unexpected error occurred during API call: {e}")
        return []