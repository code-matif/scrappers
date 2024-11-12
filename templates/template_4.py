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
        title="Benift Hook",
        description="Short title of the Benift (6-9 words, 40-45 characters)"
    )

    description: str = Field(
        ...,
        title="Benift Description",
        description="Short description of the Benift (25-27 words, 165-175 characters)"
    )


class Product(BaseModel):
    title: str = Field(
        ...,
        title="Product Title",
        description="Title of the product (8-12 words 45-55 characters)"
    )

    tagline: str = Field(
        ...,
        title="Tagline",
        description="A catchy phrase summarizing the product's category like  Minimal Interior Design : (3-5 words, 20-25 characters)"
    )

    decoration_text: Optional[str] = Field(
        ...,
        title="Decoration Text",
        description="Text for decoration purposes, like promotional slogans. (6-10 words, 35-40 characters)",
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
        min_items=1,
        title="Product Features",
        description="Up to 1 product benefits with a hook and description"
    )

    class Config:
        schema_extra = {
            "example": {
                "title": "Elegant Wooden Dining Table Set for Modern Homes",
                "tagline": "Minimal Interior Design",
                "decoration_text": "Limited Edition for This Season",
                "tags": ["furniture", "dining table", "wooden", "modern"],
                "options": [
                    {
                        "name": "Color",
                        "values": ["Natural Wood", "Dark Oak", "Walnut"]
                    },
                    {
                        "name": "Size",
                        "values": ["4-Seater", "6-Seater", "8-Seater"]
                    },
                    {
                        "name": "Material",
                        "values": ["Oak Wood", "Teak Wood", "Walnut Wood"]
                    },
                    {
                        "name": "Finish",
                        "values": ["Matte", "Glossy"]
                    }
                ],
                "variants": [
                    {
                        "title": "4-Seater Dining Table - Natural Wood, Matte Finish",
                        "option1": "Natural Wood",
                        "option2": "4-Seater",
                        "option3": "Matte",
                        "price": 399.99,
                        "sku": "DT4-NW-MAT",
                        "inventory_quantity": 25
                    },
                    {
                        "title": "6-Seater Dining Table - Dark Oak, Glossy Finish",
                        "option1": "Dark Oak",
                        "option2": "6-Seater",
                        "option3": "Glossy",
                        "price": 499.99,
                        "sku": "DT6-DO-GLS",
                        "inventory_quantity": 15
                    },
                    {
                        "title": "8-Seater Dining Table - Walnut Wood, Matte Finish",
                        "option1": "Walnut",
                        "option2": "8-Seater",
                        "option3": "Matte",
                        "price": 599.99,
                        "sku": "DT8-WW-MAT",
                        "inventory_quantity": 10
                    },
                    {
                        "title": "6-Seater Dining Table - Oak Wood, Matte Finish",
                        "option1": "Oak Wood",
                        "option2": "6-Seater",
                        "option3": "Matte",
                        "price": 459.99,
                        "sku": "DT6-OAK-MAT",
                        "inventory_quantity": 20
                    }
                ],
                "category": "Home & Furniture",
                "vendor": "Luxury Living",
                "average_rating": 4.8,
                "features": [
                    {
                        "hook": "Premium Quality Material",
                        "description": "Crafted from high-grade solid wood with a natural finish for enhanced durability and aesthetics."
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
        description="Review text from the customer (38-45 words, 210-220 characters)"
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
        "file_name": "template_4",
        "is_descriptions": False,
        "descriptions_count": 1,
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

    template_id = os.getenv("TEMPLATE_4_ID")
    cursor = db.cursor(dictionary=True)
    sql = "UPDATE product_templates SET template_schema = %s WHERE id = %s"
    cursor.execute(sql, (json.dumps(schema), template_id))
    db.commit()

    cursor.close()
    db.close()
