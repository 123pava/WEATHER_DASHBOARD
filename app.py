import os

from flask import Flask, jsonify, render_template, request
import requests

app = Flask(__name__)

API_KEY = os.getenv("OPENWEATHER_API_KEY")
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"


def build_weather_response(data):
    return {
        "city": data["name"],
        "temperature": data["main"]["temp"],
        "feels_like": data["main"]["feels_like"],
        "humidity": data["main"]["humidity"],
        "pressure": data["main"]["pressure"],
        "wind": data["wind"]["speed"],
        "description": data["weather"][0]["description"],
        "icon": data["weather"][0]["icon"],
    }


def fetch_weather(url):
    try:
        response = requests.get(url, timeout=10)
        return response.json()
    except requests.RequestException:
        return {"cod": 500, "message": "Unable to reach weather service right now"}


@app.route("/")
def home():
    return render_template("index.html")



@app.route("/weather")
def get_weather():
    city = request.args.get("city")

    if not API_KEY:
        return jsonify({"error": "Server is missing OPENWEATHER_API_KEY configuration"})

    if not city:
        return jsonify({"error": "Please enter a city name"})

    url = f"{BASE_URL}?q={city}&appid={API_KEY}&units=metric"
    data = fetch_weather(url)

    if data.get("cod") != 200:
        return jsonify({"error": data.get("message", "City not found")})

    return jsonify(build_weather_response(data))


@app.route("/weather/location")
def get_location_weather():
    lat = request.args.get("lat")
    lon = request.args.get("lon")

    if not API_KEY:
        return jsonify({"error": "Server is missing OPENWEATHER_API_KEY configuration"})

    if not lat or not lon:
        return jsonify({"error": "Latitude and longitude are required"})

    url = f"{BASE_URL}?lat={lat}&lon={lon}&appid={API_KEY}&units=metric"
    data = fetch_weather(url)

    if data.get("cod") != 200:
        return jsonify({"error": data.get("message", "Unable to fetch weather for your location")})

    return jsonify(build_weather_response(data))


if __name__ == "__main__":
    app.run(debug=True)
