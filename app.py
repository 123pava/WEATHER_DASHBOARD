import os

from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

API_KEY = os.getenv("OPENWEATHER_API_KEY")

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/ui-demo")
def ui_demo():
    return render_template("ui_demo.html")

@app.route('/weather')
def get_weather():
    city = request.args.get('city')

    if not API_KEY:
        return jsonify({"error": "Server is missing OPENWEATHER_API_KEY configuration"})

    if not city:
        return jsonify({"error": "Please enter a city name"})

    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
    response = requests.get(url, timeout=10)
    data = response.json()

    # ✅ ADD THIS ERROR CHECK
    if data.get("cod") != 200:
        return jsonify({"error": data.get("message", "City not found")})

    # ✅ MODIFY RESPONSE FORMAT
    return jsonify({
        "city": data["name"],
        "temperature": data["main"]["temp"],
        "feels_like": data["main"]["feels_like"],
        "humidity": data["main"]["humidity"],      
        "pressure": data["main"]["pressure"],
        "wind": data["wind"]["speed"],
        "description": data["weather"][0]["description"],
        "icon": data["weather"][0]["icon"]
    })
if __name__ == "__main__":
    app.run(debug=True)
