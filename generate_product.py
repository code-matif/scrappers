from pydantic.v1 import BaseModel, Field
from typing import List, Dict, Optional
from enum import Enum
import base64
import requests
from langchain_core.output_parsers import JsonOutputParser
from langchain.chains import TransformChain
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage
from langchain_core.runnables import chain
from dotenv import load_dotenv


# Load environment variables
load_dotenv()


def load_images(image_urls: List[str]) -> List[Optional[str]]:
    """Fetch and encode images from URLs."""
    images_base64 = []
    for image_url in image_urls:
        try:
            response = requests.get(image_url)
            image_base64 = base64.b64encode(response.content).decode('utf-8')
            images_base64.append(image_base64)
        except Exception as e:
            print(
                f"Error fetching or encoding the image from {image_url}: {e}")
            images_base64.append(None)  # Append None for failed fetch
    return images_base64


load_image_chain = TransformChain(
    input_variables=['image_urls'],
    output_variables=["images"],
    transform=lambda inputs: {"images": load_images(inputs['image_urls'])}
)


@chain
def image_model(inputs: dict, parser: JsonOutputParser):
    """Invoke model with images and prompt."""
    model = ChatOpenAI(temperature=0.5, model="gpt-4o", max_tokens=1024)
    image_urls = inputs.get("images", [])

    msg = model.invoke(
        [
            HumanMessage(
                content=[
                    {"type": "text", "text": inputs["prompt"]},
                    {"type": "text", "text": parser.get_format_instructions()},
                    *[
                        {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{img}"}} for img in image_urls if img
                    ],
                ]
            )
        ]
    )
    return msg.content


def get_product(
    image_urls: Optional[List[str]],
    tone: str,
    lang: str,
    existingTitle: str,
    description: str,
    Product
) -> dict:
    parser = JsonOutputParser(pydantic_object=Product)
    """Generate product details based on inputs."""

    prompt = f"""
        Given the images of a product, rewrite the product details in {lang} Language:
        Existing Title: {existingTitle}
        Existing Description: {description}
        
        Make it more appealing to eco-conscious consumers.
        The tone of the description should be {tone.lower()}.
    """

    # generate_product_chain = load_image_chain | image_model | parser
    generate_product_chain = (
        load_image_chain
        | image_model.bind(parser=parser)  # Pass the parser correctly
        | parser
    )
    return generate_product_chain.invoke({
        'image_urls': image_urls if image_urls else [],
        'prompt': prompt
    })
