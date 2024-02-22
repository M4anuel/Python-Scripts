from discord import SelectOption, SelectMenu
from discord.ext import commands
import requests
import discord
import asyncio
import tokens

bot = commands.Bot(command_prefix="!")

checked = []

ignoredoppler = True
ignorech = True
maxprice = 70
minprice = 30
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
        print(f"name: {self.name} price: {self.price}, steam price: {self.suggested_price}, percentage: {self.percentage}, link: {self.link}")


@bot.event
async def on_ready():
    print('ready')


@bot.command()
async def CSF_run(ctx):
    while True:
        api_key = tokens.CSFLOAT_KEY
        r = requests.get("https://csgofloat.com/api/v1/listings",
                         headers={'Authorization': api_key},
                         params={'min_price': minprice * 100,
                                 'max_price': maxprice * 100,
                                 'type': 'buy_now'
                                 }).json()
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
                        embed = discord.Embed(title="Snipe", url=item.link, description=description)
                        if ignoredoppler and ignorech:
                            if "Doppler" not in item.name and "Case Hardened" not in item.name:
                                await ctx.send("<@&955051435144400936>", embed=embed)
                        elif ignoredoppler:
                            if "Doppler" not in item.name:
                                await ctx.send("<@&955051435144400936>", embed=embed)
                        elif ignorech:
                            if "Case Hardened" not in item.name:
                                await ctx.send("<@&955051435144400936>", embed=embed)
                        else:
                            await ctx.send("<@&955051435144400936>", embed=embed)
                        checked.append(float(i["created_at"]))
            except Exception as e:
                pass
        channel = bot.get_channel(948512094972682241)
        await channel.send("sleeping for 5 min")
        await asyncio.sleep(300)


bot.run(tokens.DISCORD_CSFLOAT_BASE_BOT_KEY)