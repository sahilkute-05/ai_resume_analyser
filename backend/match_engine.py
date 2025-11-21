# backend/match_engine.py (Updated for Text Preprocessing)

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def compute_match(jd_text, resume_text):
    
    # Initialize TfidfVectorizer with Stop Word Removal.
    # 'english' tells the vectorizer to ignore common English filler words 
    # (like 'a', 'the', 'is', 'of'), which significantly improves the matching accuracy.
    vectorizer = TfidfVectorizer(stop_words='english')
    
    # Fit and transform the two documents (resume and job description)
    vectors = vectorizer.fit_transform([resume_text, jd_text])
    
    # Compute the cosine similarity between the two vectors
    similarity = cosine_similarity(vectors[0:1], vectors[1:2])[0][0]
    
    # Return similarity as a percentage
    return round(similarity * 100, 2)