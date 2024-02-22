import tokens
import requests
from datetime import datetime
lat = 47.05675823301017
lon = 7.6194591203878
api_key = tokens.OPEN_WEATHER_KEY
lang = "de"
url = "http://api.openweathermap.org/data/2.5/weather?lat="+str(lat)+"&lon="+str(lon)+"&units=metric&appid="+api_key+"&lang="+lang

result = requests.get(url).json()
temp = result["main"]["temp"]
sunrise = datetime.utcfromtimestamp(result["sys"]["sunrise"]).strftime('%Y-%m-%d %H:%M:%S')

checked = []
class Item:
    name: str
    steam_suggested_price: float
    price: float
    percentage: float
    link: str

    def __init__(self, name, price, suggested_price, percentage, link):
        self.name = name
        self.price = price
        self.suggested_price = suggested_price
        self.percentage = percentage
        self.link = link

    def printer(self):
        print(f"name: {self.name} price: {self.price}, steam price: {self.suggested_price}, percentage: {self.percentage}, link: {self.link}")

r = requests.get("https://api.skinport.com/v1/items", params={
            "app_id": 730,
            "currency": "CHF",
            "tradable": 0
        }).json()
print(r)
for i in r:
            try:
                if float(i["created_at"]) not in checked:
                    if float(i["min_price"])/float(i["suggested_price"]) <= 0.7:
                        if 10 < float(i["min_price"]) < 200:
                            item = Item(i["market_hash_name"], i["min_price"], i["suggested_price"], float(i["min_price"])/float(i["suggested_price"]), i["item_page"])
                            description = f"{item.name} \n Price: {item.price} CHF \n Percentage: {(100-item.percentage*100).__round__(2)}% off \n item page: {item.link} \n"
                            if "Doppler" not in item.name:
                                print(description)

            except Exception as e:
                pass




