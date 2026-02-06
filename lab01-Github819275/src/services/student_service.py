"""Student service module for the University Course Management System."""
from src.core import StorageSystem
from src.core.dto import StudentDTO
from src.core.entities import Student


class StudentService:
    """Service class to handle student management logic."""
    
    def __init__(self, storage_system: StorageSystem) -> None:
        """Initialize the StudentService with required dependencies."""
        self.storage_system = storage_system

    def get_all_students(self) -> list[Student | None]:
        """Retrieve all student entities from storage."""
        return self.storage_system.get_all_students()

    def add_student(self, student_dto: StudentDTO) -> Student | None:
        """Add a new student to the storage system."""
        student_storage = self.storage_system.student_storage

        # Check if student already exists
        if student_storage.get_by_id(student_dto.user_id) is not None:
            raise ValueError(f"Student with ID {student_dto.user_id} already exists")

        # Add the student
        student_storage.add(student_dto)
        return self.storage_system.get_student(student_dto.user_id)

    def get_student(self, student_id: str) -> Student:
        """Retrieve a student by ID."""
        student = self.storage_system.get_student(student_id)
        if student is None:
            raise ValueError(f"Student with ID {student_id} not found")
        return student

    def student_exists(self, student_id: str) -> bool:
        """Check if a student exists in storage."""
        student_storage = self.storage_system.student_storage
        return student_storage.get_by_id(student_id) is not None

    def remove_student(self, student_id: str) -> None:
        """Remove a student and their enrollments."""
        student_storage = self.storage_system.student_storage
        enrollment_storage = self.storage_system.enrollment_storage

        if student_storage.get_by_id(student_id) is None:
            raise ValueError(f"Student with ID {student_id} not found")

        # Remove all enrollments linked to this student
        enrollments = enrollment_storage.get_by_student_id(student_id)
        for enrollment in enrollments:
            enrollment_storage.delete(enrollment.id)

        # Remove the student
        student_storage.delete(student_id)

    def get_transcript(self, student_id: str) -> dict:
        """Return a student's transcript (completed courses and grades)."""
        # Check if student exists
        student = self.storage_system.get_student(student_id)
        if student is None:
            raise ValueError(f"Student with ID {student_id} not found")

        # Gather completed enrollments
        enrollment_storage = self.storage_system.enrollment_storage
        enrollments = enrollment_storage.get_by_student_id(student_id)

        # Return a dict of completed courses and grades
        transcript = {
            e.course_id: e.grade for e in enrollments if e.status == "completed"
        }
        return transcript
