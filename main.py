import datetime
from os import path
import requests

history = {}


class WeatherForecast:
    def __init__(self, api):
        self.api = api
        self.opad = ("Rain", "Snow", "Będzie padać", "Nie będzie padać")

    def data_load(self):
        if path.isfile("pogoda2.txt"):
            for line in self.generator():
                history[line[0]]=line[1]
            return history
        else:
            self.czytaj_16dni(self)

    def czytaj_16dni(self):
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

        response = requests.request(
            "GET", url, headers=headers, params=querystring
            )
        dane = response.json()

        for day in dane["list"]:
            date = datetime.datetime.utcfromtimestamp(int(day["dt"])).strftime(
            "%Y-%m-%d"
        )
            history[date] = (
                "Będzie padać" if day["weather"][0]["main"] in self.opad else
                 "Nie będzie padać"
                 )
        return history

    def generator(self):
        with open("pogoda2.txt", "r") as pogoda_log:
            for line in pogoda_log:
                yield (line.split(' ')[0], ' '.join(line.strip().split(' ')[1:]))         


    def __iter__(self):
        self.dates_list = []
        self.fp = open("pogoda2.txt")
        return self

    def __next__(self):
        dates = self.fp.readline().strip().split()
        if not dates:
            self.fp.close()
            raise StopIteration
        self.dates_list.append(dates)
        return dates

    def __getitem__(self, item):
        return f"{item} {history[item]}"

    def __str__(self):
        for dates in self:
            print(dates[0]) 
        return "stop iterator"

    def items(self):
        for line in self.generator():
            print((line[0], line[1]))


wf = WeatherForecast("")
wf.data_load()
#print("\niterator wf:")
#print(wf)
#print("\nwf[data]:")
print(history)
date = "2022-02-15"
print(wf[date])
#print("\nwf.items():")
#wf.items()
#print("\n")

#print(wf.czytaj_16dni())
