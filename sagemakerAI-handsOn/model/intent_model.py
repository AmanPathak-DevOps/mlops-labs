import os
import joblib

# SageMaker unpacks model.tar.gz into SM_MODEL_DIR at inference time.
# Locally we fall back to the repo's model/artifacts/ directory.
_DEFAULT_MODEL_DIR = os.environ.get(
    "SM_MODEL_DIR",
    os.path.join(os.path.dirname(__file__), "artifacts")
)
_DEFAULT_MODEL_PATH = os.path.join(_DEFAULT_MODEL_DIR, "intent_model.pkl")


class IntentModel:
    def __init__(self, path=_DEFAULT_MODEL_PATH):
        self.pipeline = joblib.load(path)

    def predict(self, text):
        pred = self.pipeline.predict([text])[0]
        return {"intent": pred}
