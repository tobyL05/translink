from pydantic import BaseModel

from .price import Price


class Fare(BaseModel):
    fare_media_type: float
    price_min: Price
    price_max: Price
