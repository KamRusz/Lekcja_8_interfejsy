import datetime
from os import path
import requests
import json
import sys

try:
    api_key = sys.argv[1]
except IndexError:
    exit("nie podano klucza api")
else:
    api_key = sys.argv[1]

try:
    req_date = sys.argv[2]
except IndexError:
    req_date = str(datetime.date.today() + datetime.timedelta(days=1))
else:
    req_date = sys.argv[2]
taken_date = datetime.datetime.strptime(req_date, "%Y-%m-%d")

if taken_date < (datetime.datetime.today() - datetime.timedelta(1)) or taken_date > (
    datetime.datetime.today() + datetime.timedelta(15)
):
    exit(
        f"\n{req_date} : Nie wiem"
        "\n\nProgram obsługuje wyłącznie daty od"
        f" {datetime.date.today()}"
        f" do {datetime.date.today() + datetime.timedelta(15)}\n"
    )


class WeatherForecast:
    def __init__(self, api):
        self.api = api
        self.opad = ("Rain", "Snow")
        self.history = {}
        self.data_load()

    def data_load(self):
        if path.isfile("pogoda2.txt"):
            with open("pogoda2.txt", "r") as pogoda_log:
                self.history = json.load(pogoda_log)
                if self.history["valid till"] != str(datetime.date.today()):
                    self.read_api()
                return self.history
        else:
            self.read_api()

    def data_save(self):
        with open("pogoda2.txt", "w") as pogoda_log:
            json.dump(
                self.history, pogoda_log, sort_keys=True, indent=4, ensure_ascii=False
            )

    def read_api(self):
        url = "https://community-open-weather-map.p.rapidapi.com/forecast/daily"

        querystring = {
            "q": "roszkowo,pl",
            "lat": "54.253841",
            "lon": "18.681574",
            "cnt": "16",
            "units": "metric",
            "mode": "json",
            "lang": "pl",
        }

        headers = {
            "x-rapidapi-host": "community-open-weather-map.p.rapidapi.com",
            "x-rapidapi-key": self.api,
        }

        response = requests.request("GET", url, headers=headers, params=querystring)
        dane = response.json()
        valid_date = dane["list"][0]["dt"]
        valid_date = datetime.datetime.utcfromtimestamp(int(valid_date)).strftime(
            "%Y-%m-%d"
        )
        self.history["valid till"] = valid_date

        for day in dane["list"]:
            date = datetime.datetime.utcfromtimestamp(int(day["dt"])).strftime(
                "%Y-%m-%d"
            )

            self.history[date] = (
                "Będzie padać"
                if day["weather"][0]["main"] in self.opad
                else "Nie będzie padać"
            )
        return self.history

    def __iter__(self):
        return iter(self.history.keys())

    def __getitem__(self, item):
        return f"{item} {self.history[item]}"

    def __str__(self):
        for dates in self:
            print(dates[0])
        return "stop iterator"

    def items(self):
        return self.history.items()


wf = WeatherForecast(api_key)
wf.data_save
date = "2022-02-20"
print(wf[date])

"""
for date, prescript in wf.items():
    print(date, prescript)
"""
"""
for date in wf:
    print(date)
"""
