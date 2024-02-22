from discord import SelectOption, SelectMenu
from discord.ext import commands
import requests
import discord
import asyncio
import tokens

bot = commands.Bot(command_prefix="!")

checked = []

ignoredoppler = False
ignorech = True
maxprice = 600
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


@bot.event
async def on_ready():
    print('ready')


@bot.command()
async def SP_run(ctx):
    while True:
        r = requests.get("https://api.skinport.com/v1/items", params={
            "app_id": 730,
            "currency": "CHF",
            "tradable": 0
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
                                    await ctx.send("<@&955051370401124362>", embed=embed)
                            elif ignoredoppler:
                                if "Doppler" not in item.name:
                                    await ctx.send("<@&955051370401124362>", embed=embed)
                            elif ignorech:
                                if "Case Hardened" not in item.name:
                                    await ctx.send("<@&955051370401124362>", embed=embed)
                            else:
                                await ctx.send("<@&955051370401124362>", embed=embed)
                            checked.append(float(i["created_at"]))
            except Exception as e:
                pass
        channel = bot.get_channel(948512094972682241)
        await channel.send("sleeping for 60 sec")
        await asyncio.sleep(60)


bot.run(tokens.DISCORD_CSFLOAT_BASE_BOT_KEY)
