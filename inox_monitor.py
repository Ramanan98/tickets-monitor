from discord import Webhook, RequestsWebhookAdapter
import telegram_send
import time
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

driver = webdriver.Firefox()
webhook = Webhook.from_url("https://discord.com/api/webhooks/...", adapter=RequestsWebhookAdapter())
isBookingOpened = False
target_url = "https://www.inoxmovies.com/Movie/Spider-man-No-Way-Home/24121/sn/4"
try:
    driver.get(target_url)
except WebDriverException as wb:
    print("Check internet")
    webhook.send("Check internet")
try:
    WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, "//*[@id=\"onesignal-slidedown-cancel-button\"]")))
except TimeoutException as toe:
    telegram_send.send(messages=["Timeout occurred in INOX!"])
    driver.close()
button = driver.find_element(By.ID, 'onesignal-slidedown-cancel-button')
button.click()
try:
    WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, "//*[@id=\"ctl00_divMetroCity\"]/div[4]/div/div[2]")))
except TimeoutException as toe:
    telegram_send.send(messages=["Timeout occurred in INOX!"])
    driver.close()
city = driver.find_element(By.XPATH, "//*[@id=\"ctl00_divMetroCity\"]/div[4]/div/div[2]")
driver.execute_script("arguments[0].click();", city)
try:
    WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, "//*[@id=\"ctl00_ContentPlaceHolder1_divShowTheater\"]")))
except TimeoutException as toe:
    telegram_send.send(messages=["Timeout occurred in INOX!"])
while isBookingOpened == False:
    try:
        driver.get(target_url)
    except WebDriverException as wb:
        print("Check internet")
        webhook.send("Check internet")
    try:
        WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, "//*[@id=\"ctl00_ContentPlaceHolder1_divShowTheater\"]")))
    except TimeoutException as toe:
        telegram_send.send(messages=["Timeout occurred in INOX!"])
        driver.close()
    selector = driver.find_element(By.XPATH, "//*[@id=\"ctl00_ContentPlaceHolder1_divShowTheater\"]")
    bookingStatus = selector.get_attribute("style")
    if bookingStatus == "margin: 0px; display: none;":
        print("Booking not opened at",time.strftime("%I:%M:%S %p"))
        webhook.send("Booking not opened at "+time.strftime("%I:%M:%S %p"))
        time.sleep(90)
        #driver.refresh()
    else:
        print("Booking OPENED at",time.strftime("%I:%M:%S %p"))
        for i in range(10):
            telegram_send.send(messages=["Booking opened at INOX!\n"+target_url])
            time.sleep(2)
        isBookingOpened = True
        driver.close()
