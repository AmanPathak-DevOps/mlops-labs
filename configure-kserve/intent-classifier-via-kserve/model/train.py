import os
import joblib
import random

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline

# Expanded training dataset

training_data = {
    "greeting": [
        "hi",
        "hello",
        "hey",
        "good morning",
        "good evening",
        "hey there",
        "how are you",
        "yo",
        "hii",
        "hola",
        "namaste",
        "what's up",
        "good afternoon",
        "hello team",
        "hi support",
        "greetings",
        "hey buddy",
        "hi there",
        "hello friend",
        "morning"
    ],

    "question": [
        "how to reset password",
        "how can i login",
        "where can i update profile",
        "how to change email",
        "can you help me",
        "how does billing work",
        "how to contact support",
        "where is my order",
        "how to track my shipment",
        "how to upgrade plan",
        "how to download invoice",
        "how to change username",
        "how do i unsubscribe",
        "where are settings",
        "can i change my password",
        "how to delete account",
        "how to install application",
        "how to configure account",
        "what is pricing",
        "where can i see dashboard"
    ],

    "complaint": [
        "cancel my subscription",
        "your service is bad",
        "very disappointed",
        "this is terrible",
        "application is slow",
        "i hate this app",
        "payment failed again",
        "website is broken",
        "not working properly",
        "service is unavailable",
        "i am frustrated",
        "worst support experience",
        "this issue is annoying",
        "login keeps failing",
        "dashboard is crashing",
        "too many bugs",
        "my account is locked",
        "refund my money",
        "i cannot access my account",
        "poor performance"
    ],

    "praise": [
        "great service",
        "awesome experience",
        "excellent support",
        "very helpful",
        "amazing product",
        "good job",
        "fantastic work",
        "love this platform",
        "really impressed",
        "best application",
        "wonderful service",
        "support was quick",
        "super fast response",
        "you solved my issue",
        "highly appreciated",
        "great customer support",
        "this app is awesome",
        "smooth experience",
        "very satisfied",
        "excellent platform"
    ]
}

# Build dataset
X = []
y = []

for intent, examples in training_data.items():
    for text in examples:
        X.append(text.lower())
        y.append(intent)

# Shuffle dataset
combined = list(zip(X, y))
random.shuffle(combined)

X, y = zip(*combined)

# ML pipeline
pipeline = Pipeline([
    (
        "vect",
        CountVectorizer(
            lowercase=True,
            stop_words="english",
            ngram_range=(1, 2)
        )
    ),
    ("clf", MultinomialNB())
])

# Train model
pipeline.fit(X, y)

# Save model artifact
os.makedirs("model/artifacts", exist_ok=True)

joblib.dump(
    pipeline,
    "model/artifacts/intent_model.pkl"
)

print("Model trained successfully 🚀")
