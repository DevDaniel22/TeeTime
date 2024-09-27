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

def main():
    with open('inputs.json') as file:
        data = json.load(file)
    
    email = data['email']
    password = data['password']
    course = data['course']
    date = data['date']
    latest_time = data['latest_time']
    num_people = data['num_people']
    
    options = Options()
    options.add_argument("start-maximized")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    # brings session to login page
    driver.get("https://foreupsoftware.com/index.php/booking/19765/2431#teetimes")

    button = driver.find_element(By.XPATH, "//button[text()='Non Resident']")
    button.click()

    # select the course
    course_select = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "schedule_select"))
    )
    selectCourse = Select(course_select)
    selectCourse.select_by_value(f"{course}")
    
    
    # select the date
    date_field = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "date-field"))
    )
    date_field.clear()
    date_field.send_keys(Keys.CONTROL + "a")  # Select all existing text
    date_field.send_keys(Keys.DELETE)
    date_field.send_keys(date)
    print(date_field.get_attribute('value'))

    time.sleep(10)

    players_div = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "players"))
    )
    selectPlayers = players_div.find_element(By.CSS_SELECTOR, f'a[data-value="{num_people}"]')
    selectPlayers.click()


    time_tiles = driver.find_element_by_class_name("time-tiles")
    first_child = time_tiles.find_element_by_xpath("./*[1]")
    booking_start_time_label = first_child.find_element_by_class_name("booking-start-time-label")
    text = booking_start_time_label.text
    booking_time = datetime.datetime.strptime(text, "%I:%M%p").time()
    if booking_time < latest_time:
        first_child.click()
        print("Button clicked successfully.")
    else:
        print("Booking start time is later than the latest time.")

    

    button = driver.find_element_by_xpath("//button[contains(text(), 'Book Time')]")
    button.click()
    
    email_field = driver.find_element_by_id("login_email")
    email_field.send_keys(email)

    email_field = driver.find_element_by_id("login_password")
    email_field.send_keys(password)

    login_button = driver.find_element_by_xpath("//button[contains(text(), 'Log In')]")
    login_button.click()

    # ends the session
    driver.quit()


main()