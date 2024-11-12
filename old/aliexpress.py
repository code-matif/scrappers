import time
import random
from selenium_recaptcha_solver import RecaptchaSolver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, ElementClickInterceptedException
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager


def fetch_aliexpress_product_detail(product_url, driver):
    product_details = {}
    driver.get(product_url)

    # Wait until the username and password fields are visible
    try:
        # Introduce a random delay to mimic human behavior
        time.sleep(random.uniform(2, 5))
        is_recaptcha_on = True
        try:
            WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'h1[data-pl="product-title"]'))
            )
            is_recaptcha_on = False
        except TimeoutException:
            is_recaptcha_on = True
        if is_recaptcha_on:
            try:
                print("waiting for CAPTCHA iframe.")
                error_banner = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, '//iframe[@title="reCAPTCHA"]'))
                )
                print("CAPTCHA required. Solving CAPTCHA...")

                # Locate the reCAPTCHA iframe and solve it
                recaptcha_solved = False
                try:
                    print("CAPTCHA before iframe.")
                    recaptcha_iframe = driver.find_element(By.XPATH, '//iframe[@title="reCAPTCHA"]')

                    # Solve the CAPTCHA using the visual method
                    print("CAPTCHA before solving visual.",recaptcha_iframe)
                    solver.click_recaptcha_v2(iframe=recaptcha_iframe)

                    # Wait a bit to let the CAPTCHA solve
                    time.sleep(random.uniform(2, 5))
                    driver.switch_to.frame(recaptcha_iframe)
                    # Check if the CAPTCHA checkbox is checked
                    print("CAPTCHA before checkbox.")
                    checkbox = driver.find_element(By.ID, "recaptcha-anchor")
                    if "recaptcha-checkbox-checked" in checkbox.get_attribute("class"):
                        recaptcha_solved = True
                        print("CAPTCHA solved successfully.")
                    else:
                        print("CAPTCHA not solved, retrying...")

                except NoSuchElementException:
                    print("Failed to locate reCAPTCHA iframe or checkbox.")

            except TimeoutException:
                # print("Error banner not found, but URL did not change. outter")
                recaptcha_solved = True
        
        if recaptcha_solved or not is_recaptcha_on:
            try:
                title = driver.find_element(By.CSS_SELECTOR, 'h1[data-pl="product-title"]').text
            except:
                title = "N/A"
            
            # Extract product price
            try:
                price = driver.find_element(By.CSS_SELECTOR, ".product-price-value").text
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
                variant_elements = driver.find_elements(By.CSS_SELECTOR, 'div[data-sku-col] span')
                for variant in variant_elements:
                    variants.append(variant.text)
            except:
                variants = []

            # Close the browser
            driver.quit()

            # Return the scraped product data
            found_data = {
                'title': title,
                'price': price,
                'description': description,
                'images': images,
                'variants': variants
            }

       
        output_data = {'success':1,'data':found_data}
        return output_data
        
    except TimeoutException:
        message = "Timeout waiting for login form fields to be visible."
        output_data = {'success':0,'message':message}
        return output_data
        print("Timeout waiting for login form fields to be visible.")
    finally:
        if driver:
            driver.quit()
