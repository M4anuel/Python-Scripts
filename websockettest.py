import websocket
import rel
import json


def on_message(ws, message):
    if message == "2":
        ws.send("3")
    if message == '42["steamStatusUpdated","operational"]':
        ws.send('42["saleFeedJoin",{"appid":730,"currency":"CHF","locale":"en"}]')
    response = json.loads(message[2:])
    stri = response[1]["sales"][0]["marketHashName"]
    print(stri)
    print(response[1]["sales"][0]["marketHashName"],
          response[1]["sales"][0]["salePrice"],
          response[1]["sales"][0]["suggestedPrice"],
          float(response[1]["sales"][0]["salePrice"]) / float(response[1]["sales"][0]["suggestedPrice"]),
          "https://skinport.com/de/item/" + response[1]["sales"][0]["url"] + "/" + str(response[1]["sales"][0]["saleId"]),
          response[1]["sales"][0]["image"])
    if message[0:2] == "42":
        # response = json.loads(message[2:])
        # str = response[1]["sales"][0]["url"]
        # print(response)
        # print(str)

        item = Item(response[1]["sales"][0]["marketHashName"],
                    response[1]["sales"][0]["salePrice"],
                    response[1]["sales"][0]["suggestedPrice"],
                    float(response[1]["sales"][0]["salePrice"]) / float(response[1]["sales"][0]["suggestedPrice"]),
                    "https://skinport.com/de/item/" + response[1]["sales"][0]["url"] + "/" + str(response[1]["sales"][0]["saleId"]),
                    response[1]["sales"][0]["image"])
        #item.printer()


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


def on_error(ws, error):
    print(error)


def on_close(ws, close_status_code, close_msg):
    print("### closed ###")


def on_open(ws):
    print("Opened connection")
    ws.send("40")


if __name__ == "__main__":
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
