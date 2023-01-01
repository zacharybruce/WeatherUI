
import requests
import json
import os
import tkinter as tk
from datetime import datetime, timezone

root = tk.Tk()
root.title("Current Weather")
root.geometry("270x250")


def get_temp():
    global weather_label

    city = requests.get(f"http://api.openweathermap.org/geo/1.0/"
                        f"direct?q={cityEntry.get()}&limit=1"
                        f"&appid={os.environ.get('WeatherAPIToken')}").text
    city_load = json.loads(city)
    city_dump = json.dumps(city_load, indent=4)

    try:
        lat = city_load[0]['lat']
        lon = city_load[0]['lon']
    except IndexError:
        weather_label["text"] = "Invalid City Name"
        return

    # Get current weather data for custom location from openweathermap.org
    weather = requests.get(f"https://api.openweathermap.org/data/2.5/"
                           f"onecall?lat={lat}&lon={lon}&exclude=minutely&units=imperial"
                           f"&appid={os.environ.get('WeatherAPIToken')}").text

    weather_load = json.loads(weather)
    weather_dump = json.dumps(weather_load, indent=4)

    current_time = datetime.fromtimestamp(weather_load['current']['dt']).time()

    # Weather Label
    try:
        weather_label["text"] = f"{current_time}\n\n" \
                                f"{weather_load['current']['weather'][0]['main']}\n\n" \
                                f"Temperature:\t{weather_load['current']['temp']} F\n" \
                                f"Feels Like:\t{weather_load['current']['feels_like']} F\n" \
                                f"Wind Speed: \t{weather_load['current']['wind_gust']} mph"

    except:
        weather_label["text"] = "Could not find weather"


weather_label = tk.Label(root, text="")
weather_label.grid(row=4, column=0, columnspan=2, padx=20, pady=20)

# City label
cityLabel = tk.Label(root, text="Enter City Name:")
cityLabel.grid(row=0, column=0, pady=5, padx=20)

# City entries
cityEntry = tk.Entry(root)
cityEntry.grid(row=0, column=1)

# Get temperature button
weatherButton = tk.Button(text="Get Weather", padx=10, pady=5, command=get_temp, bg="#F1948A")
weatherButton.grid(row=3, column=0, columnspan=2, padx=5, pady=5)

root.mainloop()
