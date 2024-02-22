from discord import SelectOption, SelectMenu
from discord.ext import commands
import requests
import discord
import asyncio
import tokens

checked = []

ignoredoppler = True
ignorech = True
maxprice = 500
maxperc = 0.7


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


s = requests.get("https://api.skinport.com/v1/items", params={
    "app_id": 730,
    "currency": "EUR"
}).json()

api_key = tokens.SWAPPGG_API_KEY
r = requests.get("https://market-api.swap.gg/v1/pricing/lowest?appId=730",
                 headers={'Authorization': api_key, 'Content-Type': 'multipart/form-data'
                          }).json()
for i in r:
    try:
        if float(i["created_at"]) not in checked:
            if float(i["min_price"]) / float(i["suggested_price"]) <= maxperc:
                if 10 < float(i["min_price"]) < maxprice:
                    item = Item(i["market_hash_name"], i["min_price"], i["suggested_price"],
                                float(i["min_price"]) / float(i["suggested_price"]), i["item_page"])
                    description = f"{item.name} \n Price: {item.price} CHF \n Percentage: {(100 - item.percentage * 100).__round__(2)}% off"
                    embed = discord.Embed(title="Snipe", url=item.link, description=description)
                    if ignoredoppler and ignorech:
                        if "Doppler" not in item.name and "Case Hardened" not in item.name:
                            await ctx.send("<@&948511559901134888>", embed=embed)
                            checked.append(float(i["created_at"]))
                    elif ignoredoppler:
                        if "Doppler" not in item.name:
                            await ctx.send("<@&948511559901134888>", embed=embed)
                            checked.append(float(i["created_at"]))
                    elif ignorech:
                        if "Case Hardened" not in item.name:
                            await ctx.send("<@&948511559901134888>", embed=embed)
                            checked.append(float(i["created_at"]))
                    else:
                        await ctx.send("<@&948511559901134888>", embed=embed)
                        checked.append(float(i["created_at"]))
    except Exception as e:
        pass

print(r)

item = Item(i["market_hash_name"], i["min_price"], i["suggested_price"],
            float(i["min_price"]) / float(i["suggested_price"]), i["item_page"])
