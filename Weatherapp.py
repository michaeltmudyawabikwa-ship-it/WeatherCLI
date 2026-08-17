#saving data in an csv file
import requests
import csv
from datetime import datetime
import pandas as pd
import matplotlib.pyplot as plt


class WeatherApp:
    def __init__(self, city, lat, lon):
        self.city = city
        self.lat = lat
        self.lon = lon
        self.data = None

    def get_coords(self, city_name):
        url = f"https://geocoding-api.open-meteo.com/v1/search?name={city_name}&count=1"
        try:
            response = requests.get(url, timeout=5)
            response.raise_for_status()
            data = response.json()

            if "results" in data and len(data["results"]) > 0:
                lat = data["results"][0]["latitude"]
                lon = data["results"][0]["longitude"]
                return lat, lon
            else:
                return None, None

        except requests.exceptions.RequestException:
            print("Network error. Check your internet connection.")
            return None, None

    def fetch_weather(self):
        """Fetch full weather data (current, hourly, daily) and store in self.data."""
        url = (
            f"https://api.open-meteo.com/v1/forecast"
            f"?latitude={self.lat}&longitude={self.lon}"
            f"&current_weather=true"
            f"&hourly=relativehumidity_2m"
            f"&daily=temperature_2m_max,temperature_2m_min,windspeed_10m_max"
            f"&timezone=auto"
        )
        try:
            response = requests.get(url, timeout=5)
            response.raise_for_status()
            self.data = response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching weather data: {e}")
            self.data = None

    def get_weather(self):
        """Return current temperature."""
        if not self.data or "current_weather" not in self.data:
            return "No weather data available. Run fetch_weather() first."
        temp = self.data["current_weather"]["temperature"]
        return f"Weather in {self.city}: {temp} °C"

    def get_humidity(self):
        """Return the most recent hourly humidity reading."""
        if not self.data or "hourly" not in self.data:
            return "No humidity data available."
        humidity = self.data["hourly"]["relativehumidity_2m"][0]
        return f"Humidity in {self.city}: {humidity}%"

    def get_wind_speed(self):
        """Return current wind speed."""
        if not self.data or "current_weather" not in self.data:
            return "No wind data available."
        wind = self.data["current_weather"]["windspeed"]
        return f"Wind speed in {self.city}: {wind} km/h"

    def get_forecast(self):
        """Return today's min/max temperature forecast."""
        if not self.data or "daily" not in self.data:
            return "No forecast data available."
        max_temp = self.data["daily"]["temperature_2m_max"][0]
        min_temp = self.data["daily"]["temperature_2m_min"][0]
        return f"Forecast for {self.city}: Min {min_temp} °C / Max {max_temp} °C"

    def save_to_csv(self, filename="weather_log.csv"):
        """Append current weather data to a CSV file."""
        if not self.data or "current_weather" not in self.data:
            return "No data to save. Run fetch_weather() first."

        temp = self.data["current_weather"]["temperature"]
        humidity = self.data["hourly"]["relativehumidity_2m"][0]
        wind = self.data["current_weather"]["windspeed"]
        max_temp = self.data["daily"]["temperature_2m_max"][0]
        min_temp = self.data["daily"]["temperature_2m_min"][0]
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        write_header = False
        try:
            with open(filename, "r") as f:
                write_header = f.read(1) == ""  # empty file → write header
        except FileNotFoundError:
            write_header = True  # file doesn't exist yet → write header

        with open(filename, "a", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            if write_header:
                writer.writerow(["Timestamp", "City", "Temp", "Humidity", "Wind", "Min", "Max"])
            writer.writerow([timestamp, self.city, temp, humidity, wind, min_temp, max_temp])

        return f"Saved {self.city} data to {filename}"


def plot_temps(csv_file="weather_log.csv"):
    """Plot temperature over time for all cities in the CSV."""
    try:
        df = pd.read_csv(csv_file)
    except FileNotFoundError:
        print(f"No data file found at '{csv_file}'. Fetch some data first.")
        return

    plt.figure(figsize=(10, 5))
    for city in df["City"].unique():
        city_data = df[df["City"] == city]
        plt.plot(city_data["Timestamp"], city_data["Temp"], marker="o", label=city)

    plt.title("Temperature by City Over Time")
    plt.xlabel("Time")
    plt.ylabel("Temperature °C")
    plt.xticks(rotation=45)
    plt.legend()
    plt.tight_layout()
    plt.show()


def main():
    print("Weather CLI App - Type 'quit' to exit")

    while True:
        city_name = input("\nEnter city name or 'quit' to exit: ").strip()

        if city_name.lower() == "quit":
            print("Bye!")
            break

        if not city_name:
            print("Please enter a city name.")
            continue

        # Resolve coordinates
        app = WeatherApp(city_name, 0, 0)
        lat, lon = app.get_coords(city_name)

        if lat is None:
            print(f"City '{city_name}' not found. Try again.")
            continue

        # Re-initialise with real coords and fetch all data in one call
        app = WeatherApp(city_name, lat, lon)
        app.fetch_weather()

        if app.data is None:
            print("Failed to retrieve weather data. Try again.")
            continue

        print(app.get_weather())
        print(app.get_humidity())
        print(app.get_wind_speed())
        print(app.get_forecast())
        print(app.save_to_csv())

    # Show plot after the loop exits
    try:
        plot_temps()
    except Exception as e:
        print(f"Could not plot graph: {e}")


if __name__ == "__main__":
    main()