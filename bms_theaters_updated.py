from discord import SyncWebhook
import telegram_send
import time
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# options = Options()
# options.add_argument("--headless")
# driver = webdriver.Firefox(options=options)
# os.environ["TZ"] = "Asia/Kolkata"
# time.tzset()
driver = webdriver.Firefox()
webhook = SyncWebhook.from_url("https://discord.com/api/webhooks/...")
isBookingOpened = False
target_url = "https://in.bookmyshow.com/buytickets/..."

try:
    driver.get(target_url)
except WebDriverException as wb:
    print("Check internet")


try:
    WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[1]/div[1]/div[2]/section[1]")))
except TimeoutException as toe:
    telegram_send.send(messages=["Timeout occurred in BMS!"])
    driver.quit()

book_tickets_button = driver.find_element(By.XPATH, "//*[@id=\"page-cta-container\"]/button/div")
book_tickets_button.click()

# try:
#     WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//*[@id=\"super-container\"]/div[2]/div/div[2]/div/div/ul/li/section[2]/div[2]")))
# except TimeoutException as toe:
#     telegram_send.send(messages=["Timeout occurred in BMS!"])
#     driver.quit()

# imax_button = driver.find_element(By.XPATH, "//*[@id=\"super-container\"]/div[2]/div/div[2]/div/div/ul/li/section[2]/div[2]")
# imax_button.click()

try:
    WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[20]/div[2]")))
except TimeoutException as toe:
    telegram_send.send(messages=["Timeout occurred in BMS!"])

try:
    WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.ID, "wzrk-cancel")))
except Exception:
    telegram_send.send(messages=["Timeout occurred in BMS!"])
cancel_button = driver.find_element(By.ID, 'wzrk-cancel')
cancel_button.click()

try:
    WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "/html/body/section[1]/div[3]/div")))
except TimeoutException as toe:
    telegram_send.send(messages=["Timeout occurred in BMS!"])
    driver.quit()

# Change last characters of the xpath for other days
# try:
#     sat_button = driver.find_element(By.XPATH, "//div[contains(@class, 'date-day') and normalize-space(text()) = 'Sat']")
# except NoSuchElementException:
#     telegram_send.send(messages=["Date cannot be found!"])
#     driver.quit()

# sat_button.click()

try:
    WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "/html/body/section[1]/div[3]/div")))
except TimeoutException as toe:
    telegram_send.send(messages=["Timeout occurred in BMS!"])
    driver.quit()

try_url = driver.current_url

while isBookingOpened == False:
    try:
        driver.get(try_url)
    except Exception as e:
        print("Check internet")
    try:
        WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "/html/body/section[1]")))  # noqa: E501
    except Exception as e:
        print("Timeout occurred")
        telegram_send.send(messages=["Timeout occurred in BMS"])
        driver.quit()
    try:
        availability = driver.find_element(By.XPATH, "//*[@id=\"venuelist\"]//li[@data-name='PVR: Nexus (Formerly Forum), Koramangala']")
        # sat_button = driver.find_element(By.XPATH, "//div[contains(@class, 'date-day') and normalize-space(text()) = 'Sat']")
    except NoSuchElementException:
        isBookingOpened = False
        print("Booking not opened at",time.strftime("%I:%M:%S %p"))
        webhook.send("Booking not opened at "+time.strftime("%I:%M:%S %p"))
        time.sleep(5)
    else:
        print("Booking OPENED at",time.strftime("%I:%M:%S %p"))
        for i in range(5):
            telegram_send.send(messages=["Booking opened at BookMyShow!\n"+target_url])
            time.sleep(2)
        isBookingOpened = True
        driver.quit()