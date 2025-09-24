import requests
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

# Coordinates for Kuala Lumpur (change if you want another city)
LAT, LON = 3.139, 101.686

# --- Get Weather Data ---
weather_url = (
    f"https://api.open-meteo.com/v1/forecast?"
    f"latitude={LAT}&longitude={LON}&hourly=temperature_2m"
)
w = requests.get(weather_url).json()
weather = w["hourly"]

# --- Get Air Quality Data (safe) ---
aq_url = f"https://api.openaq.org/v2/latest?coordinates={LAT},{LON}&parameter=pm25"
a = requests.get(aq_url).json()

# Use .get to avoid KeyError
aqi = None
results = a.get("results", [])
if results:
    measurements = results[0].get("measurements", [])
    if measurements:
        aqi = measurements[0].get("value")

        print(f"Air Quality (PM2.5): {aqi if aqi is not None else 'No data'}")

# --- Put it into a Table ---
df = pd.DataFrame({
    "time": weather["time"],
    "temperature": weather["temperature_2m"]
})
df["time"] = pd.to_datetime(df["time"])
df["comfort_index"] = 100 - (df["temperature"] * 0.5 + (aqi or 0))

# --- Save & Plot ---
csv_name = f"dashboard_{datetime.now():%Y%m%d_%H%M}.csv"
df.to_csv(csv_name, index=False)
print(f"Saved data to {csv_name}")
print(df.head())  # show first few rows

plt.plot(df["time"], df["temperature"], label="Temperature °C")
plt.plot(df["time"], df["comfort_index"], label="Comfort Index")
plt.legend()
plt.title("Weather & Comfort Index")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("weather_dashboard.png")
plt.show()
