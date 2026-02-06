"""Student storage implementation with JSON persistence."""


from typing import ClassVar

from ..dto.student_dto import StudentDTO
from .base import BaseStorage


class StudentStorage(BaseStorage[StudentDTO]):
    """Storage implementation for students with JSON persistence."""
    
    dto_class: ClassVar[type[StudentDTO]] = StudentDTO
    id_field = "user_id"
