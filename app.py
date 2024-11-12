# app.py
from typing import Any, Dict, Type, List, Optional
from pydantic.v1 import BaseModel, create_model, Field

from generate_product import get_product
from generate_product_description import get_product_description
from generate_product_reviews import get_product_reviews

from amazon import fetch_amazon_product_detail
from aliexpress import fetch_aliexpress_product_detail
from alibaba import fetch_alibaba_product_detail
from shopify import fetch_shopify_product_detail
from flask import Flask, request, jsonify

import time
import os
import re
import requests
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
import mysql.connector
from dotenv import load_dotenv
from langchain_core.output_parsers import JsonOutputParser
import importlib
from datetime import datetime

from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage

from Schema.BlogPost import BlogPost


# Load environment variables
load_dotenv()

# A list of different User-Agent strings to rotate between
user_agents = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/11.1 Safari/605.1.15',
    'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0'
]


app = Flask(__name__)

IMAGE_DIR = '/var/www/html/automated-stores/x-builder-core/img/product-images'

# Create the directory if it doesn't exist
os.makedirs(IMAGE_DIR, exist_ok=True)

def slugify(string):
    string = string.lower()
    string = re.sub(r'[^a-z0-9\s-]', '', string)
    string = re.sub(r'[\s]+', '-', string).strip('-')
    return string

def get_timestamp():
    return datetime.now().strftime('%Y%m%d_%H%M%S_%f')

def save_image(image_url, filename):
    response = requests.get(image_url)
    if response.status_code == 200:
        with open(os.path.join(IMAGE_DIR, filename), 'wb') as f:
            f.write(response.content)
        return filename
    else:
        print("Error downloading image:", response.content)
        return None

def generate_images(prompt, num_images=4):
    dalle_url = 'https://api.openai.com/v1/images/generations'
    headers = {
        'Authorization': f"Bearer {os.getenv('OPENAI_API_KEY')}",
        'Content-Type': 'application/json'
    }
    images = []
    data = {
        'prompt': prompt,
        'n': num_images,
        'size': '1024x1024'
    }
    response = requests.post(dalle_url, headers=headers, json=data)
    if response.status_code == 200:
        images = [img['url'] for img in response.json().get('data', [])]
    else:
        print("Error generating image:", response.content)
    return images


def generate_banner_image(prompt, title):
    dalle_url = 'https://api.openai.com/v1/images/generations'
    headers = {
        'Authorization': f"Bearer {os.getenv('OPENAI_API_KEY')}",
        'Content-Type': 'application/json'
    }
    data = {
        'prompt': prompt,
        'n': 1,
        'size': '1024x1024'
    }
    
    response = requests.post(dalle_url, headers=headers, json=data)
    
    if response.status_code == 200:
        image_info = response.json().get('data', [])[0]
        image_url = image_info.get('url')
        
        if image_url:
            img_data = requests.get(image_url).content
            file_name = f"{slugify(title)}.png"
            file_path = f"/var/www/html/automated-stores/x-builder-core/img/blogs/{file_name}"
            relative_path = f"img/blogs/{file_name}"
            
            # Ensure the directory exists
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            
            # Save the image
            with open(file_path, 'wb') as img_file:
                img_file.write(img_data)
            
            return relative_path
    else:
        print("Error generating image:", response.content)
        return None

def save_blog_banner(image_url, title):
    img_data = requests.get(image_url).content
    file_name = f"{slugify(title)}.png"
    file_path = f"/var/www/html/automated-stores/x-builder-core/img/blogs/{file_name}"
    relative_path = f"img/blogs/{file_name}"
    
    # Ensure the directory exists
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    
    # Save the image
    with open(file_path, 'wb') as img_file:
        img_file.write(img_data)
    
    return relative_path

def generate_variations(image_urls):
    dalle_variation_url = 'https://api.openai.com/v1/images/variations'
    headers = {
        'Authorization': f"Bearer {os.getenv('OPENAI_API_KEY')}"
    }
    
    variations = []
    for image_url in image_urls:

        image_name = image_url.split('/')[-1]

        files = {
            "image": (f"{image_name}", open(f"{os.path.join(IMAGE_DIR, image_name)}", "rb")),
        }

        data = {
            "model": "dall-e-2",
            "n": 1,
            "size": "1024x1024"
        }

        response = requests.post(dalle_variation_url, headers=headers, files=files, data=data)

        if response.status_code == 200:
            variations += [img['url'] for img in response.json().get('data', [])]


    return variations


def save_and_append_image(img_url, filename_prefix, image_list):
    """Helper function to save an image and append its URL to the image list."""
    filename = f"{filename_prefix}-{len(image_list) + 1}-{get_timestamp()}.png"
    saved_filename = save_image(img_url, filename)
    if saved_filename:
        image_list.append(f"https://dev.xbuilder.ai/x-builder-core/img/product-images/{saved_filename}")

def generate_required_images(product_title, num_images_needed, local_images):
    """Generate and save images until the required count is met."""
    prompt = f"Create a variation of {product_title}."
    new_images = generate_images(prompt, num_images_needed)
    for new_img_url in new_images:
        save_and_append_image(new_img_url, f"generated-{product_title}-image", local_images)
        if len(local_images) >= 4:
            break


def get_db():
    try:
        db_connection = mysql.connector.connect(
            host=os.getenv('DB_HOST'),
            database=os.getenv('DB_DATABASE'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD')
        )
        # cursor = db_connection.cursor(dictionary=True)
        return db_connection
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None, None


@app.route('/test-db', methods=['GET'])
def test_db():
    # from templates.template_1 import save_schema
    # save_schema(get_db())
    # from templates.template_2 import save_schema
    # save_schema(get_db())
    # from templates.template_3 import save_schema
    # save_schema(get_db())
    # from templates.template_4 import save_schema
    # save_schema(get_db())
    # from templates.template_5 import save_schema
    # save_schema(get_db())
    # from templates.template_6 import save_schema
    # save_schema(get_db())
    # from templates.template_7 import save_schema
    # save_schema(get_db())
    

    return jsonify({"success": True})


@app.route('/product-details', methods=['POST'])
def product_details():
    data = request.json
    product_url = data.get('product_url')
    language = data.get('language', 'English')
    store_name = data.get('store_name')
    is_generate = data.get('is_generate', False)
    template_id = None

    if is_generate:
        template_id = data.get('template_id')
        if not template_id or template_id == "":
            return jsonify({"success": False, "message": "Template Id is required"})

    if not store_name or store_name == "":
        return jsonify({"success": False, "message": "Store Name is required"})

    if not product_url or product_url == "":
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

    # Main code starts here
    local_images = []
    product_title_slug = slugify(response['data'].get('title', 'product'))
    existing_images = response['data'].get("images", [])[:5] if isinstance(response['data'].get("images"), list) else []

    # Save existing images locally
    for i, img_url in enumerate(existing_images):
        save_and_append_image(img_url, f"{product_title_slug}-image", local_images)

    # If no images exist, generate the first one
    if not local_images:
        prompt = f"Create an image of {response['data'].get('title', 'product')}, which is {response['data'].get('description', '')}."
        first_image = generate_images(prompt, 1)
        if first_image:
            save_and_append_image(first_image[0], f"created-{product_title_slug}-image", local_images)

    # Generate additional images or variations if less than 4 exist
    if len(local_images) < 4:
        num_images_needed = 4 - len(local_images)
        if local_images:
            variations = generate_variations(local_images)
            for variation_url in variations:
                save_and_append_image(variation_url, f"generated-{product_title_slug}-variation", local_images)
                if len(local_images) >= 4:
                    break

        # If still not enough images, generate new ones
        if len(local_images) < 4:
            generate_required_images(product_title_slug, num_images_needed, local_images)

    # Update response with local image URLs
    response['data']["images"] = local_images

    # Generate product using OpenAI
    if response.get('success', False) and is_generate:
        product = generate_product_details(response['data'], template_id, language)
        response['data'] = product
        
    print(jsonify(response))
    # time.sleep(2)
    return jsonify(response)
@app.route('/generate-blog', methods=['POST'])
def generate_blog():
    data = request.json
    prompt = data.get('prompt')
    banner = data.get('banner', None)
    
    if not prompt or prompt == "":
        return jsonify({"success": False, "message": "prompt is required"})

    # Enhanced writing instructions
    writing_instructions = (
        "You are a professional blog writer. Your task is to create a detailed, engaging, and SEO-optimized blog post. "
        "Your writing should include:\n"
        "- A catchy title that attracts readers\n"
        "- Clear and informative sections with appropriate HTML headings (e.g., <h2>, <h3>)\n"
        "- Bullet points for lists using <ul> and <li> tags to enhance readability\n"
        "- A strong introduction in a <p> tag that hooks the reader and a compelling conclusion with a call to action\n"
        "- Effective use of keywords for SEO\n"
        "- A brief excerpt summarizing the content in a <p> tag\n"
        "- Relevant tags for categorization\n"
        "- Random Effectiveness Score Between 70 and 93 Based On Generated Content \n"
        "Please follow these formatting guidelines for the output, and ensure all content is properly formatted in HTML."
    )

    parser = JsonOutputParser(pydantic_object=BlogPost)

    prompt = (
        f"{writing_instructions}\n\n"
        f"{prompt}\n\n"
    )
    model = ChatOpenAI(temperature=0.6, model="gpt-4o", max_tokens=1024)
    msg = model.invoke(
        [
            HumanMessage(
                content=[
                    {"type": "text", "text": prompt},
                    {"type": "text", "text": parser.get_format_instructions()}
                ]
            )
        ]
    )

    try:
        # Clean up the msg.content to extract valid JSON
        json_content = msg.content.strip().split('\n', 1)[1]  # Get the part after the first line
        json_content = json_content.strip('```json\n')  # Remove the initial ```json\n
        json_content = json_content.strip('```')  # Remove the trailing ```

        output_data = json.loads(json_content)  # Parse the cleaned JSON string

        if banner:
            output_data['banner'] = save_blog_banner(banner, output_data['name'])
        else:
            output_data['banner'] = generate_banner_image(output_data['banner_prompt'], output_data['name'])
        
    except (json.JSONDecodeError, IndexError) as e:
        return jsonify({"success": False, "message": "Failed to parse JSON.", "error": str(e), "raw_output": msg.content})

    return jsonify({"success": True, "data": output_data})


def get_schema(template_id):
    db = get_db()
    cursor = db.cursor(dictionary=True)

    sql = "SELECT template_schema FROM product_templates WHERE id = %s"
    cursor.execute(sql, (template_id,))
    result = cursor.fetchone()
    cursor.close()
    db.close()
    if result:
        return json.loads(result['template_schema'])
    else:
        return None


def generate_product_details(data, template_id, language="English"):

    des = data.get('description', 'Not Available')
    title = data.get('title', 'Not Available')
    images = data.get('images', [])
    tone = "playful"
    schema_data = get_schema(template_id)

    if not schema_data or schema_data is None:
        return {}

    file_name = schema_data.get("file_name")
    descriptions_count = schema_data.get("descriptions_count",4)
    is_descriptions = schema_data.get("is_descriptions")
    is_reviews = schema_data.get("is_reviews")
    is_2nd_step = is_descriptions or is_reviews

    schemas = schema_data.get("schema", [])

    product_schema = schemas[0]

    Product = product_schema.get("schema")

    module = importlib.import_module(f"templates.{file_name}")
    schema_class = getattr(module, Product)

    product = get_product(images, tone, language, title, des, schema_class)

    product["images"] = images
    if is_2nd_step:
        description = product.get('description', 'Not Available')
        product_title = product.get('title', 'Not Available')

        descriptions = []
        reviews = []
        i = 0

        for img in images:
            i = i + 1

            if is_descriptions and i <= descriptions_count:

                # dynamic import
                description_schema = schemas[1]
                Description = description_schema.get("schema")
                Description = getattr(module, Description)

                prompt = f"Generate a playful description of this product."
                result = get_product_description(
                    img, prompt, tone, language, Description)
                result["image"] = img
                descriptions.append(result)

            if is_reviews:
                # dynamic import
                reviews_schema = schemas[2]
                ProductReview = reviews_schema.get("schema")
                ProductReview = getattr(module, ProductReview)

                # generating reviews
                review = get_product_reviews(
                    img, tone, language, product_title, description, ProductReview)
                review["image"] = img
                reviews.append(review)

        if is_reviews:
            product["reviews"] = reviews

        if is_descriptions:
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
