
from pydantic import BaseModel, Field


class ProductDetailRequest(BaseModel):
    product_id: int = Field(
        ...,
        description="Provide the product ID.",
        examples=[11,12,13]
    )

class ProductStockRequest(BaseModel):
    product_id: int = Field(
        ...,
        description="Provide the product ID whose stock needs to be updated.",
        examples=[11]
    )
    stock_quantity: int = Field(
        ...,
        description="Provide the new stock quantity.",
        ge=0,
        examples=[20]
    )    
