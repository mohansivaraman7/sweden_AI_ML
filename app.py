from flask import Flask, jsonify, request
import joblib

app = Flask(__name__)
print("hello India")
model = joblib.load("sridhar.pkl")

@app.route("/")
def my_landing_page():
    return "Welcome to my API"

@app.route("/reshma")
def my_special_function():
    return "Welcome to new home"

@app.route("/predict", methods=["POST"])
def predict():

    data = request.json
    size = data["size"]
    prediction = model.predict([[size]])
    predicted_price = float(prediction[0])

    return jsonify({
        "house_size": size,
        "predicted_price": predicted_price
    })

if __name__ == "__main__":
    app.run()

