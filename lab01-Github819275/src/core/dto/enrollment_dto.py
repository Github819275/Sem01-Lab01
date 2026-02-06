"""Enrollment Data Transfer Object."""

from pydantic import BaseModel


class EnrollmentDTO(BaseModel):
    """
    Enrollment Data Transfer Object.
    """
    id: str
    student_id: str
    course_id: str
    status: str
    grade: str | None = None