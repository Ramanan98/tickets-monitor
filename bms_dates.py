import telegram_send
import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

# options = Options()
# options.add_argument("--headless")
# driver = webdriver.Firefox(options=options)
driver = webdriver.Firefox()
# os.environ["TZ"] = "Asia/Kolkata"
# time.tzset()
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

WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "/html/body/section[1]")))

# header = driver.find_elements(By.XPATH, "//*[@id=\"filterLanguage\"]/*")
header = driver.find_elements(By.XPATH, "//*[@id=\"showDates\"]/div/div/*")
# header = driver.find_element(By.XPATH, "//*div[@class=\"date-day\"]")
# print(header)

print("No. of dates availabe: "+str(len(header))+"\n")

driver.close()