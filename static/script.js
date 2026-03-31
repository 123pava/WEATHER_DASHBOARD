function renderError(message) {
    document.getElementById("result").innerHTML = `<div class="result-error">${message}</div>`;
}

function renderWeatherCard(weather) {
    const iconUrl = `https://openweathermap.org/img/wn/${weather.icon}@2x.png`;

    document.getElementById("result").innerHTML = `
        <div class="card">
            <h2>${weather.city}</h2>
            <img src="${iconUrl}" alt="weather icon">
            <p>Temperature: ${weather.temperature} C</p>
            <p>Feels like: ${weather.feels_like} C</p>
            <p>Condition: ${weather.description}</p>
            <p>Humidity: ${weather.humidity}%</p>
            <p>Wind: ${weather.wind} m/s</p>
            <p>Pressure: ${weather.pressure} hPa</p>
        </div>
    `;
}

async function getWeather() {
    const city = document.getElementById("city").value.trim();

    if (!city) {
        renderError("Please enter a city name.");
        return;
    }

    try {
        const response = await fetch(`/weather?city=${encodeURIComponent(city)}`);
        const data = await response.json();

        if (data.error) {
            renderError(data.error);
            return;
        }

        renderWeatherCard(data);
    } catch (error) {
        console.error(error);
        renderError("Something went wrong while fetching weather data.");
    }
}

function toggleMode() {
    document.body.classList.toggle("dark-mode");
}

function startVoice() {
    if (!("webkitSpeechRecognition" in window)) {
        alert("Voice search not supported in this browser");
        return;
    }

    const recognition = new webkitSpeechRecognition();
    recognition.lang = "en-IN";
    recognition.start();

    recognition.onstart = () => {
        document.getElementById("result").innerHTML = `<div class="empty-card"><p class="empty-title">Listening...</p><p class="empty-text">Speak the city name clearly.</p></div>`;
    };

    recognition.onresult = (event) => {
        const transcript = event.results[0][0].transcript;
        document.getElementById("city").value = transcript;
        getWeather();
    };

    recognition.onerror = (event) => {
        alert("Error: " + event.error);
    };
}

function getLocationWeather() {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(success, error);
    } else {
        alert("Geolocation is not supported by this browser.");
    }
}

function success(position) {
    const lat = position.coords.latitude;
    const lon = position.coords.longitude;

    fetch(`/weather/location?lat=${encodeURIComponent(lat)}&lon=${encodeURIComponent(lon)}`)
        .then((response) => response.json())
        .then((data) => {
            if (data.error) {
                renderError(data.error);
                return;
            }

            renderWeatherCard(data);
        })
        .catch(() => {
            renderError("Error getting location weather.");
        });
}

function error() {
    alert("Location access denied");
}

document.addEventListener("DOMContentLoaded", () => {
    const cityInput = document.getElementById("city");

    cityInput.addEventListener("keydown", (event) => {
        if (event.key === "Enter") {
            getWeather();
        }
    });
});
