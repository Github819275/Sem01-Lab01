"""Enrollment storage implementation with JSON persistence."""


from typing import ClassVar

from ..dto.enrollment_dto import EnrollmentDTO
from .base import BaseStorage


class EnrollmentStorage(BaseStorage[EnrollmentDTO]):
    """Storage implementation for enrollments with JSON persistence."""

    dto_class: ClassVar[type[EnrollmentDTO]] = EnrollmentDTO

    # keep the 2 unique functions for getting by student and course id 
    
    def get_by_student_id(self, student_id: str) -> list[EnrollmentDTO]:
        """Retrieve all enrollments for a given student ID."""
        data = self._load_from_file()
        return [EnrollmentDTO.model_validate(item) 
                for item in data 
                if EnrollmentDTO.model_validate(item).student_id == student_id]
    
    def get_by_course_id(self, course_id: str) -> list[EnrollmentDTO]:
        """Retrieve all enrollments for a given course ID."""
        data = self._load_from_file()
        return [EnrollmentDTO.model_validate(item) 
                for item in data 
                if EnrollmentDTO.model_validate(item).course_id == course_id
                ]

    