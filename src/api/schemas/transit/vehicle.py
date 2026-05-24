from pydantic import BaseModel


class Vehicle(BaseModel):
    name: str | None = None
    name_inflection: str | None = None
    image: str | None = None
