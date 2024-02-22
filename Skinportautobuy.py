import time
from seleniumwire import webdriver
from selenium.webdriver.chrome.options import Options
import requests

options = Options()
options.headless = True
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.82 Safari/537.36")
driver = webdriver.Chrome(options=options)
driver.maximize_window()
driver.get("https://skinport.com/")
driver.get("https://skinport.com/de/signin")
time.sleep(2)
window_before = driver.window_handles[0]
driver.find_element_by_xpath("//*[@id=\"root\"]/div[1]/div/div[2]/div/div/div[2]/div/button[1]").click()
time.sleep(5)
window_after = driver.window_handles[1]
driver.switch_to.window(window_after)
driver.find_element_by_id("steamAccountName").send_keys("manue_f")  # username
password = input("password please")
driver.find_element_by_id("steamPassword").send_keys(password)  # passwort
time.sleep(1)
driver.find_element_by_id("acceptAllButton").click()
driver.find_element_by_id("imageLogin").click()
time.sleep(2)
tfa = input("2FA please")
driver.find_element_by_id("twofactorcode_entry").send_keys(tfa)  # 2FA Code
driver.find_element_by_xpath("//*[@id=\"login_twofactorauth_buttonset_entercode\"]/div[1]").click()
time.sleep(5)
driver.switch_to.window(window_before)
link = input("Link please")
driver.get(link)
cookies = driver.get_cookies()
headers = []
for i in driver.requests:
    if i.host == "skinport.com":
        try:
            headers.append(i.headers["cookie"])
        except Exception:
            pass
s = requests.Session()
for cookie in cookies:
    s.cookies.set(cookie['name'], cookie['value'])
s.headers.update({"cookie": headers[-1]})
r = s.get("https://skinport.com/api/inventory/account").json()
print(r)
driver.close()
driver.quit()