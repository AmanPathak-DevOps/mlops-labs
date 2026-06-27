import os
import joblib
import pandas as pd

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline

# Load dataset from CSV
data_path = os.path.join(os.path.dirname(__file__), "data", "training_data.csv")
df = pd.read_csv(data_path)

X = df["text"].str.lower().tolist()
y = df["intent"].tolist()

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

print("Model trained successfully")
