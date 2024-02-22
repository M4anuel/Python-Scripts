import json

import discord
from websocket import WebSocketApp, enableTrace
import rel
import requests
import tokens
TOKEN = tokens.DISCORD_API_TOKEN 
USER_ID = tokens.DISCORD_USER_ID

BASE_URL = f"https://discord.com/api/v9"
SEND_URL = BASE_URL + "/channels/{id}/messages"
DM_URL = BASE_URL + f"/users/@me/channels"

headers = {
    "Authorization": f"Bot {TOKEN}",
    "User-Agent": f"DiscordBot"
}



def on_message(wsapp: WebSocketApp, message: str):
    dm_channel = requests.post(DM_URL, headers=headers, json={"recipient_id": USER_ID})
    dm_channel_id = dm_channel.json()["id"]
   # requests.post(SEND_URL.format(id=dm_channel_id), headers=headers, json={"content": message})
    print(message)
    if message == '2':
        wsapp.send("3")
    if message == '42["steamStatusUpdated","operational"]':
        wsapp.send('42["saleFeedJoin",{"appid":730,"currency":"CHF","locale":"en"}]')
    if message[0:2] == "42":
        response = json.loads(message[2:])
        item = Item(response[1]["sales"][0]["marketHashName"],
                    response[1]["sales"][0]["salePrice"],
                    response[1]["sales"][0]["suggestedPrice"],
                    float(response[1]["sales"][0]["salePrice"]) / float(response[1]["sales"][0]["suggestedPrice"]),
                    "https://skinport.com/de/item/" + response[1]["sales"][0]["url"] + "/" + str(
                    response[1]["sales"][0]["saleId"]),
                    response[1]["sales"][0]["image"],
                    response[1]["sales"][0]["rarity"],
                    response[1]["sales"][0]["wear"],
                    response[1]["sales"][0]["exterior"],)
        if item.percentage<0.7:
            requests.post(SEND_URL.format(id=dm_channel_id), headers=headers, json={"content": item.toString()})
        if item.exterior == "Field Tested" and item.wear < 0.2 and item.rarity == "Extraordinary":
            requests.post(SEND_URL.format(id=dm_channel_id), headers=headers, json={"content": item.toString()})





class Item:
    name: str
    steam_suggested_price: float
    price: float
    percentage: float
    link: str
    image: str
    rarity: str
    wear: float
    exterior: str
    def __init__(self, name, price, suggested_price, percentage, link, image, rarity, wear, exterior):
        self.name = name
        self.price = price
        self.suggested_price = suggested_price
        self.percentage = percentage
        self.link = link
        self.rarity = rarity
        self.float = wear
        self.image = image
        self.exterior = exterior

    def printer(self):
        print(
            f"name: {self.name} price: {self.price}, steam price: {self.suggested_price}, percentage: {self.percentage},"
            f" link: {self.link}")

    def toString(self):
        return(
            f"{self.name}, percentage: -{round(100-(self.percentage*100),2)}%, price: {self.price/100}CHF, steam price: {self.suggested_price/100}CHF,"
            f" link: {self.link}")


def on_error(wsapp: WebSocketApp, error: str):
    print(error)


def on_close(wsapp: WebSocketApp, close_status_code, close_msg):
    if close_status_code is not None:
        print(close_status_code)
    if close_msg is not None:
        print(close_msg)
    print("### closed ###")


def on_open(wsapp: WebSocketApp):
    wsapp.send("40")
    print("Opened connection")



if __name__ == "__main__":
    enableTrace(True)
    ws = WebSocketApp("wss://skinport.com/socket.io/?EIO=4&transport=websocket",
                      on_open=on_open,
                      on_message=on_message,
                      on_error=on_error,
                      on_close=on_close)
    ws.run_forever(dispatcher=rel)  # Set dispatcher to automatic reconnection
    rel.signal(2, rel.abort)  # Keyboard Interrupt
    rel.dispatch()
