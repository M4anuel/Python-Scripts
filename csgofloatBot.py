from discord import SelectOption, SelectMenu
from discord.ext import commands
import requests
import discord
import asyncio
import tokens

bot = commands.Bot(command_prefix="!")

checked = []

ignoredoppler = False
ignorech = False
maxprice = 350
minprice = 50
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
async def csgofloat_start(ctx):
    msg_with_selects = await ctx.send('Click to Select csgofloatBot Options', components=[
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
            print(i["item"]["market_hash_name"], str(100 - (100 * (i["price"]) / (i["item"]["scm"]["price"]))), link)
            try:
                if (i["created_at"]) not in checked:
                    if (i["price"]) / (i["item"]["scm"]["price"]) <= maxperc:
                        print(i["item"]["market_hash_name"],
                              str(100 - (100 * (i["price"]) / (i["item"]["scm"]["price"]))), link)
                        item = Item(i["item"]["market_hash_name"], i["price"], i["item"]["scm"]["price"],
                                    (i["price"]) / (i["item"]["scm"]["price"]), "https://csgofloat.com/item/" + i["id"])
                        description = f"{item.name} \n Price: {item.price/100} CHF \n Percentage: {percentage.__round__(2)}% off"
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


@bot.command()
async def csgofloat_ignore_doppler(ctx):
    global ignoredoppler
    message = ""
    match ignoredoppler:
        case False:
            ignoredoppler = True
            message = " ignored"
        case True:
            ignoredoppler = False
            message = " not ignored anymore"
    await ctx.send("Dopplers are now" + message)


@bot.command()
async def csgofloat_ignore_ch(ctx):
    global ignorech
    message = ""
    match ignorech:
        case False:
            ignorech = True
            message = " ignored"
        case True:
            ignorech = False
            message = " not ignored anymore"
    await ctx.send("Case Hardened are now" + message)


@bot.command()
async def csgofloat_max_price(ctx, maxmoney):
    global maxprice
    maxprice = maxmoney
    await ctx.send("The max price of skins is now " + maxmoney + " CHF")


@bot.command()
async def csgofloat_min_percentage(ctx, percentage):
    global maxperc
    maxperc = 1 - (float(percentage) / 100)
    await ctx.send("The skins must now be " + percentage + " % down")


bot.run(tokens.CSFLOAT_KEY)
