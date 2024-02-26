
import csv
from datetime import datetime, timedelta
import requests

# Setze hier deinen API-Schlüssel ein
#api_key = '8c46804659dc1c7f660fa34475490426'
stadt = 'Berlin,DE'


# Funktion zum Abrufen der Wetterdaten von der API
def abrufen_wetterdaten():
    try:
        url = f"http://api.openweathermap.org/data/2.5/forecast?q={stadt}&appid={api_key}&units=metric"
        response = requests.get(url)
        data = response.json()

        if response.status_code == 200:
            return data
        else:
            print('Fehler beim Abrufen der Wetterdaten.')
            return None
    except Exception as e:
        print('Fehler beim Abrufen der Wetterdaten:', str(e))
        return None


# Funktion zum Generieren der Wetterdaten
def generiere_wetterdaten():
    data = abrufen_wetterdaten()

    if data is not None:
        station_name = data['city']['name']
        current_date = datetime.now()

        with open('wetterdaten.csv', 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Name der Station', 'Jahr', 'Monat', 'Wochentag', 'Uhrzeit', 'Temperatur', 'Niederschlag',
                             'Bewölkung', 'Sonneneinstrahlung', 'Windrichtung'])

            for forecast in data['list']:
                timestamp = forecast['dt']
                forecast_date = datetime.fromtimestamp(timestamp)

                if forecast_date >= current_date:
                    row = [
                        station_name,
                        forecast_date.year,
                        forecast_date.month,
                        forecast_date.strftime("%A"),
                        forecast_date.strftime("%H:%M"),
                        forecast['main']['temp'],
                        forecast.get('rain', {}).get('3h', 'N/A'),
                        forecast['clouds']['all'],
                        forecast.get('sun', {}).get('sunset', 'N/A'),
                        forecast['wind']['speed']
                    ]
                    writer.writerow(row)


# Hauptprogramm
generiere_wetterdaten()

# Weitere Verarbeitung der Wetterdaten

#Fehler beim Abrufen der Wetterdaten.
