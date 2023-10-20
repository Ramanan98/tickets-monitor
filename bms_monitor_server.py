from discord import SyncWebhook
import os
import sys
import telegram_send
import time
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

options = Options()
options.add_argument("--headless")
driver = webdriver.Firefox(options=options)
driver.set_page_load_timeout(20)
webhook = SyncWebhook.from_url("https://discord.com/api/webhooks/...")
webhook_error = SyncWebhook.from_url("https://discord.com/api/webhooks/...")
os.environ["TZ"] = "Asia/Kolkata"
time.tzset()
isBookingOpened = False
target_url = "https://in.bookmyshow.com/bengaluru/movies/guardians-of-the-galaxy-vol-3/ET00310794"
try:
    driver.delete_all_cookies()
    driver.get(target_url)
except Exception:
    webhook_error.send("Timeout occurred at initial page load at "+time.strftime("%I:%M:%S %p"))
    driver.quit()
# try:
#     WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[3]/div[2]")))
# except Exception:
#     telegram_send.send(messages=["Timeout occurred in BMS!"])
# button = driver.find_element(By.ID, 'wzrk-cancel')
# button.click()
try:
    WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[1]/div[1]/div[2]/section[1]")))
except Exception:
    webhook_error.send("Timeout occurred at banner find at "+time.strftime("%I:%M:%S %p"))
    driver.quit()
while isBookingOpened == False:
    try:
        driver.delete_all_cookies()
        driver.get(target_url)
    except Exception:
        webhook_error.send("Timeout occurred at page reload at "+time.strftime("%I:%M:%S %p"))
    try:
        WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[1]/div[1]/div[2]/section[1]")))
    except Exception:
        webhook_error.send("Timeout occurred at banner find at "+time.strftime("%I:%M:%S %p"))
        driver.close()
        driver.quit()
    try:
        book_tickets_button = driver.find_element(By.XPATH, "//*[@id=\"page-cta-container\"]/button/div")
        if(book_tickets_button):
            for i in range(5):
                telegram_send.send(messages=["Booking opened at BookMyShow!\n"+target_url])
                time.sleep(2)
            print("Booking OPENED at",time.strftime("%I:%M:%S %p"))
            isBookingOpened = True
            driver.close()
            driver.quit()
            sys.exit(1)
    except NoSuchElementException:
        isBookingOpened = False
        print("Booking not opened at",time.strftime("%I:%M:%S %p"))
        webhook.send("Booking not opened at "+time.strftime("%I:%M:%S %p"))
        time.sleep(180)
    except Exception:
        webhook_error.send("Exception occurred at book tickets button at "+time.strftime("%I:%M:%S %p"))
        driver.close()
        driver.quit()
        sys.exit(1)