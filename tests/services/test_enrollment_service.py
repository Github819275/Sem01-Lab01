"""
Tests for EnrollmentService using the new core storage system.

These tests focus on enrollment functionality including validation,
enrollment management, and course completion tracking.
"""
import tempfile
import pytest
import uuid
from pathlib import Path

from src.core import StorageSystem
from src.core.dto import StudentDTO, StaffDTO, CourseDTO, EnrollmentDTO, TimeSlotDTO
from src.core.entities import Student, Staff, Course
from src.services.enrollment_service import EnrollmentService
from src.exceptions import (
    AlreadyEnrolledError,
    CourseFullError,
    CourseNotFoundError,
    ScheduleConflictError,
)


@pytest.fixture
def temp_data_dir():
    """Create a temporary directory for test data."""
    with tempfile.TemporaryDirectory() as temp_dir:
        yield Path(temp_dir)


@pytest.fixture
def storage_system(temp_data_dir):
    """Create a fresh StorageSystem for each test."""
    return StorageSystem(temp_data_dir)


@pytest.fixture
def enrollment_service(storage_system):
    """Create an EnrollmentService instance."""
    return EnrollmentService(storage_system)


@pytest.fixture
def sample_student(storage_system):
    """Create and add a sample student."""
    student_dto = StudentDTO(user_id="student123", name="John Doe")
    storage_system.student_storage.add(student_dto)
    return storage_system.get_student("student123")


@pytest.fixture
def sample_course(storage_system):
    """Create and add a sample course."""
    course_dto = CourseDTO(
        id=str(uuid.uuid4()),
        name="Introduction to Programming",
        capacity=30
    )
    storage_system.course_storage.add(course_dto)
    return storage_system.get_course(course_dto.id)


@pytest.fixture
def full_course(storage_system):
    """Create and add a course that is at capacity."""
    course_dto = CourseDTO(
        id=str(uuid.uuid4()),
        name="Full Course",
        capacity=1
    )
    storage_system.course_storage.add(course_dto)
    
    # Add a student and enroll them to make it full
    student_dto = StudentDTO(user_id="other_student", name="Other Student")
    storage_system.student_storage.add(student_dto)
    
    enrollment_dto = EnrollmentDTO(
        id=str(uuid.uuid4()),
        student_id="other_student",
        course_id=course_dto.id,
        status="enrolled"
    )
    storage_system.enrollment_storage.add(enrollment_dto)
    
    return storage_system.get_course(course_dto.id)


@pytest.fixture
def conflicting_courses(storage_system):
    """Create two courses with conflicting time slots."""
    time_slot = TimeSlotDTO(weekday=1, start_time="09:00:00", duration=3600)
    
    course1_dto = CourseDTO(
        id=str(uuid.uuid4()),
        name="Morning Course 1",
        time_slot=time_slot
    )
    course2_dto = CourseDTO(
        id=str(uuid.uuid4()),
        name="Morning Course 2", 
        time_slot=time_slot
    )
    
    storage_system.course_storage.add(course1_dto)
    storage_system.course_storage.add(course2_dto)
    
    return (
        storage_system.get_course(course1_dto.id),
        storage_system.get_course(course2_dto.id)
    )


class TestEnrollmentService:
    """Test class for EnrollmentService functionality."""
    
    def test_enroll_student_basic_success(self, enrollment_service, sample_student, sample_course):
        """Test basic successful enrollment."""
        enrollment = enrollment_service.enroll_student_in_course(
            sample_student.user_id, sample_course.id
        )
        
        assert enrollment is not None
        assert isinstance(enrollment, EnrollmentDTO)
        assert enrollment.student_id == sample_student.user_id
        assert enrollment.course_id == sample_course.id
        assert enrollment.status == "enrolled"
        assert enrollment.grade is None
    
    def test_enroll_student_invalid_student_id(self, enrollment_service, sample_course):
        """Test enrollment with invalid student ID."""
        with pytest.raises(ValueError) as exc_info:
            enrollment_service.enroll_student_in_course("nonexistent", sample_course.id)
        
        assert "Student with ID nonexistent not found" in str(exc_info.value)
    
    def test_enroll_student_invalid_course_id(self, enrollment_service, sample_student):
        """Test enrollment with invalid course ID."""
        with pytest.raises(CourseNotFoundError) as exc_info:
            enrollment_service.enroll_student_in_course(sample_student.user_id, "nonexistent")
        
        assert "nonexistent" in str(exc_info.value)
    
    def test_enroll_student_not_found(self, enrollment_service, sample_course):
        """Test enrollment with non-existent student."""
        with pytest.raises(ValueError) as exc_info:
            enrollment_service.enroll_student_in_course("nonexistent", sample_course.id)
        
        assert "Student with ID nonexistent not found" in str(exc_info.value)
    
    def test_enroll_course_not_found(self, enrollment_service, sample_student):
        """Test enrollment with non-existent course."""
        with pytest.raises(CourseNotFoundError) as exc_info:
            enrollment_service.enroll_student_in_course(sample_student.user_id, "nonexistent")
        
        assert "nonexistent" in str(exc_info.value)
    
    def test_enroll_already_enrolled(self, enrollment_service, sample_student, sample_course):
        """Test enrollment when student is already enrolled."""
        # First enrollment
        enrollment_service.enroll_student_in_course(sample_student.user_id, sample_course.id)
        
        # Second enrollment should fail
        with pytest.raises(AlreadyEnrolledError) as exc_info:
            enrollment_service.enroll_student_in_course(sample_student.user_id, sample_course.id)
        
        assert sample_course.id in str(exc_info.value)
    
    def test_enroll_course_full(self, enrollment_service, sample_student, full_course):
        """Test enrollment when course is full."""
        with pytest.raises(CourseFullError) as exc_info:
            enrollment_service.enroll_student_in_course(sample_student.user_id, full_course.id)
        
        assert full_course.id in str(exc_info.value)
    
    def test_enroll_schedule_conflict(self, enrollment_service, sample_student, conflicting_courses):
        """Test enrollment with schedule conflict."""
        course1, course2 = conflicting_courses
        
        # Enroll in first course
        enrollment_service.enroll_student_in_course(sample_student.user_id, course1.id)
        
        # Try to enroll in conflicting course
        with pytest.raises(ScheduleConflictError) as exc_info:
            enrollment_service.enroll_student_in_course(sample_student.user_id, course2.id)
        
        assert course2.id in str(exc_info.value)
        assert course1.id in str(exc_info.value)
    
    def test_drop_course_success(self, enrollment_service, sample_student, sample_course, storage_system):
        """Test successful course dropping."""
        # First enroll
        enrollment_service.enroll_student_in_course(sample_student.user_id, sample_course.id)
        
        # Then drop
        enrollment_service.drop_course(sample_student.user_id, sample_course.id)
        
        # Verify enrollment status changed to dropped
        enrollments = storage_system.enrollment_storage.get_by_student_id(sample_student.user_id)
        assert len(enrollments) == 1
        assert enrollments[0].status == "dropped"
    
    def test_drop_course_invalid_student_id(self, enrollment_service, sample_course):
        """Test dropping course with invalid student ID."""
        with pytest.raises(ValueError) as exc_info:
            enrollment_service.drop_course("nonexistent", sample_course.id)
        
        assert "Student with ID nonexistent not found" in str(exc_info.value)
    
    def test_drop_course_invalid_course_id(self, enrollment_service, sample_student):
        """Test dropping course with invalid course ID."""
        with pytest.raises(CourseNotFoundError) as exc_info:
            enrollment_service.drop_course(sample_student.user_id, "nonexistent")
        
        assert "nonexistent" in str(exc_info.value)
    
    def test_drop_course_not_enrolled(self, enrollment_service, sample_student, sample_course):
        """Test dropping course when not enrolled."""
        with pytest.raises(ValueError) as exc_info:
            enrollment_service.drop_course(sample_student.user_id, sample_course.id)
        
        assert f"Student {sample_student.user_id} is not enrolled in course {sample_course.id}" in str(exc_info.value)
    
    def test_complete_course_success(self, enrollment_service, sample_student, sample_course, storage_system):
        """Test successful course completion."""
        # First enroll
        enrollment_service.enroll_student_in_course(sample_student.user_id, sample_course.id)
        
        # Then complete with grade
        enrollment_service.complete_course(sample_student.user_id, sample_course.id, "A")
        
        # Verify enrollment status changed to completed with grade
        enrollments = storage_system.enrollment_storage.get_by_student_id(sample_student.user_id)
        assert len(enrollments) == 1
        assert enrollments[0].status == "completed"
        assert enrollments[0].grade == "A"
    
    def test_complete_course_not_enrolled(self, enrollment_service, sample_student, sample_course):
        """Test completing course when not enrolled."""
        with pytest.raises(ValueError) as exc_info:
            enrollment_service.complete_course(sample_student.user_id, sample_course.id, "A")
        
        assert f"Student {sample_student.user_id} is not enrolled in course {sample_course.id}" in str(exc_info.value)
    
    def test_get_student_enrollments_success(self, enrollment_service, sample_student, sample_course):
        """Test getting student enrollments."""
        # Enroll student
        enrollment_service.enroll_student_in_course(sample_student.user_id, sample_course.id)
        
        # Get enrollments
        enrollments = enrollment_service.get_student_enrollments(sample_student.user_id)
        
        assert len(enrollments) == 1
        assert enrollments[0].student_id == sample_student.user_id
        assert enrollments[0].course_id == sample_course.id
        assert enrollments[0].status == "enrolled"
    
    def test_get_student_enrollments_not_found(self, enrollment_service):
        """Test getting enrollments for non-existent student."""
        with pytest.raises(ValueError) as exc_info:
            enrollment_service.get_student_enrollments("nonexistent")
        
        assert "Student with ID nonexistent not found" in str(exc_info.value)
    
    def test_get_course_enrollments_success(self, enrollment_service, sample_student, sample_course):
        """Test getting course enrollments."""
        # Enroll student
        enrollment_service.enroll_student_in_course(sample_student.user_id, sample_course.id)
        
        # Get enrollments
        enrollments = enrollment_service.get_course_enrollments(sample_course.id)
        
        assert len(enrollments) == 1
        assert enrollments[0].student_id == sample_student.user_id
        assert enrollments[0].course_id == sample_course.id
        assert enrollments[0].status == "enrolled"
    
    def test_get_course_enrollments_invalid_id(self, enrollment_service):
        """Test getting enrollments with invalid course ID."""
        with pytest.raises(ValueError) as exc_info:
            enrollment_service.get_course_enrollments("nonexistent")
        
        assert "Course with ID nonexistent not found" in str(exc_info.value)
    
    def test_get_course_enrollments_not_found(self, enrollment_service):
        """Test getting enrollments for non-existent course."""
        with pytest.raises(ValueError) as exc_info:
            enrollment_service.get_course_enrollments("nonexistent")
        
        assert "Course with ID nonexistent not found" in str(exc_info.value)
    
    def test_enrollment_service_persistence(self, temp_data_dir):
        """Test that enrollments persist across service instances."""
        student_dto = StudentDTO(user_id="persistent_student", name="Persistent Student")
        course_dto = CourseDTO(id="persistent_course", name="Persistent Course")
        
        # Create first service instance and enroll
        storage1 = StorageSystem(temp_data_dir)
        service1 = EnrollmentService(storage1)
        storage1.student_storage.add(student_dto)
        storage1.course_storage.add(course_dto)
        
        enrollment = service1.enroll_student_in_course("persistent_student", "persistent_course")
        
        # Create second service instance with same data directory
        storage2 = StorageSystem(temp_data_dir)
        service2 = EnrollmentService(storage2)
        
        # Verify enrollment persists
        enrollments = service2.get_student_enrollments("persistent_student")
        assert len(enrollments) == 1
        assert enrollments[0].student_id == "persistent_student"
        assert enrollments[0].course_id == "persistent_course"
        assert enrollments[0].status == "enrolled" 