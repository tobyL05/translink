from pydantic import BaseModel


class DisplayShortName(BaseModel):
    elements: list[str | None]
    route_name_redundancy: bool | None = None
    boxed_text: str | None = None
