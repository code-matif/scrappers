from langchain_core.output_parsers import JsonOutputParser
from langchain.chains import TransformChain
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage
import base64
from langchain_core.runnables import chain
from dotenv import load_dotenv
import requests

load_dotenv()


def load_image(inputs: dict) -> dict:
    try:
        image_file = inputs["image_path"]
        response = requests.get(image_file)
        image_base64 = base64.b64encode(response.content).decode('utf-8')
        return {"image": image_base64}

    except Exception as e:
        print(f"Error fetching or encoding the image: {e}")
        return None


load_image_chain = TransformChain(
    input_variables=['image_path'],
    output_variables=["image"],
    transform=load_image
)


@chain
def image_model(inputs: dict, parser: JsonOutputParser):
    """Invoke model with image and prompt."""
    model = ChatOpenAI(temperature=0.5, model="gpt-4o", max_tokens=1024)
    msg = model.invoke(
        [
            HumanMessage(
                content=[
                    {"type": "text", "text": inputs["prompt"]},
                    {"type": "text", "text": parser.get_format_instructions()},
                    {"type": "image_url",
                     "image_url": {"url": f"data:image/jpeg;base64,{inputs['image']}"}},
                ])]
    )
    return msg.content


def get_product_reviews(image_path: str, tone: str, lang: str, existingTitle: str, description: str, ProductReview) -> dict:
    parser = JsonOutputParser(pydantic_object=ProductReview)
    """Generate product details based on inputs."""
    prompt = f"""
        Given the image of a product, provide the following information in {lang} Language:
        - Write Product Review that reflect user experiences with the product titled: {existingTitle}
        - The reviews should cover various aspects such as quality, usability, and value for money, building upon the description: {description}
        The tone of the review should be {tone.lower()}.
    """

    generate_product_chain = load_image_chain | image_model.bind(
        parser=parser) | parser
    return generate_product_chain.invoke({'image_path': image_path, 'prompt': prompt})
