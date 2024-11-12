from pydantic.v1 import BaseModel, Field
from typing import List, Dict, Optional
import json
from pydantic import ValidationError
import os
from enum import Enum
from dotenv import load_dotenv
from pydantic.v1 import schema_json_of
load_dotenv()


class ProductOption(BaseModel):
    """Represents an option for a product, such as size or color."""
    name: str = Field(
        ...,
        title="Option Name",
        description="Name of the option, e.g., 'Color' or 'Size'"
    )

    values: List[str] = Field(
        ...,
        title="Option Values",
        description="Possible values for the option, e.g., ['Red', 'Blue']"
    )


class ProductVariant(BaseModel):
    """Details for product variants, such as price and SKU."""
    title: str = Field(
        ...,
        title="Variant Title",
        description="Name of the variant, e.g., 'Large - Red'"
    )

    option1: str = Field(
        ...,
        title="Option 1",
        description="Value for the first option, e.g., 'Red'"
    )
    option2: Optional[str] = Field(
        None,
        title="Option 2",
        description="Value for the second option, e.g., 'Large'"
    )
    option3: Optional[str] = Field(
        None,
        title="Option 3",
        description="Value for the third option, if applicable"
    )
    price: float = Field(
        ...,
        title="Price",
        description="Price of the variant"
    )
    sku: str = Field(
        ...,
        title="SKU",
        description="Stock Keeping Unit for inventory tracking"
    )

    inventory_quantity: int = Field(
        ...,
        title="Inventory Quantity",
        description="Number of items available in stock"
    )


class Description(BaseModel):
    """Product description."""
    hook: str = Field(
        ...,
        title="Product Hook",
        description="Engaging hook for the product (3-5 words, 24-30 characters)"
    )

    description: str = Field(
        ...,
        title="Product Description",
        description="Description of the product (55-60 words, 365-370 characters)"
    )


class ProductFeature(BaseModel):
    hook: str = Field(
        ...,
        title="Feature Hook",
        description="Short title of the feature (3-5 words, 38-42 characters)"
    )

    description: str = Field(
        ...,
        title="Feature Description",
        description="Short description of the feature (15-20 words, 93-98 characters)"
    )


class Product(BaseModel):
    title: str = Field(
        ...,
        title="Product Title",
        description="Title of the product (3-5 words, 20-25 characters)"
    )

    tagline: str = Field(
        ...,
        title="Tagline",
        description="A catchy phrase summarizing the product's appeal (5-8 words, 30-35 characters)"
    )

    p_features: List[ProductFeature] = Field(
        ...,
        min_items=3,
        title="Product Features",
        description="Up to 3 product features with a hook and description"
    )

    why_choose_us: str = Field(
        ...,
        title="Why Choose Us",
        description="Reasons why customers should choose this product or brand (30-35 words, 207-215 characters)"
    )

    description: str = Field(
        ...,
        title="Product Description",
        description="Detailed description of the product (30-35 words 208-216 characters)"
    )

    tags: List[str] = Field(
        ...,
        title="Product Tags",
        description="Tags for SEO and categorization"
    )

    options: List[ProductOption] = Field(
        ...,
        min_items=4,
        title="Product Options",
        description="Options like color, size, etc."
    )

    variants: List[ProductVariant] = Field(
        ...,
        min_items=4,
        title="Product Variants",
        description="Different available versions of the product"
    )

    category: str = Field(
        ...,
        title="Product Category",
        description="Category under which the product falls"
    )

    vendor: str = Field(
        ...,
        title="Vendor Name",
        description="Name of the product vendor or brand"
    )

    average_rating: float = Field(
        ...,
        title="Average Rating",
        description="Average customer rating out of 5 min 4.5"
    )

    features: List[ProductFeature] = Field(
        ...,
        min_items=4,
        title="Product Features",
        description="Up to 4 product features with a hook and description"
    )

    class Config:
        schema_extra = {
            "example": {
                "title": "Ultimate Hiking Backpack",
                "tagline": "Adventure Awaits You",
                "p_features": [
                    {
                        "hook": "Comfortable Fit",
                        "description": "Padded shoulder straps distribute weight evenly."
                    },
                    {
                        "hook": "Weather Resistant",
                        "description": "Durable material keeps gear dry in rain."
                    },
                    {
                        "hook": "Ample Storage",
                        "description": "Multiple compartments for organized packing."
                    }
                ],
                "why_choose_us": "Designed by hikers for hikers, ensuring durability and comfort on all your outdoor adventures.",
                "description": "A high-quality hiking backpack with superior support, designed for long trips and rough terrain.",
                "tags": ["hiking", "outdoors", "backpack", "travel"],
                "options": [
                    {
                        "name": "Color",
                        "values": ["Black", "Green", "Blue", "Red"]
                    },
                    {
                        "name": "Size",
                        "values": ["Small", "Medium", "Large", "X-Large"]
                    },
                    {
                        "name": "Material",
                        "values": ["Nylon", "Canvas", "Polyester"]
                    },
                    {
                        "name": "Frame Type",
                        "values": ["Internal", "External"]
                    }
                ],
                "variants": [
                    {
                        "title": "Ultimate Hiking Backpack - Black, Medium, Nylon",
                        "option1": "Black",
                        "option2": "Medium",
                        "option3": "Nylon",
                        "price": 129.99,
                        "sku": "UHB-M-BL-NY",
                        "inventory_quantity": 50
                    },
                    {
                        "title": "Ultimate Hiking Backpack - Green, Large, Canvas",
                        "option1": "Green",
                        "option2": "Large",
                        "option3": "Canvas",
                        "price": 149.99,
                        "sku": "UHB-L-GR-CA",
                        "inventory_quantity": 30
                    },
                    {
                        "title": "Ultimate Hiking Backpack - Blue, Small, Polyester",
                        "option1": "Blue",
                        "option2": "Small",
                        "option3": "Polyester",
                        "price": 109.99,
                        "sku": "UHB-S-BL-PO",
                        "inventory_quantity": 60
                    },
                    {
                        "title": "Ultimate Hiking Backpack - Red, X-Large, Nylon",
                        "option1": "Red",
                        "option2": "X-Large",
                        "option3": "Nylon",
                        "price": 169.99,
                        "sku": "UHB-XL-RD-NY",
                        "inventory_quantity": 20
                    }
                ],
                "category": "Outdoor Gear",
                "vendor": "TrailBlazer Co.",
                "average_rating": 4.8,
                "features": [
                    {
                        "hook": "Ergonomic Design",
                        "description": "Supports back for extended comfort on trails."
                    },
                    {
                        "hook": "Lightweight Build",
                        "description": "Won't weigh you down during hikes."
                    },
                    {
                        "hook": "Water Bottle Pocket",
                        "description": "Easily accessible storage for hydration."
                    },
                    {
                        "hook": "Expandable Compartments",
                        "description": "Provides extra space when needed."
                    }
                ]
            }
        }


class ProductReview(BaseModel):
    """Product description."""
    rating: float = Field(
        ...,
        title="Rating",
        description="Rating out of 5 minimum 4.5"
    )
    comment: str = Field(
        ...,
        title="Review Comment",
        description="Review text from the customer (20-25 words, 125-130 characters)"
    )

    date: str = Field(
        ...,
        title="Review Date",
        description="Date of the review in dd-mm-yyyy format less then today, greater then from past 6 months"
    )


def save_schema(db):
    product_schema = "Product"
    product_descriptions_schema = "Description"
    product_review_schema = "ProductReview"

    schema = {
        "file_name": "template_7",
        "is_descriptions": True,
        "descriptions_count": 3,
        "is_reviews": True,
        "schema": [
            {
                "name": "product",
                "schema": product_schema
            },
            {
                "name": "descriptions",
                "schema": product_descriptions_schema
            },
            {
                "name": "reviews",
                "schema": product_review_schema
            }
        ]
    }

    template_id = os.getenv("TEMPLATE_7_ID")
    cursor = db.cursor(dictionary=True)
    sql = "UPDATE product_templates SET template_schema = %s WHERE id = %s"
    cursor.execute(sql, (json.dumps(schema), template_id))
    db.commit()

    cursor.close()
    db.close()
