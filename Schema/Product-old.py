from pydantic.v1 import BaseModel, Field
from typing import List, Dict
from enum import Enum


class ProductVariant(BaseModel):
    """Details for product variants, such as size, color, price, and other customizable options."""
    title: str = Field(..., title="Variant Title", description="Name of the variant, e.g., 'Large - Red'")
    inventory_quantity: int = Field(..., title="Inventory Quantity", description="Number of items available in stock")
    attributes: Dict[str, str] = Field(..., title="Attributes", description="Additional variant attributes like color, weight, etc.")
    price: float = Field(..., title="Price", description="Price of the variant")


class ProductFeature(BaseModel):
    """A short hook and description of the product feature."""
    hook: str = Field(..., title="Feature Hook", description="Short title of the feature")
    description: str = Field(..., title="Feature Description", description="Short description of the feature")

class Product(BaseModel):
    """Product description and details."""
    
    title: str = Field(..., title="Product Title", description="Title of the product")
    description: str = Field(..., title="Product Description", description="Detailed description of the product")
    tags: List[str] = Field(..., title="Product Tags", description="Tags for SEO and categorization")
    variants: List[ProductVariant] = Field(..., min_items=5, title="Product Variants", description="Different available versions of the product")
    category: str = Field(..., title="Product Category", description="Category under which the product falls")
    vendor: str = Field(..., title="Vendor Name", description="Name of the product vendor or brand")
    average_rating: float = Field(..., title="Average Rating", description="Average customer rating out of 5 minimum 4.5")
    bullet_points: List[str] = Field(..., min_items=5, title="Bullet Points", description="Short bullet point descriptions of key features")
    tagline: str = Field(..., title="Tagline", description="A catchy phrase summarizing the product's appeal")
    features: List[ProductFeature] = Field(..., min_items=5, title="Product Features", description="Up to 5 product features with a hook and description")
    
    class Config:
        schema_extra = {
            "example": {
                "title": "Organic Cotton T-Shirt",
                "description": "A comfortable and eco-friendly t-shirt made from 100% organic cotton.",
                "tags": ["organic", "t-shirt", "cotton", "eco-friendly"],
                "variants": [
                    {
                        "title": "Medium - Blue",
                        "inventory_quantity": 25,
                        "attributes": {
                            "color": "Blue",
                            "size": "Medium",
                            "weight": "200g"
                        },
                        "price": 29.99
                    },
                    {
                        "title": "Large - Green",
                        "inventory_quantity": 10,
                        "attributes": {
                            "color": "Green",
                            "size": "Large",
                            "weight": "210g"
                        },
                        "price": 31.99
                    },
                    {
                        "title": "Small - Red",
                        "inventory_quantity": 15,
                        "attributes": {
                            "color": "Red",
                            "size": "Small",
                            "weight": "190g"
                        },
                        "price": 27.99
                    },
                    {
                        "title": "XL - Black",
                        "inventory_quantity": 5,
                        "attributes": {
                            "color": "Black",
                            "size": "XL",
                            "weight": "220g"
                        },
                        "price": 34.99
                    },
                    {
                        "title": "XXL - White",
                        "inventory_quantity": 8,
                        "attributes": {
                            "color": "White",
                            "size": "XXL",
                            "weight": "230g"
                        },
                        "price": 36.99
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