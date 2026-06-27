from flask import Flask, request, jsonify, render_template
from model.intent_model import IntentModel

app = Flask(__name__)

model = IntentModel()


@app.route("/", methods=["GET"])
def home():
    return render_template("index.html")


@app.route("/health", methods=["GET"])
def health():
    return jsonify({
        "status": "healthy"
    }), 200


@app.route("/predict", methods=["POST"])
def predict():

    data = request.get_json()

    if not data or "text" not in data:
        return jsonify({
            "error": "text field is required"
        }), 400

    text = data.get("text")

    prediction = model.predict(text)

    return jsonify(prediction), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
