from discord import SyncWebhook
import telegram_send
import os
import time
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options #For headless
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

#Headless options START
options = Options()
options.add_argument("--headless")
driver = webdriver.Firefox(options=options)
#Headless options END
# driver = webdriver.Firefox()
webhook = SyncWebhook.from_url("https://discord.com/api/webhooks/...")
webhook_error = SyncWebhook.from_url("https://discord.com/api/webhooks/...")
os.environ["TZ"] = "Asia/Kolkata"
time.tzset()
isBookingOpened = False
target_url = "https://in.bookmyshow.com/buytickets/..."
try:
    driver.delete_all_cookies()
    driver.get(target_url)
except Exception as e:
    webhook_error.send("Timeout occurred at page load at "+time.strftime("%I:%M:%S %p"))
    driver.close()
    driver.quit()
    sys.exit(1)
try:
    WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.ID, 'wzrk-cancel')))
except Exception as e:
    webhook_error.send("Timeout occurred at button find at "+time.strftime("%I:%M:%S %p"))
    driver.close()
    driver.quit()
    sys.exit(1)
try:
    button = driver.find_element(By.ID, 'wzrk-cancel')
except Exception as e:
    webhook_error.send("Timeout occurred at button find at "+time.strftime("%I:%M:%S %p"))
    driver.close()
    driver.quit()
    sys.exit(1)
button.click()
try:
    WebDriverWait(driver, 1).until(EC.presence_of_element_located((By.CLASS_NAME, "phpShowtimes showtimes")))
except Exception as e:
    print("")
while isBookingOpened == False:
    try:
        driver.delete_all_cookies()
        driver.get(target_url)
    except Exception as e:
        webhook_error.send("Timeout occurred at page reload at "+time.strftime("%I:%M:%S %p"))
        driver.close()
        driver.quit()
        sys.exit(1)
    try:
        WebDriverWait(driver, 1).until(EC.presence_of_element_located((By.CLASS_NAME, "phpShowtimes showtimes")))
    except Exception as e:
        print("")
    try:
        formats = driver.find_element(By.XPATH, "//*[@id=\"filterLanguage\"]")
    except NoSuchElementException:
        webhook_error.send("Element not found at formats at "+time.strftime("%I:%M:%S %p"))
        print("Element not found!")
        driver.close()
        driver.quit()
        sys.exit(1)
    except Exception:
        webhook_error.send("Exception at find dropdown at "+time.strftime("%I:%M:%S %p"))
        print("Element not found!")
        driver.close()
        driver.quit()
        sys.exit(1)
    try:
        children = int(formats.get_attribute("childElementCount"))
        if children == 1:
            print("Booking for more formats not opened at",time.strftime("%I:%M:%S %p"))
            webhook.send("Booking for more formats not opened at "+time.strftime("%I:%M:%S %p"))
            time.sleep(180)
        else:
            print("Booking for more formats OPENED at",time.strftime("%I:%M:%S %p"))
            for i in range(5):
                telegram_send.send(messages=["Booking for more formats OPENED at BookMyShow\n"+target_url])
                time.sleep(2)
            isBookingOpened = True
            driver.close()
            driver.quit()
    except Exception:
        webhook_error.send("Exception occurred at children get attribute at "+time.strftime("%I:%M:%S %p"))
        driver.close()
        driver.quit()
        sys.exit(1)