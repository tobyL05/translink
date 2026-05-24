from pydantic import BaseModel


class Price(BaseModel):
    currency_code: str
    symbol: str
    text: str
    value: float
