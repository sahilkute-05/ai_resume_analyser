import pdfplumber
import re
import json
import os 

def load_keywords():
    keyword_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data', 'keywords.json')

    try:
        with open(keyword_path, 'r') as f:
            data = json.load(f)
            # Combine all skills from all categories into one flat list for extraction
            all_skills = []
            for category in data.values():
                all_skills.extend(category)
            return all_skills
    except FileNotFoundError:
        print(f"Error: Keyword file not found at {keyword_path}")
        return [] # Return empty list on failure
    
ALL_SKILLS = load_keywords()



def extract_text_from_pdf(uploaded_file):
    text = ""
    with pdfplumber.open(uploaded_file) as pdf:
        for page in pdf.pages:
            text += page.extract_text() + "\n"
    return text

def extract_skills(text):
    text = text.lower()
    found = []
    for skill in SKILLS:
        if skill in text:
            found.append(skill)
    return found
