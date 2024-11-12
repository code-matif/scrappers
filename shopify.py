import requests
from urllib.parse import urlparse
import json

def extract_domain_and_handle(product_url):
    parsed_url = urlparse(product_url)
    domain = f"{parsed_url.scheme}://{parsed_url.netloc}"
    handle = parsed_url.path.split('/')[-1]
    return domain, handle


def fetch_shopify_product_detail(product_url):
    try:
        domain, product_handle = extract_domain_and_handle(product_url)
        product_url = f"{domain}/products/{product_handle}.json"
        response = requests.get(product_url)

        if response.status_code == 200:
            product = response.json().get('product', {})

            title = product.get('title', '')
            price = product.get('variants', [{}])[0].get('price', '')
            description = product.get('body_html', '')
            images = [image.get('src', '') for image in product.get('images', [])]

            # Return custom data
            found_data = {
                "title": title,
                "price": price,
                "description": description,
                "images": images if images else []
            }
            return {'success': 1, 'data': found_data}
        else:
            return {'success': 0, 'message': "Product Not Found"}

    except Exception as e:
        print(f"Error occurred: {e}")
        return {'success': 0, 'message': "Error while fetching product"}
