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
        description="Catchy phrase summarizing the core value (3-5 words, 40-46 characters)"
    )

    description: str = Field(
        ...,
        title="Product Description",
        description="Explanation of what sets us apart (22-26 words 162-168 characters)"
    )


class ProductFeature(BaseModel):
    hook: str = Field(
        ...,
        title="Feature Hook",
        description="Short title of the feature (2-4 words, 15-20 characters)"
    )

    description: str = Field(
        ...,
        title="Feature Description",
        description="Short description of the feature (10-12 words, 60-65 characters)"
    )


class Product(BaseModel):
    title: str = Field(
        ...,
        title="Product Title",
        description="Title of the product (2-4 words, 15-20 characters)"
    )

    description: str = Field(
        ...,
        title="Product Description",
        description="Detailed description of the product (9-12 words, 70-80 characters)"
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

    descriptions: List[Description] = Field(
        ...,
        min_items=4,
        title="Why Choose Us",
        description="Up to 4 Core Values with a hook and description"
    )

    class Config:
        schema_extra = {
            "example": {
                "title": "Eco-Friendly Water Bottle",
                "description": "A reusable water bottle that keeps drinks cold for 24 hours and hot for 12 hours.",
                "tags": ["water bottle", "eco-friendly", "sustainable", "outdoors"],
                "options": [
                    {
                        "name": "Color",
                        "values": ["Blue", "Green", "Pink", "Black"]
                    },
                    {
                        "name": "Size",
                        "values": ["500ml", "750ml", "1L", "1.5L"]
                    },
                    {
                        "name": "Cap Type",
                        "values": ["Screw Cap", "Flip Top", "Straw Cap"]
                    },
                    {
                        "name": "Material",
                        "values": ["Stainless Steel", "Bamboo", "Plastic"]
                    }
                ],
                "variants": [
                    {
                        "title": "Eco-Friendly Water Bottle - Blue, 500ml, Screw Cap",
                        "option1": "Blue",
                        "option2": "500ml",
                        "option3": "Screw Cap",
                        "price": 19.99,
                        "sku": "EWB-500-BL-SC",
                        "inventory_quantity": 100
                    },
                    {
                        "title": "Eco-Friendly Water Bottle - Green, 750ml, Flip Top",
                        "option1": "Green",
                        "option2": "750ml",
                        "option3": "Flip Top",
                        "price": 24.99,
                        "sku": "EWB-750-GR-FT",
                        "inventory_quantity": 80
                    },
                    {
                        "title": "Eco-Friendly Water Bottle - Pink, 1L, Straw Cap",
                        "option1": "Pink",
                        "option2": "1L",
                        "option3": "Straw Cap",
                        "price": 29.99,
                        "sku": "EWB-1L-PK-SC",
                        "inventory_quantity": 60
                    },
                    {
                        "title": "Eco-Friendly Water Bottle - Black, 1.5L, Screw Cap",
                        "option1": "Black",
                        "option2": "1.5L",
                        "option3": "Screw Cap",
                        "price": 34.99,
                        "sku": "EWB-1.5L-BK-SC",
                        "inventory_quantity": 40
                    }
                ],
                "category": "Beverage Containers",
                "vendor": "EcoGoods",
                "average_rating": 4.9,
                "features": [
                    {
                        "hook": "Keeps Drinks Hot & Cold",
                        "description": "Double-wall vacuum insulation keeps drinks at the perfect temperature."
                    },
                    {
                        "hook": "Eco-Friendly Materials",
                        "description": "Made from sustainable materials, reducing plastic waste."
                    },
                    {
                        "hook": "Durable & Lightweight",
                        "description": "Lightweight design is easy to carry on all your adventures."
                    }
                ],
                "descriptions": [
                    {
                        "hook": "Sustainable Design",
                        "description": "Crafted from recycled materials, reducing environmental impact."
                    },
                    {
                        "hook": "Health Conscious",
                        "description": "BPA-free and safe for you and the planet."
                    },
                    {
                        "hook": "Versatile Use",
                        "description": "Perfect for hiking, gym, or daily hydration."
                    },
                    {
                        "hook": "Stylish & Functional",
                        "description": "Sleek design that fits in your car cup holder."
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
        description="Review text from the customer (35-40 words, 192-200 characters)"
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
        "file_name": "template_6",
        "is_descriptions": False,
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

    template_id = os.getenv("TEMPLATE_6_ID")
    cursor = db.cursor(dictionary=True)
    sql = "UPDATE product_templates SET template_schema = %s WHERE id = %s"
    cursor.execute(sql, (json.dumps(schema), template_id))
    db.commit()

    cursor.close()
    db.close()
