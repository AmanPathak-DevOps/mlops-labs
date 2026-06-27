import os
import joblib
import pandas as pd

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline

# ---------------------------------------------------------------------------
# Path resolution — SageMaker vs local
#
# When SageMaker runs this script inside its training container it sets two
# environment variables:
#
#   SM_CHANNEL_TRAIN  →  /opt/ml/input/data/train
#       The directory where SageMaker has downloaded your S3 training data.
#       Put training_data.csv here when you upload to S3.
#
#   SM_MODEL_DIR      →  /opt/ml/model
#       Where your trained artefact must be saved.
#       After training finishes SageMaker tars everything in this folder
#       into model.tar.gz and uploads it back to S3 automatically.
#
# Locally neither variable is set, so we fall back to the paths that already
# work in the repo (model/data/ and model/artifacts/).
# ---------------------------------------------------------------------------

IS_SAGEMAKER = "SM_MODEL_DIR" in os.environ

if IS_SAGEMAKER:
    # SageMaker paths (inside /opt/ml/)
    data_dir  = os.environ["SM_CHANNEL_TRAIN"]          # /opt/ml/input/data/train
    model_dir = os.environ["SM_MODEL_DIR"]              # /opt/ml/model
else:
    # Local paths (relative to project root)
    data_dir  = os.path.join(os.path.dirname(__file__), "data")
    model_dir = os.path.join(os.path.dirname(__file__), "artifacts")

print(f"Running on: {'SageMaker' if IS_SAGEMAKER else 'local'}")
print(f"  data_dir  → {data_dir}")
print(f"  model_dir → {model_dir}")

# ---------------------------------------------------------------------------
# Load dataset
# ---------------------------------------------------------------------------

data_path = os.path.join(data_dir, "training_data.csv")
df = pd.read_csv(data_path)

X = df["text"].str.lower().tolist()
y = df["intent"].tolist()

print(f"Loaded {len(X)} training examples across {df['intent'].nunique()} classes")

# ---------------------------------------------------------------------------
# Train
# ---------------------------------------------------------------------------

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

pipeline.fit(X, y)

# ---------------------------------------------------------------------------
# Save model artefact
#
# SageMaker:  saves to /opt/ml/model/intent_model.pkl
#             → SageMaker auto-packages this into model.tar.gz after training
# Local:      saves to model/artifacts/intent_model.pkl (same as before)
# ---------------------------------------------------------------------------

os.makedirs(model_dir, exist_ok=True)
model_path = os.path.join(model_dir, "intent_model.pkl")
joblib.dump(pipeline, model_path)

print(f"Model saved to {model_path}")
