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
        description="Engaging hook for the product (5-8 words, 40-46 characters)"
    )

    description: str = Field(
        ...,
        title="Product Description",
        description="Description of the product (12-15 words, 125-130 characters)"
    )


class ProductFeature(BaseModel):
    hook: str = Field(
        ...,
        title="Feature Hook",
        description="Short title of the feature"
    )

    description: str = Field(
        ...,
        title="Feature Description",
        description="Short description of the feature (25-27 words, 165-175 characters)"
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

    bullet_points: List[str] = Field(
        ...,
        min_items=5,
        title="Bullet Points",
        description="Short bullet point descriptions of key features (4-5 words, 25-35 characters in a point)"
    )

    description: str = Field(
        ...,
        title="Product Description",
        description="Detailed description of the product"
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
        min_items=5,
        title="Product Features",
        description="Up to 5 product features with a hook and description"
    )

    class Config:
        schema_extra = {
            "example": {
                "title": "Comfortable Cotton T-Shirt",
                "tagline": "Soft and breathable everyday wear",
                "bullet_points": [
                    "100% cotton material",
                    "Relaxed fit design",
                    "Available in multiple colors",
                    "Machine washable",
                    "Eco-friendly packaging"
                ],
                "description": "This comfortable cotton T-shirt is perfect for casual wear. Made from 100% breathable cotton, it features a relaxed fit and is available in various colors. It's easy to maintain and eco-friendly.",
                "tags": ["clothing", "cotton", "casual", "t-shirt"],
                "options": [
                    {
                        "name": "Color",
                        "values": ["Red", "Blue", "Green", "Black"]
                    },
                    {
                        "name": "Size",
                        "values": ["Small", "Medium", "Large", "Extra Large"]
                    },
                    {
                        "name": "Material",
                        "values": ["Cotton"]
                    },
                    {
                        "name": "Fit",
                        "values": ["Relaxed", "Regular", "Slim"]
                    }
                ],
                "variants": [
                    {
                        "title": "Red - Small",
                        "option1": "Red",
                        "option2": "Small",
                        "option3": None,
                        "price": 19.99,
                        "sku": "TSHIRT-RED-S",
                        "inventory_quantity": 100
                    },
                    {
                        "title": "Blue - Medium",
                        "option1": "Blue",
                        "option2": "Medium",
                        "option3": None,
                        "price": 19.99,
                        "sku": "TSHIRT-BLUE-M",
                        "inventory_quantity": 150
                    }
                ],
                "category": "Clothing",
                "vendor": "Cotton Co.",
                "average_rating": 4.7,
                "features": [
                    {
                        "hook": "Breathable Fabric",
                        "description": "The fabric allows air circulation, keeping you cool throughout the day."
                    },
                    {
                        "hook": "Eco-Friendly",
                        "description": "Packaged using sustainable materials, reducing environmental impact."
                    },
                    {
                        "hook": "Relaxed Fit",
                        "description": "Designed to provide comfort and a relaxed fit for all-day wear."
                    },
                    {
                        "hook": "Durable Material",
                        "description": "High-quality stitching ensures long-lasting durability."
                    },
                    {
                        "hook": "Machine Washable",
                        "description": "Easy to clean and maintain with machine-washable fabric."
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


# print()

def save_schema(db):
    product_schema = "Product"
    product_descriptions_schema = "Description"
    product_review_schema = "ProductReview"

    schema = {
        "file_name": "template_1",
        "is_descriptions": True,
        "descriptions_count": 4,
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

    template_id = os.getenv("TEMPLATE_1_ID")
    cursor = db.cursor(dictionary=True)
    sql = "UPDATE product_templates SET template_schema = %s WHERE id = %s"
    cursor.execute(sql, (json.dumps(schema), template_id))
    db.commit()

    cursor.close()
    db.close()
