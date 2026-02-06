"""Course storage implementation with JSON persistence."""


from typing import ClassVar

from ..dto.course_dto import CourseDTO
from .base import BaseStorage


class CourseStorage(BaseStorage[CourseDTO]):
    """Storage implementation for courses with JSON persistence."""
    
    dto_class: ClassVar[type[CourseDTO]] = CourseDTO

    # This derived class needs it's own add method to enforce the unique error message.

    def add(self, entity: CourseDTO) -> CourseDTO:
        """Add a new course."""
        data = self._load_from_file()

        if any(CourseDTO.model_validate(item).id == entity.id for item in data):
            raise ValueError(f"Failed to add course. Course with id '{entity.id}' already exists.")

        data.append(entity.model_dump())
        self._save_to_file(data)
        return entity