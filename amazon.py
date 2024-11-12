import time
import re
from amazoncaptcha import AmazonCaptcha
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, ElementClickInterceptedException
from bs4 import BeautifulSoup
import json


def to_snake_case(text):
    return re.sub(r'\W+', '_', text).lower()

# Function to solve captcha


def solve_captcha(driver, max_retries=3):
    for attempt in range(max_retries):
        print(f"Attempt {attempt + 1} to solve captcha")
        driver.get('https://www.amazon.com/errors/validateCaptcha')
        time.sleep(2)

        # Get the captcha image URL and solve it
        image_element = driver.find_element(
            By.CSS_SELECTOR, 'div.a-row.a-text-center img')
        image_url = image_element.get_attribute('src')
        captcha = AmazonCaptcha.fromlink(image_url)
        solution = captcha.solve(keep_logs=True)

        # Input the captcha solution
        input_element = driver.find_element(By.ID, 'captchacharacters')
        input_element.send_keys(solution)

        # Submit the captcha form
        button_element = driver.find_element(
            By.XPATH, "//button[@type='submit' and contains(@class, 'a-button-text') and text()='Continue shopping']")
        button_element.click()

        time.sleep(3)

        # Check if the URL has changed
        current_url = driver.current_url
        if current_url != 'https://www.amazon.com/errors/validateCaptcha':
            print("Captcha solved successfully!")
            return True
        else:
            print("Failed to solve captcha. Retrying...")

    print("Max retries reached. Failed to solve captcha.")
    return False


def fetch_amazon_product_detail(product_url, driver):
    # solve captcha
    if solve_captcha(driver):
        driver.get(product_url)
        time.sleep(5)
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')

        try:
            title = soup.find('h1', {'id': 'title'}).text.strip()
        except:
            title = ""

        try:
            price = soup.find(
                "span", {"class": "a-price"}).find("span").text
        except:
            price = ""

        try:
            images = re.findall('"hiRes":"(.+?)"', html)
        except:
            images = []

        try:
            description = soup.select_one(
                '#productDescription').text.strip()
        except:
            description = ""

        found_data = {
            "title": title,
            "price": price,
            "description": description,
            "images": images
        }

        output_data = {"success": 1, "data": found_data}
        driver.quit()
        return output_data

    else:
        message = "Failed to navigate to the product page due to unsolved captcha."
        output_data = {"success": 0, "message": message}
        driver.quit()
        return output_data
