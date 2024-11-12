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
        description="Engaging hook for the product (2-5 words, 35-40 characters)"
    )

    description: str = Field(
        ...,
        title="Product Description",
        description="Description of the product (60-70 words, 370-380 characters)"
    )


class ProductFeature(BaseModel):
    hook: str = Field(
        ...,
        title="Feature Hook",
        description="Short title of the feature (2-3 words, 18-20 characters)"
    )

    description: str = Field(
        ...,
        title="Feature Description",
        description="Short description of the feature (9-12 words, 55-60 characters)"
    )


class Product(BaseModel):
    title: str = Field(
        ...,
        title="Product Title",
        description="Title of the product (3-5 words, 30-35 characters)"
    )

    bullet_points: List[str] = Field(
        ...,
        min_items=5,
        title="Bullet Points",
        description="Short bullet point descriptions of key features (4-5 words, 25-30 characters)"
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
                "title": "Deluxe Coffee Maker",
                "bullet_points": [
                    "Brew coffee in minutes",
                    "Customizable strength",
                    "Built-in grinder",
                    "Easy-to-use interface",
                    "Energy-saving mode"
                ],
                "tags": ["coffee", "kitchen", "appliance", "home"],
                "options": [
                    {
                        "name": "Color",
                        "values": ["Black", "Silver", "Red"]
                    },
                    {
                        "name": "Size",
                        "values": ["Small", "Medium", "Large"]
                    },
                    {
                        "name": "Type",
                        "values": ["Drip", "Single Serve", "Espresso"]
                    },
                    {
                        "name": "Material",
                        "values": ["Plastic", "Stainless Steel", "Glass"]
                    }
                ],
                "variants": [
                    {
                        "title": "Deluxe Coffee Maker - Black",
                        "option1": "Black",
                        "option2": "Medium",
                        "option3": None,
                        "price": 99.99,
                        "sku": "CM-001-BK",
                        "inventory_quantity": 50
                    },
                    {
                        "title": "Deluxe Coffee Maker - Silver",
                        "option1": "Silver",
                        "option2": "Medium",
                        "option3": None,
                        "price": 109.99,
                        "sku": "CM-001-SL",
                        "inventory_quantity": 30
                    },
                    {
                        "title": "Deluxe Coffee Maker - Red",
                        "option1": "Red",
                        "option2": "Medium",
                        "option3": None,
                        "price": 109.99,
                        "sku": "CM-001-RD",
                        "inventory_quantity": 20
                    },
                    {
                        "title": "Deluxe Coffee Maker - Black - Large",
                        "option1": "Black",
                        "option2": "Large",
                        "option3": None,
                        "price": 119.99,
                        "sku": "CM-001-BK-LG",
                        "inventory_quantity": 25
                    }
                ],
                "category": "Kitchen Appliances",
                "vendor": "CoffeeCo",
                "average_rating": 4.7,
                "features": [
                    {
                        "hook": "Fast Brewing",
                        "description": "Brews a full pot in under 10 minutes"
                    },
                    {
                        "hook": "Custom Strength",
                        "description": "Adjust brew strength for a perfect cup"
                    },
                    {
                        "hook": "Built-in Grinder",
                        "description": "Freshly ground coffee with every brew"
                    },
                    {
                        "hook": "Easy Cleanup",
                        "description": "Dishwasher safe components"
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
        description="Review text from the customer (25-30 words, 120-125 characters)"
    )
    date: str = Field(
        ...,
        title="Review Date",
        description="Date of the review in dd-mm-yyyy format less then today, greater then from past 6 months"
    )


# print()

def save_schema(db):
    product_schema = "Product"
    product_descriptions_schema = "Description"
    product_review_schema = "ProductReview"

    schema = {
        "file_name": "template_3",
        "descriptions_count": 2,
        "is_descriptions": True,
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

    template_id = os.getenv("TEMPLATE_3_ID")
    cursor = db.cursor(dictionary=True)
    sql = "UPDATE product_templates SET template_schema = %s WHERE id = %s"
    cursor.execute(sql, (json.dumps(schema), template_id))
    db.commit()

    cursor.close()
    db.close()
