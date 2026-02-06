"""Student Data Transfer Object."""

from pydantic import BaseModel


class StudentDTO(BaseModel):
    """
    Student Data Transfer Object.
    """
    user_id: str
    name: str