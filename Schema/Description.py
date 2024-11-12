from pydantic import BaseModel, Field

class Description(BaseModel):
    """Product description."""
    hook: str = Field(..., title="Product Hook", description="Engaging hook for the product")
    description: str = Field(..., title="Product Description", description="Description of the product")