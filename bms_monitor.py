from discord import SyncWebhook
import telegram_send
import time
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.by import By
# from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# options = Options()
# options.add_argument("--headless")
# driver = webdriver.Firefox(options=options)
driver = webdriver.Firefox()
webhook = SyncWebhook.from_url("https://discord.com/api/webhooks/...")
isBookingOpened = False
target_url = "https://in.bookmyshow.com/bengaluru/movies/indiana-jones-and-the-dial-of-destiny/ET00346122"
try:
    driver.delete_all_cookies()
    driver.get(target_url)
except WebDriverException as wb:
    print("Check internet")
    driver.quit()
# try:
#     WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[3]/div[2]")))
# except TimeoutException as toe:
#     telegram_send.send(messages=["Timeout occurred in BMS!"])
# button = driver.find_element(By.ID, 'wzrk-cancel')
# button.click()
try:
    WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[1]/div[1]/div[2]/section[1]")))
except TimeoutException as toe:
    telegram_send.send(messages=["Timeout occurred in BMS!"])
    driver.quit()
while isBookingOpened == False:
    try:
        driver.delete_all_cookies()
        driver.get(target_url)
    except WebDriverException as wb:
        print("Check internet")
        driver.quit()
    try:
        WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[1]/div[1]/div[2]/section[1]")))
    except TimeoutException as toe:
        telegram_send.send(messages=["Timeout occurred in BMS!"])
        driver.quit()
    try:
        book_tickets_button = driver.find_element(By.XPATH, "//*[@id=\"page-cta-container\"]/button/div")
    except NoSuchElementException:
        isBookingOpened = False
        print("Booking not opened at",time.strftime("%I:%M:%S %p"))
        webhook.send("Booking not opened at "+time.strftime("%I:%M:%S %p"))
        time.sleep(5)
    else:
        for i in range(5):
            telegram_send.send(messages=["Booking opened at BookMyShow!\n"+target_url])
            time.sleep(2)
        isBookingOpened = True
        driver.quit()