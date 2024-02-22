from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import random
import time
import tokens

PATH = "C:\WebDriver\chromedriver.exe"
driver = webdriver.Chrome(PATH)

driver.get("https://discord.com/channels/802241096192491530/802280552191098960")

email = driver.find_element(by=By.NAME, value="email")
email.send_keys(tokens.DISCORD_ALT_MAIL)
password = driver.find_element(by=By.NAME, value="password")
password.send_keys(tokens.DISCORD_ALT_PW)
password.send_keys(Keys.RETURN)

messages = ["Hallo Nelio",
            "I bi um die Zyte no wach",
            "Na, wie geits dir so?",
            "scho komisch wini öppä aui 60 Sekunde öppis schribe",
            "I bi sicher kei Bot",
            "I würd nie über dini Mueter rede",
            "wieso hani so es höchs mee6 level?",
            "I weiss ni obi drfür e discord Ban kassiere, wäg däm machis ni ufem main account",
            "schono witzig",
            "Never gonna give you up Never gonna let you down Never gonna run around and desert you Never gonna make you cry Never gonna say goodbye Never gonna tell a lie and hurt you",
            "lol",
            "i due mini zyt vor de Maturprüefige guet investiere",
            "weles Level i wou ha?",
            "!rank"]

time.sleep(5)
while True:
    search = driver.find_element(by=By.CLASS_NAME, value="editor-H2NA06")
    search.send_keys(messages[(random.randint(0, 13))])
    search.send_keys(Keys.RETURN)
    time.sleep(60+round(random.uniform(0.00, 23.54), 2))
