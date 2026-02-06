"""
Data Transfer Objects (DTOs) package.

These classes represent data exactly as stored in JSON files,
providing a clean interface between storage and business logic.
"""

from src.core.dto.course_dto import CourseDTO, TimeSlotDTO
from src.core.dto.enrollment_dto import EnrollmentDTO
from src.core.dto.staff_dto import StaffDTO
from src.core.dto.student_dto import StudentDTO

__all__ = ['StudentDTO', 'StaffDTO', 'CourseDTO', 'TimeSlotDTO', 'EnrollmentDTO'] 