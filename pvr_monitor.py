from discord import Webhook, RequestsWebhookAdapter
import telegram_send
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import WebDriverException

driver = webdriver.Firefox()
webhook = Webhook.from_url("https://discord.com/api/webhooks/...", adapter=RequestsWebhookAdapter())
isBookingOpened = False
target_url = "https://www.pvrcinemas.com/moviesessions/Coimbatore/SPIDER-MAN-NO-WAY-HOME/NHO00017923"
try:
    driver.get(target_url)
except WebDriverException as wb:
    print("Check internet")
    webhook.send("Check internet")
try:
    WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, "//*[@id=\"main__wrapper\"]/app-root/app-full-layout/nav/div/div[1]/div/div/div[2]/div[1]")))
except TimeoutException as toe:
    telegram_send.send(messages=["Timeout occurred!"])
while isBookingOpened == False:
    try:
        driver.get(target_url)
    except Exception as wb:
        print("Check internet")
        webhook.send("Check internet")
    try:
        WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, "//*[@id=\"main__wrapper\"]/app-root/app-full-layout/nav/div/div[1]/div/div/div[2]/div[1]")))
    except Exception as toe:
        print("Timeout occurred!")
        telegram_send.send(messages=["Timeout occurred in PVR!"])
        url = "https://www.pvrcinemas.com"
    else:
        url = driver.current_url
        print(url)
    if "moviesessions" in url:
        isBookingOpened = True
        print("Booking OPENED at PVR",time.strftime("%I:%M:%S %p"))
        for i in range(10):
            telegram_send.send(messages=["Booking opened at PVR!\n"+target_url])
            time.sleep(2)
        driver.close()
    else:
        isBookingOpened = False
        print("Booking not opened at",time.strftime("%I:%M:%S %p"))
        webhook.send("Booking not opened at "+time.strftime("%I:%M:%S %p"))
        time.sleep(90)
