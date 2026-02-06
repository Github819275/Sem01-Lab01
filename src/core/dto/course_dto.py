"""Course and TimeSlot Data Transfer Objects."""

from pydantic import BaseModel, Field


class TimeSlotDTO(BaseModel):
    """
    Time Slot Data Transfer Object.
    """
    weekday: int = Field(ge=1, le=7)  # pyrefly: ignore[no-matching-overload]
    # 1=Monday, 7=Sunday 
    start_time: str = Field(pattern=r'^([01]?[0-9]|2[0-3]):[0-5][0-9](:\d{2})?$')  
    # Format ("HH:MM"), seconds fixed to "00" or blank
    duration: int  # Duration in minutes


class CourseDTO(BaseModel):
    """
    Course Data Transfer Object.
    """
    id: str
    name: str
    time_slot: TimeSlotDTO | None = None
    capacity: int = 30
    instructor_id : str | None = None

