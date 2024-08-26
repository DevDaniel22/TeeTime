from selenium import webdriver
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
    
    driver = webdriver.Chrome()
    # brings session to login page
    driver.get("https://foreupsoftware.com/index.php/booking/19765/2431#teetimes")
    button = driver.find_element_by_xpath("//button[contains(text(), 'Verified NYS Resident - Bethpage Only')]")
    button.click()

    button = driver.find_element_by_xpath("//button[contains(text(), 'Log In')]")
    button.click()

    email_field = driver.find_element_by_id("login_email")
    email_field.send_keys(email)

    email_field = driver.find_element_by_id("login_password")
    email_field.send_keys(password)

    # TODO: click the actual login button
    login_button = driver.find_element_by_xpath("//button[contains(text(), 'Log In')]")
    login_button.click()

    # select course, date, time, number of people
    course_select = driver.find_element_by_id("schedule_select")
    course_option = course_select.find_element_by_xpath(f"//option[text()='{course}']")
    course_option.click()

    course_select = driver.find_element_by_id("date-menu")
    course_option = course_select.find_element_by_xpath(f"//option[text()='{date}']")
    course_option.click()

    players_div = driver.find_element_by_xpath("//div[@label='Players']")
    link = players_div.find_element_by_xpath(f"//a[@data-value='{num_people}']")
    link.click()
    # TODO: check if any tiles exist, if not refresh and wait for them to appear

    while driver.find_element_by_id("times-empty") or booking_time >= latest_time:
        driver.refresh()
        time_tiles = driver.find_element_by_class_name("time-tiles")
        first_child = time_tiles.find_element_by_xpath("./*[1]")
        booking_start_time_label = first_child.find_element_by_class_name("booking-start-time-label")
        text = booking_start_time_label.text
        booking_time = datetime.datetime.strptime(text, "%I:%M%p").time()

    first_child.click()

    button = driver.find_element_by_xpath("//button[contains(text(), 'Book Time')]")
    button.click()
    # ends the session
    driver.quit()


