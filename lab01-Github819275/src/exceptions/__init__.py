"""Exceptions package for the University Course Management System."""
# Import exception classes for easier access
from src.exceptions.enrollment_errors import (
    AlreadyEnrolledError,
    CourseFullError,
    CourseNotFoundError,
    EnrollmentError,
    ScheduleConflictError,
)

__all__ = [
    'EnrollmentError',
    'ScheduleConflictError',
    'CourseFullError',
    'AlreadyEnrolledError',
    'CourseNotFoundError'
]