# backend/llm_matcher.py (FINAL, OPENROUTER STABLE VERSION)

import requests
import streamlit as st
import json
import re
from requests.exceptions import RequestException

# --- 1. THE CORE RECRUITER PROMPT ---
def get_recruiter_prompt(resume_text, jd_text, user_seniority):
    """Generates the detailed system prompt for human-like analysis."""
    return f"""
    You are an Expert Senior Recruiter (Level 10) specializing in global tech roles. 
    Your task is to analyze the candidate's ENTIRE resume profile against the job description (JD).
    
    --- ANALYSIS INSTRUCTIONS ---
    1. DETERMINE SENIORITY: Based on the entire resume, classify the candidate as one of: Fresher/Intern (0-1 yr), Entry-Level (1-3 yrs), Mid-Level (3-7 yrs), or Senior/Lead (7+ yrs).
    2. CALCULATE SCORE: Calculate the overall Match Score from 0 to 100. Seniority mismatch MUST heavily penalize the score (e.g., a candidate estimated as {user_seniority} matched against a Senior Lead role should score low).
    3. IDENTIFY CORE DATA: Identify the Top 5 most critical technical skills shared by both documents and the Top 5 most critical skills missing from the resume but required by the JD.

    Your response must ONLY be the requested JSON structure. Do NOT include any additional text or markdown formatting outside of the JSON block.

    --- DATA ---
    CANDIDATE'S ESTIMATED SENIORITY: {user_seniority}
    RESUME: 
    {resume_text}

    JOB DESCRIPTION: 
    {jd_text}

    --- OUTPUT FORMAT ---
    {{
        "SENIORITY_ESTIMATE": "Fresher/Intern | Entry-Level | Mid-Level | Senior/Lead",
        "SCORE": [0-100],
        "SUMMARY": "Brief (1-sentence) explanation of the match focusing on seniority and core alignment.",
        "SHARED_SKILLS": ["skill1", "skill2", "..."],
        "MISSING_SKILLS": ["skill1", "skill2", "..."]
    }}
    """

# --- 2. API CALL FUNCTION (Reliable HTTP Request with OpenRouter) ---
def analyze_and_match_llm(resume_text, jd_text, user_seniority):
    
    # CRITICAL FIX: Access the flat key name set in Streamlit Secrets
    try:
        openrouter_key = st.secrets["openrouter"]["api_key"]
    except KeyError:
        st.error("Error: OpenRouter API key not found in secrets. Please verify OPENROUTER_KEY is set in Streamlit Secrets.")
        return None

    prompt = get_recruiter_prompt(resume_text, jd_text, user_seniority)
    
    # OpenRouter API Endpoint (Standard OpenAI-compatible format)
    API_URL = "https://openrouter.ai/api/v1/chat/completions"
    
    # Define Model and Authentication
    headers = {
        "Authorization": f"Bearer {openrouter_key}",
        "Content-Type": "application/json"
    }

    payload = {
        # Using a reliable, fast, free or very low-cost Mistral model via OpenRouter
        "model": "mistralai/mistral-7b-instruct:free", 
        "messages": [
            {"role": "system", "content": "You are a specialized AI designed to output only the requested JSON structure."},
            {"role": "user", "content": prompt}
        ],
        "response_format": {"type": "json_object"},
        "temperature": 0.1,
        "max_tokens": 1000
    }
    
    try:
        st.caption("🤖 Analyzing profile with OpenRouter (Mistral 7B)...")
        
        response = requests.post(API_URL, headers=headers, json=payload, timeout=60)
        response.raise_for_status() # Raise HTTPError for bad statuses
        
        # Get the response content
        result_text = response.json()['choices'][0]['message']['content']
        
        # Parse the structured JSON output
        return json.loads(result_text)
        
    except requests.exceptions.HTTPError as e:
        # Catches 401 Unauthorized (invalid key) or other network errors
        st.error(f"OpenRouter API Error (Status {e.response.status_code}): Check API Key or Quota.")
        return None
    except Exception as e:
        st.error(f"Failed to parse LLM response: {e}")
        return None

# --- 3. HELPER: LLM EXTRACTION FOR SCRAPER ---
def extract_job_details_llm(job_description):
    """
    Uses LLM to extract 'Experience' and 'Location' from a job description 
    when regex fails.
    """
    try:
        openrouter_key = st.secrets["openrouter"]["api_key"]
    except KeyError:
        return None

    prompt = f"""
    You are a data extraction assistant. Extract the following fields from the Job Description below:
    1. EXPERIENCE: The required experience range (e.g., "0-2 years", "3+ years"). If not found, return "N/A".
    2. LOCATION: The job location (e.g., "Bangalore", "Remote", "All India"). If not found, return "N/A".

    JOB DESCRIPTION:
    {job_description[:3000]}  # Truncate to avoid token limits

    OUTPUT FORMAT (JSON ONLY):
    {{
        "EXPERIENCE": "extracted value",
        "LOCATION": "extracted value"
    }}
    """

    API_URL = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {openrouter_key}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "mistralai/mistral-7b-instruct:free",
        "messages": [{"role": "user", "content": prompt}],
        "response_format": {"type": "json_object"},
        "temperature": 0.1
    }

    try:
        response = requests.post(API_URL, headers=headers, json=payload, timeout=10)
        if response.status_code == 200:
            data = response.json()['choices'][0]['message']['content']
            return json.loads(data)
    except Exception:
        pass
    
    return None

# --- 4. HELPER: DETECT CANDIDATE SENIORITY (OPTIMIZED) ---
def detect_candidate_seniority(resume_text):
    """
    Uses LLM to intelligently analyze the resume and determine the candidate's 
    seniority level: Fresher/Intern, Entry-Level, Mid-Level, or Senior/Lead.
    
    Falls back to regex-based detection if LLM fails or times out.
    """
    try:
        openrouter_key = st.secrets["openrouter"]["api_key"]
    except KeyError:
        st.warning("⚠️ OpenRouter API key not found. Using fallback detection.")
        return _fallback_seniority_detection(resume_text)

    # Simplified, faster prompt
    prompt = f"""Analyze this resume and classify seniority level.

RULES:
- Fresher/Intern: 0-1 yrs, student/recent grad
- Entry-Level: 1-3 yrs, junior roles
- Mid-Level: 3-7 yrs, intermediate roles
- Senior/Lead: 7+ yrs, senior/lead roles

RESUME (first 2500 chars):
{resume_text[:2500]}

Return ONLY this JSON:
{{"SENIORITY_LEVEL": "Fresher/Intern|Entry-Level|Mid-Level|Senior/Lead", "REASONING": "1 sentence"}}"""

    API_URL = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {openrouter_key}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "mistralai/mistral-7b-instruct:free",
        "messages": [{"role": "user", "content": prompt}],
        "response_format": {"type": "json_object"},
        "temperature": 0.0,  # More deterministic
        "max_tokens": 150    # Reduced for faster response
    }

    try:
        with st.spinner("🔍 Detecting seniority level..."):
            response = requests.post(API_URL, headers=headers, json=payload, timeout=30)
            
            if response.status_code == 200:
                data = response.json()['choices'][0]['message']['content']
                result = json.loads(data)
                seniority = result.get("SENIORITY_LEVEL", "Unknown")
                reasoning = result.get("REASONING", "")
                
                st.success(f"✅ Seniority: **{seniority}**")
                if reasoning:
                    st.caption(f"💡 {reasoning}")
                return seniority
            else:
                st.warning(f"⚠️ LLM API returned status {response.status_code}. Using fallback detection.")
                return _fallback_seniority_detection(resume_text)
                
    except requests.exceptions.Timeout:
        st.warning("⏱️ LLM request timed out. Using quick fallback detection.")
        return _fallback_seniority_detection(resume_text)
    except Exception as e:
        st.warning(f"⚠️ LLM detection failed. Using fallback.")
        return _fallback_seniority_detection(resume_text)

def _fallback_seniority_detection(resume_text):
    """
    Fast regex-based fallback for seniority detection when LLM is unavailable.
    """
    st.info("⚡ Using quick pattern-based detection...")
    text_lower = resume_text.lower()
    
    # Check for student/intern keywords
    if any(word in text_lower for word in ['student', 'pursuing', 'undergraduate', 'intern', 'internship']):
        st.success("✅ Seniority: **Fresher/Intern**")
        st.caption("💡 Detected student/intern keywords")
        return "Fresher/Intern"
    
    # Check for senior keywords
    if any(word in text_lower for word in ['senior', 'lead', 'principal', 'architect', 'manager', 'head of', 'director']):
        # But verify they have substantial experience
        exp_patterns = [r'(\d+)\+?\s*years?', r'(\d+)\+?\s*yrs?']
        for pattern in exp_patterns:
            matches = re.findall(pattern, text_lower)
            if matches:
                max_years = max([int(m) for m in matches])
                if max_years >= 7:
                    st.success("✅ Seniority: **Senior/Lead**")
                    st.caption(f"💡 Detected {max_years}+ years experience with senior title")
                    return "Senior/Lead"
                elif max_years >= 3:
                    st.success("✅ Seniority: **Mid-Level**")
                    st.caption(f"💡 Detected {max_years} years experience")
                    return "Mid-Level"
                elif max_years >= 1:
                    st.success("✅ Seniority: **Entry-Level**")
                    st.caption(f"💡 Detected {max_years} years experience")
                    return "Entry-Level"
        st.success("✅ Seniority: **Mid-Level**")
        st.caption("💡 Detected senior title")
        return "Mid-Level"
    
    # Check for experience years mentioned
    exp_patterns = [r'(\d+)\+?\s*years?\s+(?:of\s+)?experience', r'experience.*?(\d+)\+?\s*years?']
    for pattern in exp_patterns:
        matches = re.findall(pattern, text_lower)
        if matches:
            max_years = max([int(m) for m in matches])
            if max_years >= 7:
                st.success("✅ Seniority: **Senior/Lead**")
                st.caption(f"💡 Detected {max_years}+ years experience")
                return "Senior/Lead"
            elif max_years >= 3:
                st.success("✅ Seniority: **Mid-Level**")
                st.caption(f"💡 Detected {max_years} years experience")
                return "Mid-Level"
            elif max_years >= 1:
                st.success("✅ Seniority: **Entry-Level**")
                st.caption(f"💡 Detected {max_years} year(s) experience")
                return "Entry-Level"
            else:
                st.success("✅ Seniority: **Fresher/Intern**")
                st.caption(f"💡 Detected less than 1 year experience")
                return "Fresher/Intern"
    
    # Check for fresh graduate indicators
    if any(word in text_lower for word in ['recent graduate', 'fresh graduate', 'graduated 202']):
        st.success("✅ Seniority: **Fresher/Intern**")
        st.caption("💡 Detected recent graduate")
        return "Fresher/Intern"
    
    # Default to Entry-Level if unclear
    st.success("✅ Seniority: **Entry-Level**")
    st.caption("💡 Default classification (no clear indicators found)")
    return "Entry-Level"