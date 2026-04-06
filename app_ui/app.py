from flask import Flask, render_template, request
import requests

app = Flask(__name__)

# FastAPI endpoint
API_URL = "http://api:8000/predict"

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/predict", methods=["POST"])
def predict():
    try:
        data = {
            "trans_date_trans_time": request.form["trans_date_trans_time"],
            "cc_num": float(request.form["cc_num"]),
            "merchant": request.form["merchant"],
            "category": request.form["category"],
            "amt": float(request.form["amt"]),
            "gender": request.form["gender"],
            "city": request.form["city"],
            "state": request.form["state"],
            "job": request.form["job"],
            "dob": request.form["dob"]
        }

        response = requests.post(API_URL, json=data)
        result = response.json()

        return render_template("index.html", result=result)

    except Exception as e:
        return render_template("index.html", error=str(e))


if __name__ == "__main__":
    app.run(host="0.0.0.0",debug=True, port=5000)