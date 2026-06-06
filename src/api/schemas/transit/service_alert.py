from typing import Literal
from pydantic import BaseModel

from .active_period import ActivePeriod
from .informed_entity import InformedEntity


class ServiceAlert(BaseModel):
    effect: Literal[
        "NO_SERVICE", "REDUCED_SERVICE", "SIGNIFICANT_DELAYS", "DETOUR",
        "ADDITIONAL_SERVICE", "MODIFIED_SERVICE", "OTHER_EFFECT",
        "UNKNOWN_EFFECT", "STOP_MOVED", "NO_EFFECT", "TRIP_CANCELLED",
    ]
    cause: Literal[
        "UNKNOWN_CAUSE", "OTHER_CAUSE", "TECHNICAL_PROBLEM", "STRIKE",
        "DEMONSTRATION", "ACCIDENT", "HOLIDAY", "WEATHER", "MAINTENANCE",
        "CONSTRUCTION", "POLICE_ACTIVITY", "MEDICAL_EMERGENCY",
    ]
    severity: Literal["Unknown", "Info", "Warning", "Severe"]
    description: str
    created_at: int
    informed_entities: list[InformedEntity]
    title: str | None = None
    active_periods: list[ActivePeriod] = []
