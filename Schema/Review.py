from pydantic.v1 import BaseModel, Field
from enum import Enum


class Gender(str, Enum):
    """Gender of the reviewer."""
    male = 'm'
    female = 'f'


class ProductReview(BaseModel):
    """Product description."""
    rating: float = Field(..., title="Rating",
                          description="Rating out of 5 minimum 4.5")
    comment: str = Field(..., title="Review Comment",
                         description="Review text from the customer")
    date: str = Field(..., title="Review Date",
                      description="Date of the review")
