import requests
from bs4 import BeautifulSoup
from requests.exceptions import RequestException
import streamlit as st 
import re # Added for potential cleanup, though not used in simple example

def scrape_naukri_jobs(role):
    url = f"https://www.naukri.com/{role}-jobs"
    jobs = []
    
    st.info(f"Attempting to scrape jobs from: {url}")
    
    # 1. Network Level Error Handling
    try:
        # Added timeout and error check for bad status codes
        response = requests.get(url, timeout=15) 
        response.raise_for_status() 
        html = response.text
    except RequestException as e:
        # Display an error gracefully in the Streamlit app
        st.error(f"Failed to fetch jobs from Naukri. Check your connection or the URL structure. Error: {e}")
        return [] # Return empty list on failure

    soup = BeautifulSoup(html, "html.parser")

    # Find the main job list container articles (this selector might need refinement)
    # Using a common class selector for better targeting
    job_articles = soup.find_all("article", class_=re.compile(r"jobTuple|srp_tuple"))[:10]
    
    if not job_articles:
        st.warning(f"Could not find any job articles for role: '{role}'. Try a different search term.")
        return []

    for job in job_articles:
        # 2. Parsing Level Error Handling (Per Job)
        try:
            # --- Essential Fields ---
            # Title: Using common class names for Title
            title_tag = job.find("a", class_="title") or job.find("a") 
            title = title_tag.text.strip()
            link = title_tag["href"]
            
            # --- Additional Requested Fields ---
            
            # Company Name: Using common class selector
            company_tag = job.find("a", class_="comp-name")
            company = company_tag.text.strip() if company_tag else "N/A"
            
            # Find all sub-details (Experience, Location, Salary) in one go
            sub_details = job.find_all("li", class_="fleft") 
            
            experience = "N/A"
            location = "N/A"
            salary = "N/A"
            
            # Parse the sub-details list
            for detail in sub_details:
                text = detail.text.strip()
                if "Yrs" in text or "year" in text:
                    experience = text
                elif "location" in str(detail).lower(): # Generic check for location span
                    location = text
                elif "lakh" in text.lower() or "k" in text.lower() or "salary" in str(detail).lower():
                    salary = text
            
            # Posted Date: Looking for common tag/class for posted time
            posted_tag = job.find("span", class_="postTime")
            posted_on = posted_tag.text.strip() if posted_tag else "N/A"
            
            # Job Description Snippet (using the entire article text as a fallback)
            description = job.text.strip()

            jobs.append({
                "title": title,
                "link": link,
                "description": description, # This is the full snippet used for match score
                "company": company,
                "experience": experience,
                "location": location,
                "salary": salary,
                "posted_on": posted_on,
            })
        except Exception:
            # Fail silently for individual bad job postings
            pass

    return jobs