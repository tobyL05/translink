from pydantic import BaseModel


class ActivePeriod(BaseModel):
    start: int | None = None
    end: int | None = None
