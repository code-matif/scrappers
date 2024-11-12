import requests
from urllib.parse import urlparse
import json

# Function to extract domain and handle from the product URL
def extract_domain_and_handle(product_url):
    parsed_url = urlparse(product_url)
    domain = f"{parsed_url.scheme}://{parsed_url.netloc}"
    handle = parsed_url.path.split('/')[-1]
    return domain, handle

# Function to fetch the product details
def fetch_shopify_product_detail(product_url):
    try:
        domain, product_handle = extract_domain_and_handle(product_url)
        product_url = f"{domain}/products/{product_handle}.json"
        response = requests.get(product_url)

        if response.status_code == 200:
            product = response.json().get('product', {})
            return {'success': 1, 'data': product}
        else:
            return {'success': 0, 'message': "Product Not Found"}

    except Exception as e:
        print(f"Error occurred: {e}")
        return {'success': 0, 'message': "Error while fetching product"}