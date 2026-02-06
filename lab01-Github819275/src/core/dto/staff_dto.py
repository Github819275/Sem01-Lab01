"""Staff Data Transfer Object."""

from pydantic import BaseModel


class StaffDTO(BaseModel):
    """
    Staff Data Transfer Object.
    """
    user_id: str
    name: str
    department: str