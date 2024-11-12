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


class ProductFeature(BaseModel):
    hook: str = Field(
        ...,
        title="Feature Hook",
        description="Short title of the feature (2-3 words, 20-22 characters)"
    )

    description: str = Field(
        ...,
        title="Feature Description",
        description="Short description of the feature (10-12 words, 50-52 characters)"
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
        description="A catchy phrase summarizing the product's appeal (8-10 words, 60-65 characters)"
    )

    description: str = Field(
        ...,
        title="Product Description",
        description="description of the product (45-50 words, 310-320 characters)"
    )

    why_choose_us: str = Field(..., title="Why Choose Us",
                               description="Reasons why customers should choose this product or brand (35-40 words, 265-275 characters)")
    about_us: str = Field(..., title="About Us",
                          description="Information about the company or brand (70-75 words, 495-500 characters)")

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
        min_items=3,
        title="Product Features",
        description="Up to 3 product features with a hook and description"
    )

    class Config:
        schema_extra = {
            "example": {
                "title": "Comfortable Cotton T-Shirt",
                "tagline": "Soft, breathable, and stylish",
                "description": "Our Comfortable Cotton T-Shirt is made from 100% premium cotton, offering unmatched softness and breathability. Perfect for casual outings or lounging at home, it’s a must-have for any wardrobe.",
                "why_choose_us": "Choose our t-shirts for their quality, style, and comfort. We prioritize sustainable sourcing and ethical manufacturing.",
                "about_us": "We are a passionate team committed to delivering high-quality clothing that combines comfort and style. Our mission is to create fashion that feels as good as it looks.",
                "tags": ["tshirt", "cotton", "comfortable", "casual"],
                "options": [
                    {
                        "name": "Color",
                        "values": ["Red", "Blue", "Green", "Black"]
                    },
                    {
                        "name": "Size",
                        "values": ["Small", "Medium", "Large", "X-Large"]
                    },
                    {
                        "name": "Style",
                        "values": ["Crew Neck", "V-Neck"]
                    },
                    {
                        "name": "Fit",
                        "values": ["Regular", "Slim"]
                    }
                ],
                "variants": [
                    {
                        "title": "Small - Red",
                        "option1": "Red",
                        "option2": "Small",
                        "option3": None,
                        "price": 19.99,
                        "sku": "TSHIRT-RD-S",
                        "inventory_quantity": 50
                    },
                    {
                        "title": "Medium - Blue",
                        "option1": "Blue",
                        "option2": "Medium",
                        "option3": None,
                        "price": 19.99,
                        "sku": "TSHIRT-BL-M",
                        "inventory_quantity": 30
                    },
                    {
                        "title": "Large - Green",
                        "option1": "Green",
                        "option2": "Large",
                        "option3": None,
                        "price": 19.99,
                        "sku": "TSHIRT-GN-L",
                        "inventory_quantity": 20
                    },
                    {
                        "title": "X-Large - Black",
                        "option1": "Black",
                        "option2": "X-Large",
                        "option3": None,
                        "price": 19.99,
                        "sku": "TSHIRT-BK-XL",
                        "inventory_quantity": 15
                    }
                ],
                "category": "Apparel",
                "vendor": "Fashion Co.",
                "average_rating": 4.8,
                "features": [
                    {
                        "hook": "Eco-Friendly Material",
                        "description": "Made from sustainable, organic cotton."
                    },
                    {
                        "hook": "Comfort Fit",
                        "description": "Designed for all-day comfort without compromising style."
                    },
                    {
                        "hook": "Durable Stitching",
                        "description": "High-quality stitching for long-lasting wear."
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
        description="Review text from the customer (30-32 words, 165-175 characters)"
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
        "file_name": "template_2",
        "is_descriptions": False,
        "descriptions_count": 0,
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

    template_id = os.getenv("TEMPLATE_2_ID")
    cursor = db.cursor(dictionary=True)
    sql = "UPDATE product_templates SET template_schema = %s WHERE id = %s"
    cursor.execute(sql, (json.dumps(schema), template_id))
    db.commit()

    cursor.close()
    db.close()
