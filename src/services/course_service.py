"""Course service module for the University Course Management System."""

from src.core import StorageSystem
from src.core.dto import CourseDTO
from src.core.entities import Course


class CourseService:
    """Service class to handle course management logic."""
    
    def __init__(self, storage_system: StorageSystem) -> None:
        """Initialize the CourseService with required dependencies."""
        self.storage_system = storage_system
    
    def get_all_courses(self) -> list[Course | None]:
        """Retrieve all courses from the storage system."""
        return self.storage_system.get_all_courses()
    
    def add_course(self, course_dto: CourseDTO) -> Course | None:
        """Add a new course to the storage system."""
        course_storage = self.storage_system.course_storage
        return_course_dto = course_storage.add(course_dto)
        course = self.storage_system.get_course(return_course_dto.id)
        return course
    
    def get_course(self, course_id: str) -> Course | None:
        """Retrieve a course by its ID."""
        course = self.storage_system.get_course(course_id)
        if course is None:
            raise ValueError(f"Course with ID {course_id} not found")
        return course
    
    def remove_course(self, course_id: str) -> None:
        """Remove a course by its ID."""
        course_storage = self.storage_system.course_storage
        enrollment_storage = self.storage_system.enrollment_storage
        
        # Check if course exists
        course = course_storage.get_by_id(course_id)
        if course is None:
            raise ValueError(f"Course with ID {course_id} not found")
        
        # Remove enrollments associated with the course
        enrollments = enrollment_storage.get_by_course_id(course_id)
        for enrollment in enrollments:
            enrollment_storage.delete(enrollment.id)
        
        # Remove the course
        success = course_storage.delete(course_id)
        if not success:
            raise ValueError(f"Failed to remove course with ID {course_id}")

    