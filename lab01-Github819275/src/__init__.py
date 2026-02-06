"""University Course Management System package initialization."""
from pathlib import Path

from src.core import StorageSystem
from src.services.course_service import CourseService
from src.services.enrollment_service import EnrollmentService
from src.services.staff_service import StaffService
from src.services.student_service import StudentService


class DependencyContainer:
    """Dependency injection container for the University Course Management System."""
    
    def __init__(self, data_dir: str) -> None:
        """Initialize the dependency container."""
        self.data_dir = Path(data_dir)
        
        # Create storage system
        self.storage_system = StorageSystem(self.data_dir)
        
        # Create service instances with injected dependencies
        self.course_service = CourseService(self.storage_system)
        self.student_service = StudentService(self.storage_system)
        self.staff_service = StaffService(self.storage_system)
        self.enrollment_service = EnrollmentService(self.storage_system)
