"""Enrollment service module for the University Course Management System."""
import uuid

from src.core import StorageSystem
from src.core.dto import EnrollmentDTO
from src.core.entities import Course, Student
from src.exceptions import (
    AlreadyEnrolledError,
    CourseFullError,
    CourseNotFoundError,
    EnrollmentError,
    ScheduleConflictError,
)


class EnrollmentService:
    """Service class to handle course enrollment logic."""
    
    def __init__(self, storage_system: StorageSystem) -> None:
        """Initialize the EnrollmentService with required dependencies."""
        self.storage_system = storage_system

    def enroll_student_in_course(self, student_id: str, course_id: str) -> EnrollmentDTO:
        """Enroll a student in a course, checking for conflicts and capacity."""
        enrollment_storage = self.storage_system.enrollment_storage
        status = "enrolled"
        grade = None

        student = self.storage_system.get_student(student_id)
        if student is None:
            raise ValueError(f"Student with ID {student_id} not found")
        
        course = self.storage_system.get_course(course_id)
        if course is None:
            raise CourseNotFoundError(f"Course with ID {course_id} not found")
        
        # Check if already enrolled
        existing_enrollments = enrollment_storage.get_by_student_id(student_id)
        if any(e.course_id == course_id and e.status == "enrolled" for e in existing_enrollments):
            raise AlreadyEnrolledError(course_id)
        
        # Check if course is full
        
        enrolled_students = [e for e in enrollment_storage.get_by_course_id(course_id) if e.status == "enrolled"]
        if len(enrolled_students) >= course.capacity:
            raise CourseFullError(course_id)

        # Check for schedule conflicts
        for e in existing_enrollments:
            if e.status == "enrolled":
                self._validate_no_time_conflict(e.course_id, course)

        id = str(uuid.uuid4())
        enrollment_dto = EnrollmentDTO(
            id=id,
            student_id=student_id,
            course_id=course_id,
            status=status,
            grade=grade
        )
        enrollment = enrollment_storage.add(enrollment_dto)
        return enrollment
    
    def _validate_no_time_conflict(self, enrolled_course_id: str, new_course: Course) -> None:
        enrolled_course = self.storage_system.get_course(enrolled_course_id)
        if enrolled_course is not None and enrolled_course.has_time_conflict(new_course):
            raise ScheduleConflictError(new_course.id, enrolled_course.id)

    def drop_course(self, student_id: str, course_id: str) -> bool:
        """Drop a course for a student."""
        # Check if student exists
        student = self.storage_system.get_student(student_id)
        if student is None:
            raise ValueError(f"Student with ID {student_id} not found")
        
        # Check if course exists
        course = self.storage_system.get_course(course_id)
        if course is None:
            raise CourseNotFoundError(f"Course with ID {course_id} not found")
        
        
        enrollment_storage = self.storage_system.enrollment_storage
        enrollments = enrollment_storage.get_by_student_id(student_id)
        for enrollment in enrollments:
            if enrollment.course_id == course_id and enrollment.status == "enrolled":
                enrollment.status = "dropped"
                enrollment_storage.update(enrollment)
                return True
        raise ValueError(f"Student {student_id} is not enrolled in course {course_id}.")
    
    def complete_course(self, student_id: str, course_id: str, grade: str) -> bool:
        """Mark a course as completed for a student with a grade."""

        enrollment_storage = self.storage_system.enrollment_storage
        enrollments = enrollment_storage.get_by_student_id(student_id)
        
        for enrollment in enrollments:
            if enrollment.course_id == course_id and enrollment.status == "enrolled":
                
                enrollment.status = "completed"
                enrollment.grade = grade
                
                
                enrollment_storage.update(enrollment)
                return True
        raise ValueError(f"Student {student_id} is not enrolled in course {course_id}")
    
    def get_student_enrollments(self, student_id: str) -> list[EnrollmentDTO]:
        """Retrieve all enrollments for a given student ID."""

        # Check if student exists
        student = self.storage_system.get_student(student_id)
        if student is None:
            raise ValueError(f"Student with ID {student_id} not found")
        enrollment_storage = self.storage_system.enrollment_storage
        return enrollment_storage.get_by_student_id(student_id)
    
    def get_course_enrollments(self, course_id: str) -> list[EnrollmentDTO]:
        """Retrieve all enrollments for a given course ID."""
        
        # Check if course exists
        course = self.storage_system.get_course(course_id)
        if course is None:
            raise ValueError(f"Course with ID {course_id} not found")
        
        enrollment_storage = self.storage_system.enrollment_storage
        return enrollment_storage.get_by_course_id(course_id)