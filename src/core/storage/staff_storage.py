"""Staff storage implementation with JSON persistence."""


from typing import ClassVar

from ..dto.staff_dto import StaffDTO
from .base import BaseStorage


class StaffStorage(BaseStorage[StaffDTO]):
    """Storage implementation for staff with JSON persistence."""
    
    dto_class: ClassVar[type[StaffDTO]] = StaffDTO
    id_field = "user_id"