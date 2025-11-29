# 🤖 AI Resume Analyzer + Job Matcher

An intelligent AI-powered application that analyzes resumes, calculates ATS scores, detects candidate seniority levels, and matches candidates with relevant job opportunities using advanced LLM technology.

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)

## ✨ Features

### 📄 Resume Analysis
- **PDF Text Extraction**: Extracts and displays resume content from PDF files
- **Skills Detection**: Automatically identifies technical and professional skills
- **ATS Score Calculation**: Evaluates resume compatibility with Applicant Tracking Systems
- **Intelligent Seniority Detection**: Uses LLM to classify candidates as:
  - Fresher/Intern (0-1 years)
  - Entry-Level (1-3 years)
  - Mid-Level (3-7 years)
  - Senior/Lead (7+ years)

### 💼 Job Matching
- **Live Job Scraping**: Fetches real-time job postings from JSearch API
- **AI-Powered Matching**: Uses Mistral 7B LLM via OpenRouter for intelligent job-resume matching
- **Match Score Calculation**: Provides 0-100 compatibility scores
- **Skills Analysis**: Identifies shared skills and missing requirements
- **Seniority Alignment**: Considers candidate level for better job recommendations

### 📊 ATS Optimization
- **Detailed Scoring**: Comprehensive ATS compatibility analysis
- **Improvement Suggestions**: Actionable recommendations to enhance resume quality
- **Keyword Analysis**: Identifies important keywords and their presence

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- OpenRouter API key (for LLM features)
- JSearch API key (for job scraping)

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/sahilkute-05/ai_resume_analyser.git
cd ai_resume_analyser
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Set up API keys**

Create a `.streamlit/secrets.toml` file in the project root:

```toml
[openrouter]
api_key = "your_openrouter_api_key_here"

[jsearch]
api_key = "your_jsearch_api_key_here"
```

**Getting API Keys:**
- **OpenRouter**: Sign up at [openrouter.ai](https://openrouter.ai/) and get your API key
- **JSearch**: Get your API key from [RapidAPI JSearch](https://rapidapi.com/letscrape-6bRBa3QguO5/api/jsearch)

4. **Run the application**
```bash
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`

## 📖 Usage

### 1. Resume Analysis
1. Navigate to **📄 Resume Analyzer** in the sidebar
2. Upload your resume (PDF format)
3. View extracted text, detected skills, and seniority level
4. Check your ATS score and get improvement suggestions

### 2. Job Matching
1. First, analyze your resume in the Resume Analyzer
2. Navigate to **💼 Job Matcher** in the sidebar
3. Enter your target job role (e.g., "Data Scientist", "ML Engineer")
4. View matched jobs sorted by compatibility score
5. See shared skills, missing requirements, and seniority alignment

### 3. ATS Score & Suggestions
1. After analyzing your resume, navigate to **📊 ATS Score**
2. View your detailed ATS compatibility score
3. Navigate to **💡 Suggestions** for improvement recommendations

## 🏗️ Project Structure

```
ai_resume_analyser/
├── app.py                          # Main Streamlit application
├── pages/
│   ├── Resume_Analyzer.py          # Resume upload and analysis
│   ├── Job_Matcher.py              # Job matching interface
│   ├── ATS_Score.py                # ATS score display
│   └── Suggestions.py              # Improvement suggestions
├── backend/
│   ├── resume_parser.py            # PDF parsing and skill extraction
│   ├── ats_engine.py               # ATS score calculation
│   ├── llm_matcher.py              # LLM-based matching and seniority detection
│   ├── job_scraper.py              # Job scraping orchestration
│   └── job_scrapers/
│       └── api_scraper.py          # JSearch API integration
├── .streamlit/
│   └── secrets.toml                # API keys (not in repo)
└── requirements.txt                # Python dependencies
```

## 🔧 Technology Stack

- **Frontend**: Streamlit
- **PDF Processing**: pdfplumber
- **LLM**: Mistral 7B (via OpenRouter)
- **Job API**: JSearch API (RapidAPI)
- **Text Processing**: spaCy, NLTK
- **HTTP Requests**: requests

## 🧠 How It Works

### Seniority Detection
1. **Primary Method (LLM)**: Analyzes resume using Mistral 7B for intelligent classification
2. **Fallback Method (Regex)**: Pattern matching for keywords and experience years when LLM is unavailable
3. **Classification Criteria**:
   - Years of experience
   - Education level and status
   - Job titles and role levels
   - Project complexity
   - Leadership experience

### Job Matching Algorithm
1. Fetches live jobs from JSearch API
2. Sends resume + job description to LLM
3. LLM analyzes:
   - Skill overlap
   - Seniority alignment
   - Experience relevance
   - Overall compatibility
4. Returns match score (0-100) with detailed reasoning

## 🎯 Key Features Explained

### Intelligent Seniority Detection
- **Fast Processing**: Optimized prompts (2500 chars) for quick responses
- **Reliable Fallback**: Regex-based detection when LLM times out
- **Visual Feedback**: Clear reasoning for classification
- **Accurate Classification**: Considers multiple factors for precise leveling

### ATS Score Calculation
- Analyzes resume structure and formatting
- Checks for essential sections (contact, experience, education, skills)
- Evaluates keyword presence and density
- Provides actionable improvement suggestions

### Job Matching
- Real-time job data from JSearch API
- Intelligent location and experience extraction
- Seniority-aware matching (penalizes mismatches)
- Detailed skill gap analysis

## 🔐 Security Notes

- Never commit your `secrets.toml` file to version control
- Keep your API keys secure and rotate them regularly
- The `.gitignore` file already excludes sensitive files

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🐛 Known Issues & Limitations

- LLM requests may occasionally timeout (fallback detection activates automatically)
- Free tier API limits may restrict usage
- PDF extraction quality depends on PDF structure

## 🚧 Future Enhancements

- [ ] Support for more resume formats (DOCX, TXT)
- [ ] Multiple LLM provider support
- [ ] Resume builder/editor
- [ ] Job application tracking
- [ ] Email notifications for new matching jobs
- [ ] Resume comparison tool
- [ ] Interview preparation suggestions

## 📧 Contact

**Sahil Kute** - [@sahilkute-05](https://github.com/sahilkute-05)

Project Link: [https://github.com/sahilkute-05/ai_resume_analyser](https://github.com/sahilkute-05/ai_resume_analyser)

## 🙏 Acknowledgments

- [Streamlit](https://streamlit.io/) for the amazing web framework
- [OpenRouter](https://openrouter.ai/) for LLM API access
- [JSearch API](https://rapidapi.com/letscrape-6bRBa3QguO5/api/jsearch) for job data
- [Mistral AI](https://mistral.ai/) for the powerful language model

---

⭐ If you found this project helpful, please consider giving it a star!
