import schedule
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from dotenv import load_dotenv
from datetime import datetime
from dateutil import parser
import os
import yagmail

def parse_into_datetime_obj(date_string):
    date_string_cleaned = date_string.replace("st,", ",").replace("nd,", ",").replace("rd,", ",").replace("th,", ",")
    return parser.parse(date_string_cleaned)

def run_selenium_script():
    print("Running Selenium script...")

    load_dotenv()

    try:
        service = Service(executable_path="chromedriver.exe")
        driver = webdriver.Chrome(service=service)

        driver.get("https://onlinebusiness.icbc.com/webdeas-ui/login;type=driver")

        # sign in page
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, "mat-input-0")))

        last_name = driver.find_element(By.ID, "mat-input-0")
        last_name.send_keys(os.getenv("LAST_NAME"))

        license_number = driver.find_element(By.ID, "mat-input-1")
        license_number.send_keys(os.getenv("LICENSE_NUMBER"))

        keyword = driver.find_element(By.ID, "mat-input-2")
        keyword.send_keys(os.getenv("KEYWORD"))

        checkbox = driver.find_element(By.CSS_SELECTOR, ".mat-checkbox-inner-container")
        checkbox.click()

        sign_in = driver.find_element(By.CSS_SELECTOR, "button.primary")
        sign_in.click()

        # home page
        appointment_box = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".dynamic-appointment-wrapper.appointment-panel.ng-star-inserted"))
        )
        current_appointment_date = appointment_box.find_element(By.CSS_SELECTOR, ".content").text
        print(f"Current appointment: {current_appointment_date}")
        
        buttons = appointment_box.find_element(By.CSS_SELECTOR, ".mat-dialog-actions.button-group")
        reschedule = buttons.find_element(By.CSS_SELECTOR, ".raised-button.primary")
        reschedule.click()

        parent_div = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".form-control.cancel-action-buttons"))
        )
        confirm = parent_div.find_element(By.CSS_SELECTOR, '.primary.ng-star-inserted')
        confirm.click()

        # choose location
        select_location = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, '//*[@formcontrolname="finishedAutocomplete"]'))
        )
        select_location.send_keys("burn")
        time.sleep(2)
        select_location.send_keys("aby")
        time.sleep(1)
        select_location.send_keys(Keys.ARROW_DOWN)
        time.sleep(1)
        select_location.send_keys(Keys.ENTER + Keys.ENTER)

        ICBC_location = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".first-office-container"))
        )
        ICBC_location.click()

        # get the first and earliest appointment
        new_appointment_date = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".date-title"))
        ).text
        new_appointment_time_button = driver.find_element(By.CSS_SELECTOR, ".mat-button-toggle-button.mat-focus-indicator")
        new_appointment_time = new_appointment_time_button.find_element(By.CSS_SELECTOR, ".mat-button-toggle-label-content").text

        # send email if an earlier appointment time is found
        if parse_into_datetime_obj(current_appointment_date) > parse_into_datetime_obj(new_appointment_date):
            print(f"There's an earlier appointment: {new_appointment_date}")
            yag = yagmail.SMTP(os.getenv("EMAIL"), os.getenv("PASSWORD"))
            yag.send(os.getenv("EMAIL"), "Earlier road test appointment found!", f"New appointment: {new_appointment_date} at {new_appointment_time}")
        else:
            print("No earlier appointment found")
            print(f"Potential new appointment: {new_appointment_date} at {new_appointment_time}")
        new_appointment_time_button.click()

    except Exception as e:
        print(f"An error occurred: {e}")
    
    finally:
        driver.quit()

# Schedule the script to run every 10 minutes
schedule.every(10).minutes.do(run_selenium_script)

print("Scheduler started. Running every 10 minutes...")
try:
    while True:
        schedule.run_pending()
        time.sleep(60)  # Check every minute
except KeyboardInterrupt:
    print("Stopped by user")
