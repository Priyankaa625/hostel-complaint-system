import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
import joblib
import os

# Sample training data
data = {
    'description': [
        'water leaking from tap', 'bathroom tap broken', 'sink overflow water',
        'light not working', 'fan stopped', 'power socket broken', 'bulb fused',
        'food quality poor', 'stale food', 'undercooked rice', 'cold food served',
        'room not cleaned', 'dusty floor', 'garbage not collected', 'toilet dirty',
        'door lock broken', 'window pane cracked', 'bed broken', 'chair damaged',
        'water pipe burst', 'tap dripping', 'shower not working',
        'switch not working', 'wiring issue', 'no electricity',
        'food taste bad', 'expired food', 'unhygienic food',
        'floor dirty', 'bathroom smells', 'waste not removed',
        'furniture damaged', 'door hinge loose', 'window stuck'
    ],
    'category': [
        'Plumbing', 'Plumbing', 'Plumbing',
        'Electrical', 'Electrical', 'Electrical', 'Electrical',
        'Food', 'Food', 'Food', 'Food',
        'Cleanliness', 'Cleanliness', 'Cleanliness', 'Cleanliness',
        'Maintenance', 'Maintenance', 'Maintenance', 'Maintenance',
        'Plumbing', 'Plumbing', 'Plumbing',
        'Electrical', 'Electrical', 'Electrical',
        'Food', 'Food', 'Food',
        'Cleanliness', 'Cleanliness', 'Cleanliness',
        'Maintenance', 'Maintenance', 'Maintenance'
    ]
}

df = pd.DataFrame(data)

# Vectorization
print("Training ML Model...")
vectorizer = TfidfVectorizer(max_features=100, stop_words='english')
X = vectorizer.fit_transform(df['description'])
y = df['category']

# Train model
model = MultinomialNB()
model.fit(X, y)

# Create ml directory if it doesn't exist
os.makedirs('ml', exist_ok=True)

# Save model and vectorizer
joblib.dump(model, 'ml/complaint_model.pkl')
joblib.dump(vectorizer, 'ml/vectorizer.pkl')

print("✅ Model trained and saved successfully!")
print(f"📊 Training Accuracy: {model.score(X, y) * 100:.2f}%")