# from discord import Webhook, RequestsWebhookAdapter
import telegram_send
import time
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

driver = webdriver.Firefox()
isBookingOpened = False
target_url = "https://in.bookmyshow.com/buytickets/..."
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

# time.sleep(5)
# try:
#     WebDriverWait(driver, 20).until(EC._element_if_visible((By.XPATH, "/html/body/div[5]/section[2]/div[3]/div")))
# except Exception as e:
#     print("Timeout occurred")
#     telegram_send.send(messages=["Timeout occurred in BMS"])
#     driver.quit()

while isBookingOpened == False:
    try:
        driver.get(target_url)
    except Exception as e:
        print("Check internet")
    # time.sleep(5)
    # try:
    #     WebDriverWait(driver, 20).until(EC._element_if_visible((By.XPATH, "/html/body/div[5]/section[2]/div[3]/div")))
    # except Exception as e:
    #     print("Timeout occurred")
    #     telegram_send.send(messages=["Timeout occurred in BMS"])
    #     driver.quit()
    try:
        availability = driver.find_element(By.XPATH, "//*[@id=\"venuelist\"]//li[@data-name='INOX: Prozone Mall, Coimbatore']")
    except NoSuchElementException:
        isBookingOpened = False
        print("Booking not opened at",time.strftime("%I:%M:%S %p"))
        # webhook.send("Booking not opened at "+time.strftime("%I:%M:%S %p"))
        time.sleep(5)
    else:
        print("Booking OPENED at",time.strftime("%I:%M:%S %p"))
        for i in range(5):
            telegram_send.send(messages=["Booking opened at BookMyShow!\n"+target_url])
            time.sleep(2)
        isBookingOpened = True
        driver.quit()
