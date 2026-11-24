import os
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

BASE_URL = os.environ.get("BASE_URL", "http://localhost:8090")


@pytest.fixture
def driver():
    options = Options()
    options.binary_location = "/usr/bin/chromium"
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1280,800")
    options.add_argument("--user-data-dir=/tmp/chrome-profile")
    drv = webdriver.Chrome(service=Service("/usr/bin/chromedriver"), options=options)
    yield drv
    drv.quit()


def test_title_contains_roll_number(driver):
    driver.get(BASE_URL)
    assert "FA23-BSE-082" in driver.title


def test_heading_and_student_details(driver):
    driver.get(BASE_URL)
    heading = driver.find_element(By.ID, "page-heading").text
    student = driver.find_element(By.ID, "student-name").text
    roll = driver.find_element(By.ID, "roll-number").text
    assert heading == "Cloud Computing CI/CD Pipeline Portal"
    assert "Muhammad Usman" in student
    assert "FA23-BSE-082" in roll


def test_button_click_shows_message(driver):
    driver.get(BASE_URL)
    driver.find_element(By.ID, "status-btn").click()
    WebDriverWait(driver, 5).until(
        EC.text_to_be_present_in_element((By.ID, "status-msg"), "Pipeline Active")
    )
    assert driver.find_element(By.ID, "status-msg").text == "Pipeline Active - Verified by Selenium!"


def test_textbox_submit_displays_text(driver):
    driver.get(BASE_URL)
    driver.find_element(By.ID, "status-btn").click()
    note_input = driver.find_element(By.ID, "note-input")
    note_input.clear()
    note_input.send_keys("Hello from FA23-BSE-082")
    driver.find_element(By.ID, "submit-btn").click()
    WebDriverWait(driver, 5).until(
        EC.text_to_be_present_in_element((By.ID, "submitted-output"), "Hello from FA23-BSE-082")
    )
    assert driver.find_element(By.ID, "submitted-output").text == "Submitted: Hello from FA23-BSE-082"
    driver.save_screenshot("screenshot.png")
