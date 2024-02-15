

import requests
from bs4 import BeautifulSoup

def download_file(url, filename):
    response = requests.get(url)
    if response.status_code == 200:
        with open(filename, "wb") as file:
            file.write(response.content)
        print(f"Die Datei {filename} wurde erfolgreich heruntergeladen.")
    else:
        print(f"Fehler beim Herunterladen der Datei {filename}: {response.status_code} {response.reason}")

def main():
    base_url = "https://opendata.dwd.de/climate_environment/CDC/observations_germany/climate/5_minutes/precipitation/historical/2022/"
    page_url = base_url + "5min_rr_Beschreibung_Stationen.txt"

    response = requests.get(page_url)
    soup = BeautifulSoup(response.text, "html.parser")

    station_name = input("Bitte geben Sie den Namen der Station ein: ")

    station_id = None
    for line in soup.text.split("\n"):
        if station_name in line:
            station_id = line.split()[0]
            break

    if station_id is None:
        print(f"Die Station '{station_name}' wurde nicht gefunden.")
        return

    print(f"Die Station-ID für '{station_name}' lautet '{station_id}'.")

    for month in range(1, 13):
        month_str = str(month).zfill(2)
        for day in range(1, 32):
            day_str = str(day).zfill(2)
            filename = f"5minutenwerte_nieder_{station_id}_2022{month_str}{day_str}.txt"
            url = base_url + filename
            try:
                download_file(url, filename)
            except Exception as e:
                print(f"Fehler beim Herunterladen der Datei {filename}: {str(e)}")

if __name__ == "__main__":
    main()