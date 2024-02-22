import percentage as percentage
import requests
import discord
import tokens

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
        print(
            f"name: {self.name}."
            f" price: {self.price},"
            f" steam price: {self.suggested_price},"
            f" percentage: {self.percentage},"
            f" link: {self.link}")


checked = []
ignoredoppler = True
ignorech = True
maxprice = 500
maxperc = 0.7

api_key = tokens.CSFLOAT_KEY
r = requests.get("https://csgofloat.com/api/v1/listings",
                 headers={'Authorization': api_key},
                 params={"max_price": 35000,
                         "min_price": 5000,
                         "type": "buy_now"
                         }).json()

for i in r:
    percentage = 100-(100*(i["price"]) / (i["item"]["scm"]["price"]))
    link = "https://csgofloat.com/item/" + i["id"]
    print(i["item"]["market_hash_name"], i["price"], i["item"]["scm"]["price"], percentage.__round__(2), link)
