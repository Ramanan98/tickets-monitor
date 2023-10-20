import telegram_send
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

driver = webdriver.Firefox()
isBookingOpened = False
driver.get("https://www.inoxmovies.com/Movie/Last-Night-In-Soho/23748/sn/4")
WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//*[@id=\"onesignal-slidedown-cancel-button\"]")))
button = driver.find_element(By.ID, 'onesignal-slidedown-cancel-button')
button.click()
WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//*[@id=\"ctl00_divMetroCity\"]/div[4]/div/div[2]")))
city = driver.find_element(By.XPATH, "//*[@id=\"ctl00_divMetroCity\"]/div[4]/div/div[2]")
driver.execute_script("arguments[0].click();", city)
WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, "//*[@id=\"divShowdayBlock_SATURDAY\"]")))
while isBookingOpened == False:
    driver.get("https://www.inoxmovies.com/Movie/Last-Night-In-Soho/23748/sn/4")
    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, "//*[@id=\"divShowdayBlock_SATURDAY\"]")))
    saturday = driver.find_element(By.XPATH, "//*[@id=\"divShowdayBlock_SATURDAY\"]")
    bookingStatus = saturday.get_attribute("class")
    if bookingStatus == 'ShowDayDisable':
        print("Booking not opened at",time.strftime("%I:%M:%S %p"))
        #telegram_send.send(messages=["Booking not opened"])
        time.sleep(10)
        #driver.refresh()
    else:
        print("Booking opened!")
        telegram_send.send(messages=["Booking opened!"])
        isBookingOpened = True
        driver.close()
