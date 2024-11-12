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
        description="Engaging hook for the product (3-5 words, 25-30 characters)"
    )

    description: str = Field(
        ...,
        title="Product Description",
        description="Description of the product (40-45 words, 255-260 characters)"
    )


class ProductFeature(BaseModel):
    hook: str = Field(
        ...,
        title="Feature Hook",
        description="Short title of the feature (3-4 words, 15-20 characters)"
    )

    description: str = Field(
        ...,
        title="Feature Description",
        description="Short description of the feature (8-12 words, 90-95 characters)"
    )


class Product(BaseModel):
    title: str = Field(
        ...,
        title="Product Title",
        description="Title of the product (3-5 words, 25-32 characters)"
    )

    description: str = Field(
        ...,
        title="Product Description",
        description="description of the product (18-22 words, 155-160 characters)"
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
        min_items=3,
        title="Product Features",
        description="Up to 3 product features with a hook and description"
    )

    schema_extra = {
        "example": {
            "title": "Ultra Slim Laptop",
            "description": "An ultra-slim laptop with powerful performance and long battery life, perfect for professionals and students.",
            "tags": ["laptop", "technology", "electronics", "portable"],
            "options": [
                {
                    "name": "Color",
                    "values": ["Silver", "Black", "Rose Gold"]
                },
                {
                    "name": "Storage",
                    "values": ["256GB SSD", "512GB SSD", "1TB SSD"]
                },
                {
                    "name": "RAM",
                    "values": ["8GB", "16GB"]
                },
                {
                    "name": "Screen Size",
                    "values": ["13 inches", "15 inches"]
                }
            ],
            "variants": [
                {
                    "title": "Ultra Slim Laptop - Silver, 256GB SSD, 8GB RAM",
                    "option1": "Silver",
                    "option2": "256GB SSD",
                    "option3": "8GB",
                    "price": 999.99,
                    "sku": "ULS-001-SL-256-8",
                    "inventory_quantity": 25
                },
                {
                    "title": "Ultra Slim Laptop - Silver, 512GB SSD, 16GB RAM",
                    "option1": "Silver",
                    "option2": "512GB SSD",
                    "option3": "16GB",
                    "price": 1199.99,
                    "sku": "ULS-001-SL-512-16",
                    "inventory_quantity": 15
                },
                {
                    "title": "Ultra Slim Laptop - Black, 1TB SSD, 16GB RAM",
                    "option1": "Black",
                    "option2": "1TB SSD",
                    "option3": "16GB",
                    "price": 1399.99,
                    "sku": "ULS-001-BK-1TB-16",
                    "inventory_quantity": 10
                },
                {
                    "title": "Ultra Slim Laptop - Rose Gold, 512GB SSD, 8GB RAM",
                    "option1": "Rose Gold",
                    "option2": "512GB SSD",
                    "option3": "8GB",
                    "price": 1099.99,
                    "sku": "ULS-001-RG-512-8",
                    "inventory_quantity": 20
                }
            ],
            "category": "Computers",
            "vendor": "TechSavvy",
            "average_rating": 4.8,
            "features": [
                {
                        "hook": "Powerful Performance",
                        "description": "Equipped with the latest Intel processors for seamless multitasking."
                },
                {
                    "hook": "Long Battery Life",
                    "description": "Lasts up to 12 hours on a single charge, perfect for all-day use."
                },
                {
                    "hook": "Lightweight Design",
                    "description": "Weighs just 2.5 pounds, making it easy to carry anywhere."
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
        description="Review text from the customer (50-52 words, 285-292 characters)"
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
        "file_name": "template_5",
        "is_descriptions": True,
        "descriptions_count": 2,
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

    template_id = os.getenv("TEMPLATE_5_ID")
    cursor = db.cursor(dictionary=True)
    sql = "UPDATE product_templates SET template_schema = %s WHERE id = %s"
    cursor.execute(sql, (json.dumps(schema), template_id))
    db.commit()

    cursor.close()
    db.close()
