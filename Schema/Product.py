from pydantic.v1 import BaseModel, Field
from typing import List, Dict, Optional


class ProductOption(BaseModel):
    """Represents an option for a product, such as size or color."""
    name: str = Field(..., title="Option Name", description="Name of the option, e.g., 'Color' or 'Size'")
    values: List[str] = Field(..., title="Option Values", description="Possible values for the option, e.g., ['Red', 'Blue']")


class ProductVariant(BaseModel):
    """Details for product variants, such as price and SKU."""
    id: int = Field(..., title="Variant ID", description="Unique identifier for the variant")
    title: str = Field(..., title="Variant Title", description="Name of the variant, e.g., 'Large - Red'")
    option1: Optional[str] = Field(None, title="Option 1", description="Value for the first option, e.g., 'Red'")
    option2: Optional[str] = Field(None, title="Option 2", description="Value for the second option, e.g., 'Large'")
    option3: Optional[str] = Field(None, title="Option 3", description="Value for the third option, if applicable")
    price: float = Field(..., title="Price", description="Price of the variant")
    sku: str = Field(..., title="SKU", description="Stock Keeping Unit for inventory tracking")
    inventory_quantity: int = Field(..., title="Inventory Quantity", description="Number of items available in stock")


class ProductFeature(BaseModel):
    """A short hook and description of the product feature."""
    hook: str = Field(..., title="Feature Hook", description="Short title of the feature")
    description: str = Field(..., title="Feature Description", description="Short description of the feature")


class Product(BaseModel):
    """Product description and details."""
    
    id: int = Field(..., title="Product ID", description="Unique identifier for the product")
    title: str = Field(..., title="Product Title", description="Title of the product")
    description: str = Field(..., title="Product Description", description="Detailed description of the product")
    why_choose_us: str = Field(..., title="Why Choose Us", description="Reasons why customers should choose this product or brand")    
    about_us: str = Field(..., title="About Us", description="Information about the company or brand")
    tags: List[str] = Field(..., title="Product Tags", description="Tags for SEO and categorization")
    options: List[ProductOption] = Field(..., min_items=4, title="Product Options", description="Options like color, size, etc.")
    variants: List[ProductVariant] = Field(..., min_items=4, title="Product Variants", description="Different available versions of the product")
    category: str = Field(..., title="Product Category", description="Category under which the product falls")
    vendor: str = Field(..., title="Vendor Name", description="Name of the product vendor or brand")
    average_rating: float = Field(..., title="Average Rating", description="Average customer rating out of 5")
    bullet_points: List[str] = Field(..., min_items=1, title="Bullet Points", description="Short bullet point descriptions of key features")
    tagline: str = Field(..., title="Tagline", description="A catchy phrase summarizing the product's appeal")
    features: List[ProductFeature] = Field(..., min_items=5, title="Product Features", description="Up to 5 product features with a hook and description")

    
    class Config:
        schema_extra = {
            "example": {
                "id": 123,
                "title": "Organic Cotton T-Shirt",
                "description": "A comfortable and eco-friendly t-shirt made from 100% organic cotton.",
                "why_choose_us": "At EcoClothing Co., we believe in providing products that align with your values and lifestyle. Our commitment to sustainability and quality sets us apart in the fashion industry. When you choose our products, you're not just getting a piece of apparel; you're supporting eco-friendly practices, ethical sourcing, and a better future for our planet. We prioritize comfort, style, and durability, ensuring every item we offer meets the highest standards. Our range of options and customer-focused approach ensures that you always find something that fits your needs. Choose us for a brand that cares about you and the environment.",
                "about_us": "EcoClothing Co. is dedicated to producing high-quality, sustainable apparel for the eco-conscious consumer. Founded on the principles of ethical sourcing and environmental responsibility, our mission is to make fashion that leaves a positive impact on the world. We carefully select our materials and processes to ensure minimal ecological footprint while delivering products that our customers love. Join us on our journey to create a more sustainable future.",                
                "tags": ["organic", "t-shirt", "cotton", "eco-friendly"],
                "options": [
                    {
                        "name": "Color",
                        "values": ["Red", "Blue", "Green", "Black", "White"]
                    },
                    {
                        "name": "Size",
                        "values": ["Small", "Medium", "Large", "XL", "XXL"]
                    }
                ],
                "variants": [
                    {
                        "id": 1,
                        "title": "Medium - Blue",
                        "option1": "Blue",
                        "option2": "Medium",
                        "price": 29.99,
                        "sku": "TSH-M-BLUE",
                        "inventory_quantity": 25,
                        "image_url": "https://example.com/images/tshirt_blue_medium.jpg"
                    },
                    {
                        "id": 2,
                        "title": "Large - Green",
                        "option1": "Green",
                        "option2": "Large",
                        "price": 31.99,
                        "sku": "TSH-L-GREEN",
                        "inventory_quantity": 10,
                        "image_url": "https://example.com/images/tshirt_green_large.jpg"
                    },
                    {
                        "id": 3,
                        "title": "Small - Red",
                        "option1": "Red",
                        "option2": "Small",
                        "price": 27.99,
                        "sku": "TSH-S-RED",
                        "inventory_quantity": 15,
                        "image_url": "https://example.com/images/tshirt_red_small.jpg"
                    },
                    {
                        "id": 4,
                        "title": "XL - Black",
                        "option1": "Black",
                        "option2": "XL",
                        "price": 34.99,
                        "sku": "TSH-XL-BLACK",
                        "inventory_quantity": 5,
                        "image_url": "https://example.com/images/tshirt_black_xl.jpg"
                    },
                    {
                        "id": 5,
                        "title": "XXL - White",
                        "option1": "White",
                        "option2": "XXL",
                        "price": 36.99,
                        "sku": "TSH-XXL-WHITE",
                        "inventory_quantity": 8,
                        "image_url": "https://example.com/images/tshirt_white_xxl.jpg"
                    }
                ],
                "category": "Apparel",
                "vendor": "EcoClothing Co.",
                "average_rating": 4.7,
                "tagline": "Perfect solution for BBQs, picnics, and DIY projects.",
                "bullet_points": [
                    "Made from 100% organic cotton",
                    "Soft and breathable material",
                    "Available in multiple colors",
                    "Eco-friendly production process",
                    "Durable and long-lasting fabric"
                ],
                "features": [
                    {
                        "hook": "Sustainable Materials",
                        "description": "Crafted from 100% organic cotton, supporting eco-friendly fashion."
                    },
                    {
                        "hook": "Comfort First",
                        "description": "Designed for maximum comfort with soft, breathable fabric."
                    },
                    {
                        "hook": "Multiple Color Options",
                        "description": "Available in a variety of colors to suit any style."
                    },
                    {
                        "hook": "Durable Design",
                        "description": "Built to last through regular wear and washing."
                    },
                    {
                        "hook": "Eco-Friendly Production",
                        "description": "Manufactured with minimal environmental impact."
                    }
                ]
            }
        }