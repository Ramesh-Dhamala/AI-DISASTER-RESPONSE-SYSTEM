import joblib
import os
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier

print("🔄 Training Disaster Response Model...")
print("-" * 40)

# Training data
training_data = [
    ("earthquake shaking buildings collapse rescue trapped", "earthquake"),
    ("strong tremors felt evacuate immediately", "earthquake"),
    ("flood waters rising need boat rescue", "flood"),
    ("heavy rainfall causing flooding in streets", "flood"),
    ("hurricane strong winds approaching coast", "hurricane"),
    ("cyclone alert evacuate coastal areas", "hurricane"),
    ("wildfire spreading rapidly evacuate zone", "wildfire"),
    ("forest fire smoke dangerous air quality", "wildfire"),
    ("tornado warning seek shelter basement", "tornado"),
    ("twister spotted moving east take cover", "tornado"),
    ("tsunami warning coastal evacuation ordered", "tsunami"),
    ("giant waves approaching shore go to high ground", "tsunami"),
    ("volcano eruption ash cloud falling", "volcano"),
    ("lava flow approaching residential area", "volcano"),
    ("landslide blocking highway need assistance", "landslide"),
    ("mudslide destroying homes rescue needed", "landslide"),
    ("normal weather sunny day no issues", "normal"),
    ("routine traffic update highway clear", "normal"),
]

# Separate messages and labels
messages = [item[0] for item in training_data]
labels = [item[1] for item in training_data]

# Create and train vectorizer
print("📊 Vectorizing text data...")
vectorizer = TfidfVectorizer(max_features=100, stop_words='english')
X = vectorizer.fit_transform(messages)

# Train model
print("🤖 Training Random Forest classifier...")
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X, labels)

# Create directory if it doesn't exist
os.makedirs('models/saved', exist_ok=True)

# Save model and vectorizer
print("💾 Saving model files...")
joblib.dump(model, 'models/saved/disaster_model.pkl')
joblib.dump(vectorizer, 'models/saved/vectorizer.pkl')

print("\n✅ Model training completed!")
print(f"📁 Model saved to: models/saved/disaster_model.pkl")
print(f"📁 Vectorizer saved to: models/saved/vectorizer.pkl")
print(f"📊 Training samples: {len(messages)}")
print(f"🏷️  Disaster types: {set(labels)}")

# Test the model
print("\n🧪 Testing model with sample inputs:")
test_messages = [
    "earthquake help building collapsed",
    "flood water rising need rescue",
    "how is the weather today"
]

for msg in test_messages:
    X_test = vectorizer.transform([msg])
    pred = model.predict(X_test)[0]
    print(f"  Input: '{msg}'")
    print(f"  Prediction: {pred}\n")

print("="*40)
print("🎯 Model ready for use!")
print("   Start backend: python main.py")
print("   Test prediction: python test_api.py")
