import telegram_send
import time
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options #For headless
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

#Headless options START
# options = Options()
# options.headless = True
# driver = webdriver.Firefox(options=options)
driver = webdriver.Firefox()
#Headless options END
isBookingOpened = False
target_url = "https://in.bookmyshow.com/buytickets/..."
try:
    driver.get(target_url)
except Exception as e:
    print("Check internet")
try:
    WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[19]/div[2]/div[2]")))
except Exception as e:
    print("Timeout occurred")
    telegram_send.send(messages=["Timeout occurred in BMS"])
button = driver.find_element(By.ID, 'wzrk-cancel')
button.click()
try:
    WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "/html/body/section[1]")))
except Exception as e:
    print("Timeout occurred")
    telegram_send.send(messages=["Timeout occurred in BMS"])
while isBookingOpened == False:
    try:
        driver.get(target_url)
    except Exception as e:
        print("Check internet")
    try:
        WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "/html/body/section[1]")))
    except Exception as e:
        print("Timeout occurred")
        telegram_send.send(messages=["Timeout occurred in BMS"])
    try:
        formats = driver.find_element(By.XPATH, "//*[@id=\"filterLanguage\"]")
    except NoSuchElementException:
        print("Element not found!")
        telegram_send.send(messages=["Element not found!"])
    children = int(formats.get_attribute("childElementCount"))
    if children == 1:
        print("Booking for more formats not opened at",time.strftime("%I:%M:%S %p"))
        time.sleep(60)
    else:
        print("Booking for more formats OPENED at",time.strftime("%I:%M:%S %p"))
        for i in range(5):
            telegram_send.send(messages=["Booking opened at BookMyShow!\n"+target_url])
            time.sleep(2)
        isBookingOpened = True
        driver.close()