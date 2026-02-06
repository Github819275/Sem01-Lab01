"""
Entities package for the University Management System.

Rich domain models that include business logic and relationships,
built on top of the simpler DTOs.
"""

from src.core.entities.course import Course
from src.core.entities.staff import Staff
from src.core.entities.student import Student

__all__ = ['Student', 'Staff', 'Course'] 