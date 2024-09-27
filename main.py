from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
import datetime
import time
import json
from datetime import datetime, timedelta
import pytz

def main():
    with open('inputs.json') as file:
        data = json.load(file)
    
    email = data['email']
    password = data['password']
    course = data['course']
    date = data['date']
    timeIn = data['timeIn']
    num_people = data['num_people']
    
    options = Options()
    options.add_argument("start-maximized")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.get("https://foreupsoftware.com/index.php/booking/19765/2431#teetimes")

    button = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//button[text()='Verified NYS Resident - Bethpage Only']"))
    )
    button.click()
    button = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//button[text()='Log In']"))
    )
    button.click()
    email_field = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "login_email"))
    )
    email_field.send_keys(email)

    password_field = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "login_password"))
    )
    password_field.send_keys(password)

    # TODO: click the actual login button
    login_button =  WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//button[@data-loading-text='Logging In...']"))
    )
    login_button.click()

    # select course, date, time, number of people
    course_select = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "schedule_select"))
    )
    selectCourse = Select(course_select)
    selectCourse.select_by_value(f"{course}")
    
    est = pytz.timezone('US/Eastern')

    # Get the current time in UTC
    now_utc = datetime.now(pytz.utc)

    # Get the current time in EST
    now_est = now_utc.astimezone(est)
    target_time_est = now_est.replace(hour=17, minute=44, second=0, microsecond=0)

    # Calculate the time difference in seconds
    time_difference = (target_time_est - now_est).total_seconds()

    # Wait until the exact time
    time.sleep(time_difference)






    # select the date
    date_field = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "date-field"))
    )
    date_field.clear()
    date_field.send_keys(Keys.CONTROL + "a")  # Select all existing text
    date_field.send_keys(Keys.DELETE)
    date_field.send_keys(date)

    players_div = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "players"))
    )
    selectPlayers = players_div.find_element(By.CSS_SELECTOR, f'a[data-value="{num_people}"]')
    selectPlayers.click()

    time_div = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "js-time-filter"))
    )
    button = time_div.find_element(By.CSS_SELECTOR, f'a[data-value="{timeIn}"]')
    button.click()


    first_tile = WebDriverWait(driver, 40).until(
        EC.presence_of_element_located((By.CLASS_NAME, "time-tile"))
    )
    first_tile.click()


    players_div = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "js-booking-field-buttons"))
    )
    selectPlayers = players_div.find_element(By.CSS_SELECTOR, f'a[data-value="{num_people}"]')
    selectPlayers.click()
    # button = driver.find_element(By.XPATH, "//button[contains(text(), 'Book Time')]")
    # button.click()
    time.sleep(7)



main()
