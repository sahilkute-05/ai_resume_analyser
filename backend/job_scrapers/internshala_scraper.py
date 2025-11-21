# backend/job_scrapers/internshala_scraper.py

import requests
from bs4 import BeautifulSoup
from requests.exceptions import RequestException
import streamlit as st

def scrape_internshala_jobs(role):
    # Internshala searches are often case-sensitive and need proper URL encoding
    url = f"https://internshala.com/internships/{role.lower().replace(' ', '-')}-internship"
    jobs = []

    try:
        response = requests.get(url, timeout=15)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
    except RequestException as e:
        st.error(f"Internshala Scraper Failed: {e}")
        return []

    # Targeting the main job cards <div>
    job_cards = soup.find_all('div', class_='individual_internship')[:10]

    for card in job_cards:
        try:
            # --- Essential Fields ---
            title_tag = card.find('a', class_='view_detail_link')
            if not title_tag: continue
            
            title = title_tag.text.strip()
            link = "https://internshala.com" + title_tag.get('href', '')
            
            # --- Additional Requested Fields ---
            
            # Company Name
            company_tag = card.find('a', class_='company_name')
            company = company_tag.text.strip() if company_tag else "N/A"
            
            # Find all stipend/location/duration details
            details_section = card.find('div', class_='internship_other_details')
            details_spans = details_section.find_all('span', class_='stipend')
            
            # Default values
            location = "N/A"
            salary = "N/A"
            
            # Location is often found outside the details box, or in a specific tag
            location_tag = card.find('a', class_='location_link')
            location = location_tag.text.strip() if location_tag else "N/A"
            
            # Stipend/Salary is usually the first span with a specific class
            salary = details_spans[0].text.strip() if details_spans else "N/A"

            # Posted Date (Often hard to find on the search page, default to N/A)
            posted_on = "N/A"
            experience = "N/A" # Internshala focuses on internships/fresher roles

            # Job Description Snippet
            description = card.text.strip()

            jobs.append({
                "title": title,
                "link": link,
                "description": description, 
                "company": company,
                "experience": experience,
                "location": location,
                "salary": salary,
                "posted_on": posted_on,
                "source": "Internshala",
            })
        except Exception:
            pass
            
    return jobs