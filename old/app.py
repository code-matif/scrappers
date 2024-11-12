# app.py
from generate_product import get_product
from generate_product_description import get_product_description
from generate_product_reviews import get_product_reviews

from amazon import fetch_amazon_product_detail
from aliexpress import fetch_aliexpress_product_detail
from alibaba import fetch_alibaba_product_detail
from shopify import fetch_shopify_product_detail
from flask import Flask, request, jsonify

import time
import random
import sys
from selenium_recaptcha_solver import RecaptchaSolver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, ElementClickInterceptedException
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import json

# A list of different User-Agent strings to rotate between
user_agents = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/11.1 Safari/605.1.15',
    'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0'
]


app = Flask(__name__)


@app.route('/product-details', methods=['POST'])
def product_details():
    data = request.json
    product_url = data['product_url']
    store_name = data['store_name']

    if not store_name or store_name is None or store_name == "":
        return jsonify({"success": False, "message": "Store Name is required"})

    if not product_url or product_url is None or product_url == "":
        return jsonify({"success": False, "message": "Product URL is required"})

    driver = get_driver()

    response = {}

    match store_name:
        case "alibaba":
            response = fetch_alibaba_product_detail(product_url, driver)
        case "shopify":
            response = fetch_shopify_product_detail(product_url)
        case "aliexpress":
            response = fetch_aliexpress_product_detail(product_url, driver)
        case "amazon":
            response = fetch_amazon_product_detail(product_url, driver)
        case _:
            response = {"success": False, "message": "Store not supported"}

    if "images" in response['data'] and isinstance(response['data']["images"], list):
        response['data']["images"] = response['data']["images"][:5]

    # Generate 4 product variants using OpenAI
    if response.get('success', False):
        product = generate_product_details(response['data'])
        response['data'] = product

    time.sleep(2)
    return jsonify(response)


def generate_product_details(data):

    des = data.get('description', 'Not Available')
    title = data.get('title', 'Not Available')
    images = data.get('images', [])
    tone = "playful"
    language = "en"

    customPrompt = "Make it more appealing to eco-conscious consumers."
    product = get_product(images, customPrompt, tone, language, title, des)
    product["images"] = images


    description = product.get('description', 'Not Available')
    product_title = product.get('title', 'Not Available')
    descriptions = []
    reviews = []
    i = 0
    for img in images:
        prompt = "Generate a playful description of this product"
        result = get_product_description(img, prompt, tone, language)
        result["image"] = img
        descriptions.append(result)

        # generating reviews
        review = get_product_reviews(
            img, tone, language, product_title, description)
        review["image"] = img
        reviews.append(review)

    product["reviews"] = reviews
    product["descriptions"] = descriptions

    return product


def get_driver(headless=True):
    # Set up Chrome options
    options = webdriver.ChromeOptions()
    options.add_argument("--window-size=1920,1080")
    # Rotate user-agent
    options.add_argument(f'--user-agent={random.choice(user_agents)}')
    options.add_argument('--no-sandbox')

    if headless:
        options.add_argument("--headless")

    options.add_argument("--disable-extensions")
    # Avoid Selenium detection
    options.add_argument("--disable-blink-features=AutomationControlled")
    # Disable "Chrome is being controlled by automated software" info bar
    options.add_argument("--disable-infobars")
    options.add_experimental_option(
        "useAutomationExtension", False)  # Disable extension
    # Exclude automation switches
    options.add_experimental_option("excludeSwitches", ["enable-automation"])

    # Use WebDriver Manager to manage ChromeDriver installation
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)

    # Evade detection by modifying navigator.webdriver property
    driver.execute_script(
        "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

    # Clear cookies to avoid being tracked
    driver.delete_all_cookies()
    return driver


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080, debug=True, threaded=True)
