import asyncio

import websocket
import rel
import json
from discord.ext import commands
import discord
import tokens

intents = discord.Intents.all()
bot = commands.Bot(intents=intents, command_prefix='!')


def on_message(ws, message):
    if message == "2":
        ws.send("3")
    if message == '42["steamStatusUpdated","operational"]':
        ws.send('42["saleFeedJoin",{"appid":730,"currency":"CHF","locale":"en"}]')
    if message[0:2] == "42":
        response = json.loads(message[2:])
        item = Item(response[1]["sales"][0]["marketHashName"],
                    response[1]["sales"][0]["salePrice"],
                    response[1]["sales"][0]["suggestedPrice"],
                    float(response[1]["sales"][0]["salePrice"]) / float(response[1]["sales"][0]["suggestedPrice"]),
                    "https://skinport.com/de/item/" + response[1]["sales"][0]["url"] + "/" + str(
                        response[1]["sales"][0]["saleId"]),
                    response[1]["sales"][0]["image"])
        item.printer()
        print_In_Discord(item)


def print_In_Discord(item):
    description = f"{item.name} \n Price: {item.price} CHF \n Percentage: {(100 - item.percentage * 100).__round__(2)}% off"
    embed = discord.Embed(title="Snipe", url=item.link, description=description)
    bot.get_channel(948510631173165066).send("<@&955051370401124362>", embed=embed)


def on_error(ws, error):
    print(error)


def on_close(ws, close_status_code, close_msg):
    print("### closed ###")


def on_open(ws):
    print("Opened connection")
    ws.send("40")


class Item:
    name: str
    steam_suggested_price: float
    price: float
    percentage: float
    link: str
    image: str

    def __init__(self, name, price, suggested_price, percentage, link, image):
        self.name = name
        self.price = price
        self.suggested_price = suggested_price
        self.percentage = percentage
        self.link = link
        self.image = image

    def printer(self):
        print(
            f"name: {self.name} price: {self.price}, steam price: {self.suggested_price}, percentage: {self.percentage},"
            f" link: {self.link}")


@bot.event
async def on_ready(ctx):
    print('ready')
    websocket.enableTrace(True)
    ws = websocket.WebSocketApp("wss://skinport.com/socket.io/?EIO=4&transport=websocket",
                                header={'appid': '730',
                                        'currency': 'CHF',
                                        'locale': 'en'},
                                on_open=on_open,
                                on_message=on_message,
                                on_error=on_error,
                                on_close=on_close)
    ws.run_forever(dispatcher=rel)  # Set dispatcher to automatic reconnection
    rel.signal(2, rel.abort)  # Keyboard Interrupt
    rel.dispatch()



bot.run(tokens.DISCORD_CSFLOAT_BASE_BOT_KEY)
