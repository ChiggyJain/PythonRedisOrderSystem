
from pydantic import BaseModel, Field

class ProductListRequest(BaseModel):
    token: str = Field(
        ...,
        description="Provide the session token obtained after successful login.",
        examples=["9c8b12e1-fad1-4ed3-85c0-230af91ad2c1"]
    )

class ProductDetailRequest(BaseModel):
    product_id: int = Field(
        ...,
        description="Provide the product ID.",
        examples=[11,12,13]
    )    