import time
import random
import json
import sys
from selenium_recaptcha_solver import RecaptchaSolver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, ElementClickInterceptedException
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager



def fetch_alibaba_product_detail(product_url, driver):
    driver.get(product_url)
    # Wait until the username and password fields are visible
    try:
        # Introduce a random delay to mimic human behavior
        time.sleep(random.uniform(2, 5))

        try:
            title = driver.find_element(By.CSS_SELECTOR, ".product-title-container h1").text
        except:
            title = "N/A"
        
        # Extract product price
        try:
            price = driver.find_element(By.CSS_SELECTOR, ".product-price .price-item .price span").text
        except:
            price = "N/A"

        # Extract product description (usually in a div element)
        try:
            description = driver.find_element(By.CSS_SELECTOR, "div.product-description").text
        except:
            description = "N/A"
        
        # Extract product images
        images = []
        try:
            image_elements = driver.find_elements(By.CSS_SELECTOR, '.module_productImage div[data-com="ProductImageView"] img')
            for img in image_elements:
                images.append(img.get_attribute("src"))
        except:
            images = []

        # Extract product variants (if any)
        variants = []
        try:
            variant_elements = driver.find_elements(By.CSS_SELECTOR, ".sku-info .info-item > a.text")
            for variant in variant_elements:
                variants.append(variant.text)
        except:
            variants = []

        # Return the scraped product data
        found_data = {
            "title": title,
            "price": price,
            "description": description,
            "images": images,
            # "variants": variants
        }
        output_data = {"success":1,"data":found_data}
        return output_data
    except TimeoutException:
        message = "Timeout waiting for login form fields to be visible."
        output_data = {"success":0,"message":message}
        return output_data
    finally:
        if driver:
            driver.quit()