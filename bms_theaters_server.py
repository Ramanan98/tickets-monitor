from discord import SyncWebhook
import telegram_send
import os
import time
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

options = Options()
# options.add_argument("--headless")
driver = webdriver.Firefox(options=options)
os.environ["TZ"] = "Asia/Kolkata"
time.tzset()
isBookingOpened = False
webhook = SyncWebhook.from_url("https://discord.com/api/webhooks/...")
webhook_error = SyncWebhook.from_url("https://discord.com/api/webhooks/...")
target_url = "https://in.bookmyshow.com/buytickets/..."
try:
    driver.delete_all_cookies()
    driver.get(target_url)
except Exception as e:
    print("Timeout occurred in theaters")
    webhook_error.send("Timeout occurred at page load at "+time.strftime("%I:%M:%S %p"))
    driver.close()
    driver.quit()
    os.system("rm -rf geckodriver.log")

try:
    WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.ID, 'wzrk-cancel')))
except Exception as e:
    print("Timeout occurred")
    webhook_error.send("Timeout occurred at cancel button at "+time.strftime("%I:%M:%S %p"))
    driver.close()
    driver.quit()
    os.system("rm -rf geckodriver.log")
button = driver.find_element(By.ID, 'wzrk-cancel')
button.click()

while isBookingOpened == False:
    try:
        driver.delete_all_cookies()
        driver.get(target_url)
    except Exception as e:
        print("Timeout occurred in theaters")
        webhook_error.send("Timeout occurred at page reload at "+time.strftime("%I:%M:%S %p"))
        driver.close()
        driver.quit()
        os.system("rm -rf geckodriver.log")
    try:
        availability = driver.find_element(By.XPATH, "//*[@id=\"venuelist\"]//li[@data-name='PVR: Orion Mall, Dr Rajkumar Road']")
        if(availability):
            print("Booking OPENED at",time.strftime("%I:%M:%S %p"))
            for i in range(5):
                telegram_send.send(messages=["Booking opened at BookMyShow!\n"+target_url])
                time.sleep(2)
            isBookingOpened = True
            driver.close()
            driver.quit()
            os.system("rm -rf geckodriver.log")
    except NoSuchElementException:
        isBookingOpened = False
        print("Booking not opened at",time.strftime("%I:%M:%S %p"))
        webhook.send("Booking not opened at "+time.strftime("%I:%M:%S %p"))
        time.sleep(300)
    except Exception:
        webhook_error.send("Exception occurred at availability at "+time.strftime("%I:%M:%S %p"))
        driver.close()
        driver.quit()
        os.system("rm -rf geckodriver.log")
