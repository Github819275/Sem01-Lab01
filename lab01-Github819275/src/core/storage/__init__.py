"""Storage package for the University Management System."""

from src.core.storage.base import BaseStorage
from src.core.storage.course_storage import CourseStorage
from src.core.storage.enrollment_storage import EnrollmentStorage
from src.core.storage.staff_storage import StaffStorage
from src.core.storage.student_storage import StudentStorage

__all__ = [
    'BaseStorage',
    'StudentStorage', 
    'StaffStorage',
    'CourseStorage',
    'EnrollmentStorage'
] 