# backend/job_scrapers/indeed_scraper.py

import requests
from bs4 import BeautifulSoup
from requests.exceptions import RequestException
import streamlit as st

def scrape_indeed_jobs(role):
    # Indeed URL structure is typically: /jobs?q=role
    url = f"https://in.indeed.com/jobs?q={role.replace(' ', '+')}"
    jobs = []
    
    # Common headers to avoid being immediately blocked
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
    except RequestException as e:
        st.error(f"Indeed Scraper Failed: {e}")
        return []

    # Indeed job card elements use class names like 'jobCard' or similar dynamic classes
    # We will target the <li> element that holds a single job listing
    job_cards = soup.find_all('li', class_={'css-5lfssm', 'eu4oa1a0'})[:10]

    for card in job_cards:
        try:
            # --- Essential Fields ---
            # Title & Link (often within a h2 or a tag)
            title_tag = card.find('h2').find('a') if card.find('h2') else card.find('a', id=lambda x: x and x.startswith('job_'))
            if not title_tag: continue
                
            title = title_tag.text.strip()
            link = "https://in.indeed.com" + title_tag.get('href', '')
            
            # --- Additional Requested Fields ---
            
            # Company Name
            company_tag = card.find('span', class_='companyName')
            company = company_tag.text.strip() if company_tag else "N/A"
            
            # Location
            location_tag = card.find('div', class_='companyLocation')
            location = location_tag.text.strip() if location_tag else "N/A"
            
            # Salary (highly variable, using common class)
            salary_tag = card.find('div', class_='salary-snippet') or card.find('span', class_='estimated-salary')
            salary = salary_tag.text.strip() if salary_tag else "N/A"
            
            # Posted Date (using common class)
            posted_tag = card.find('span', class_='date')
            posted_on = posted_tag.text.strip() if posted_tag else "N/A"
            
            # Experience (often not directly available on search page, set to N/A)
            experience = "N/A"

            # Job Description Snippet (using the main text of the card for matching)
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
                "source": "Indeed",
            })
        except Exception:
            pass
            
    return jobs