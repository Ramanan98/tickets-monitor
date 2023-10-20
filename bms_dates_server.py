from discord import SyncWebhook
import os
import telegram_send
import time
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

options = Options()
options.add_argument("--headless")
driver = webdriver.Firefox(options=options)
driver.set_page_load_timeout(20)
# driver = webdriver.Firefox()
webhook = SyncWebhook.from_url("https://discord.com/api/webhooks/...")
os.environ["TZ"] = "Asia/Kolkata"
time.tzset()
isBookingOpened = False
target_url = "https://in.bookmyshow.com/buytickets/black-adam/..."

try:
    driver.get(target_url)
except Exception as e:
    print("Check internet")
try:
    WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.ID, 'wzrk-cancel')))
except Exception as e:
    print("Timeout occurred")
    telegram_send.send(messages=["Timeout occurred in BMS"])

button = driver.find_element(By.ID, 'wzrk-cancel')
button.click()

WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "/html/body/section[1]")))

while isBookingOpened == False:
    try:
        driver.get(target_url)
    except WebDriverException as wb:
        print("Check internet")
        telegram_send.send(messages=["Internet exception occurred in Black Adam"])
        driver.quit()
    try:
        WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "/html/body/section[1]")))
    except TimeoutException as toe:
        telegram_send.send(messages=["Timeout occurred in Black Adam!"])
        driver.quit()
    header = driver.find_elements(By.XPATH, "//*[@id=\"showDates\"]/div/div/*")
    days_open = int(len(header))
    if days_open == 1:
        print("Booking not opened at",time.strftime("%I:%M:%S %p"))
        webhook.send("Booking for Black Adam not opened at "+time.strftime("%I:%M:%S %p"))
        time.sleep(240)
    else:
        print("Booking OPENED at",time.strftime("%I:%M:%S %p"))
        for i in range(5):
            telegram_send.send(messages=["Friday booking opened for Black Adam!\n"+target_url])
            time.sleep(2)
        isBookingOpened = True
        driver.quit()