
from pydantic import BaseModel, Field

class OrderPlaceRequest(BaseModel):
    product_id: int = Field(
        ...,
        description="Provide the product ID for placing an order.",
        example=11
    )
    stock_quantity: int = Field(
        ...,
        description="Provide the quantity of product to order.",
        ge=1,
        example=20
    )
