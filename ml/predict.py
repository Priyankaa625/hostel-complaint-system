import joblib
import os

# Load model and vectorizer
model_path = os.path.join(os.path.dirname(__file__), 'complaint_model.pkl')
vectorizer_path = os.path.join(os.path.dirname(__file__), 'vectorizer.pkl')

try:
    model = joblib.load(model_path)
    vectorizer = joblib.load(vectorizer_path)
    print("✅ ML Model loaded successfully")
except:
    model = None
    vectorizer = None
    print("⚠️ ML Model not found. Please run: python ml/train_model.py")

def predict_category_and_priority(description):
    """
    Predict category and priority based on complaint description
    """
    # Default values if model not loaded
    if model is None or vectorizer is None:
        category = 'Other'
        priority = 'Medium'
    else:
        # Predict category
        description_vectorized = vectorizer.transform([description.lower()])
        category = model.predict(description_vectorized)[0]
    
    # Determine priority based on keywords
    description_lower = description.lower()
    high_priority_keywords = ['leak', 'broken', 'emergency', 'urgent', 'fire', 'electric shock', 'burst']
    low_priority_keywords = ['minor', 'cosmetic', 'aesthetic', 'small']
    
    if any(keyword in description_lower for keyword in high_priority_keywords):
        priority = 'High'
    elif any(keyword in description_lower for keyword in low_priority_keywords):
        priority = 'Low'
    else:
        priority = 'Medium'
    
    return category, priority