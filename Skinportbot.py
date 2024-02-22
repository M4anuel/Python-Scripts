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
        print(f"name: {self.name} price: {self.price}, steam price: {self.suggested_price}, percentage: {self.percentage}, link: {self.link}")


@bot.event
async def on_ready():
    print('ready')


@bot.command()
async def skinport_start(ctx):
    msg_with_selects = await ctx.send('Click to Select SkinportBot Options', components=[
        [
            SelectMenu(custom_id='_select_it', options=[
                SelectOption(emoji='🆖', label='ignore nothing', value='1',
                             description='Check this to start the bot'),
                SelectOption(emoji='1️⃣', label='Ignore Case Hardened', value='2',
                             description='Check this to ignore Case Hardened'),
                SelectOption(emoji='2️⃣', label='Ignore Dopplers', value='3',
                             description='Check this to ignore Dopplers')],
                       placeholder='Select Skinport-Bot Startoptions', max_values=2)
        ]])

    while True:
        def check_selection(i: discord.Interaction, select_menu):
            return i.author == ctx.author and i.message == msg_with_selects
        interaction, select_menu = await bot.wait_for('selection_select', check=check_selection)
        options = [{o} for o in select_menu.values]
        ignorech = False
        ignoredoppler = False
        for i in options:
            if i == {2}:
                ignorech = True
            if i == {3}:
                ignoredoppler = True

        embed = discord.Embed(title='currently being processed',
                              color=discord.Color.random())

        await interaction.respond(embed=embed, delete_after=2)
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
        await channel.send("sleeping for 1min")
        await asyncio.sleep(60)


@bot.command()
async def ignore_doppler(ctx):
    global ignoredoppler
    message = ""
    match ignoredoppler:
        case False:
            ignoredoppler = True
            message = " ignored"
        case True:
            ignoredoppler = False
            message = " not ignored anymore"
    await ctx.send("Dopplers are now"+ message)


@bot.command()
async def ignore_ch(ctx):
    global ignorech
    message = ""
    match ignorech:
        case False:
            ignorech = True
            message = " ignored"
        case True:
            ignorech = False
            message = " not ignored anymore"
    await ctx.send("Case Hardened are now"+ message)


@bot.command()
async def max_price(ctx, maxmoney):
    global maxprice
    maxprice= maxmoney
    await ctx.send("The max price of skins is now " + maxmoney + " CHF")


@bot.command()
async def min_percentage(ctx, percentage):
    global maxperc
    maxperc= 1-(float(percentage)/100)
    await ctx.send("The skins must now be " + percentage + " % down")

bot.run(tokens.DISCORD_CSFLOAT_BASE_BOT_KEY)