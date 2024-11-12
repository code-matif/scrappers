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

# A list of different User-Agent strings to rotate between
user_agents = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/11.1 Safari/605.1.15',
    'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0'
]

# Set up Chrome options
options = webdriver.ChromeOptions()
options.add_argument("--window-size=1920,1080")
options.add_argument(f'--user-agent={random.choice(user_agents)}')  # Rotate user-agent
options.add_argument('--no-sandbox')
options.add_argument("--headless")
options.add_argument("--disable-extensions")
options.add_argument("--disable-blink-features=AutomationControlled")  # Avoid Selenium detection
options.add_argument("--disable-infobars")  # Disable "Chrome is being controlled by automated software" info bar
options.add_experimental_option("useAutomationExtension", False)  # Disable extension
options.add_experimental_option("excludeSwitches", ["enable-automation"])  # Exclude automation switches

# Use WebDriver Manager to manage ChromeDriver installation
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)

# Evade detection by modifying navigator.webdriver property
driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

# Clear cookies to avoid being tracked
driver.delete_all_cookies()

# Initialize the Recaptcha Solver
solver = RecaptchaSolver(driver=driver)

# Open the Poshmark login page
driver.get('https://poshmark.com/login')

# Wait until the username and password fields are visible
try:
    WebDriverWait(driver, 20).until(
        EC.visibility_of_element_located((By.ID, "login_form_username_email"))
    )
    WebDriverWait(driver, 20).until(
        EC.visibility_of_element_located((By.ID, "login_form_password"))
    )

    # Fill in the login form
    driver.find_element(By.ID, "login_form_username_email").send_keys("mjyip")
    driver.find_element(By.ID, "login_form_password").send_keys("%@FywQ@nec5u4.X")

    # Introduce a random delay to mimic human behavior
    time.sleep(random.uniform(2, 5))

    # Capture the current URL before submission
    initial_url = driver.current_url

    # Click the submit button
    driver.find_element(By.XPATH, '//button[@type="submit"]').click()

    # Wait for URL change or error message to appear
    time.sleep(random.uniform(5, 10))

    # Check if the URL has changed
    new_url = driver.current_url
    if new_url == initial_url:
        # URL did not change, check for error banner by text
        try:
            error_banner = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'error_banner') and contains(text(), 'Please enter your login information and complete the captcha to continue.')]"))
            )
            print("CAPTCHA required. Solving CAPTCHA...")

            # Locate the reCAPTCHA iframe and solve it
            recaptcha_solved = False
            try:
                recaptcha_iframe = driver.find_element(By.XPATH, '//iframe[@title="reCAPTCHA"]')

                # Solve the CAPTCHA using the visual method
                solver.click_recaptcha_v2(iframe=recaptcha_iframe)

                # Wait a bit to let the CAPTCHA solve
                time.sleep(random.uniform(5, 10))
                driver.switch_to.frame(recaptcha_iframe)
                # Check if the CAPTCHA checkbox is checked
                checkbox = driver.find_element(By.ID, "recaptcha-anchor")
                if "recaptcha-checkbox-checked" in checkbox.get_attribute("class"):
                    recaptcha_solved = True
                    print("CAPTCHA solved successfully.")
                else:
                    print("CAPTCHA not solved, retrying...")

            except NoSuchElementException:
                    print("Failed to locate reCAPTCHA iframe or checkbox.")
            finally:
                    driver.switch_to.default_content()  # Switch back to main content

            if recaptcha_solved:
                # Wait for any overlay to disappear
                WebDriverWait(driver, 10).until(
                    EC.invisibility_of_element_located((By.XPATH, '//div[@style="width: 100%; height: 100%; position: fixed; top: 0px; left: 0px; z-index: 2000000000; background-color: rgb(255, 255, 255); opacity: 0.05;"]'))
                )

            # Click the submit button again
            try:
                driver.find_element(By.XPATH, '//button[@type="submit"]').click()

                # After clicking the submit button again, check if the URL has changed
                WebDriverWait(driver, 20).until(
                    EC.url_changes(initial_url)
                )
                new_url = driver.current_url

            except TimeoutException:
                print("Error banner not found, but URL did not change.")
        except TimeoutException:
                print("Error banner not found, but URL did not change.")
    else:
        print("Login successful, URL has changed.")

        # Get cookies after the URL has changed
        cookies = driver.get_cookies()
        print("Logged-in cookies:", cookies)

except TimeoutException:
    print("Timeout waiting for login form fields to be visible.")
finally:
    # Close the driver after the process is complete
    driver.quit()
