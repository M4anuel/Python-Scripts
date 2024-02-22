import requests
import tokens
ignoredoppler = True
ignorech = True
maxperc = 0.7
checked = []
minprice = 30
maxprice = 190


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
            f"name: {self.name} price: {self.price}, steam price: {self.suggested_price}, percentage: {self.percentage}, link: {self.link}")


api_key = tokens.CSFLOAT_KEY
r = requests.get("https://csgofloat.com/api/v1/listings", headers={'Authorization': api_key},
                 params={'min_price': minprice * 100, 'max_price': maxprice * 100, 'type': 'buy_now'}).json()
for i in r:
    link = "https://csgofloat.com/item/" + i["id"]
    percentage = 100 - (100 * (i["price"]) / (i["item"]["scm"]["price"]))
    try:
        if (i["created_at"]) not in checked:
            if (i["price"]) / (i["item"]["scm"]["price"]) <= maxperc:
                print(i["item"]["market_hash_name"],
                      str(100 - (100 * (i["price"]) / (i["item"]["scm"]["price"]))), link)
                item = Item(i["item"]["market_hash_name"], i["price"], i["item"]["scm"]["price"],
                            (i["price"]) / (i["item"]["scm"]["price"]), "https://csgofloat.com/item/" + i["id"])
                description = f"{item.name} \n Price: {item.price / 100} CHF \n Percentage: {percentage.__round__(2)}% off"
                checked.append(float(i["created_at"]))
    except Exception as e:
        pass
