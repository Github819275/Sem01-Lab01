"""
Tests for CourseService using the new core storage system.

These tests focus on essential functionality and use the StorageSystem
with temporary files for isolation.
"""
import tempfile
import pytest
import uuid
from pathlib import Path

from src.core import StorageSystem
from src.core.dto import CourseDTO, TimeSlotDTO
from src.services.course_service import CourseService


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
def course_service(storage_system):
    """Create a CourseService instance."""
    return CourseService(storage_system)


@pytest.fixture
def sample_time_slot():
    """Create a sample time slot."""
    return TimeSlotDTO(weekday=1, start_time="09:00:00", duration=3600)


@pytest.fixture
def sample_course_dto():
    """Create a sample CourseDTO."""
    return CourseDTO(
        id=str(uuid.uuid4()),
        name="Introduction to Programming",
        capacity=25
    )


class TestCourseService:
    """Test class for CourseService functionality."""
    
    def test_get_all_courses_empty(self, course_service):
        """Test getting all courses when none exist."""
        courses = course_service.get_all_courses()
        assert courses == [], f"Expected get_all_courses to return empty list when no courses exist, but got: {courses}"
    
    def test_add_course_basic(self, course_service, sample_course_dto):
        """Test adding a basic course."""
        course = course_service.add_course(sample_course_dto)
        
        assert course is not None, f"Expected add_course to return a course entity, but got None"
        assert course.id == sample_course_dto.id, f"Expected course id to be {sample_course_dto.id}, but got: {course.id}"
        assert course.name == sample_course_dto.name, f"Expected course name to be {sample_course_dto.name}, but got: {course.name}"
        assert course.capacity == sample_course_dto.capacity, f"Expected course capacity to be {sample_course_dto.capacity}, but got: {course.capacity}"
        assert course.instructor_id is None, f"Expected course instructor_id to be None by default, but got: {course.instructor_id}"
        assert course.time_slot is None, f"Expected course time_slot to be None by default, but got: {course.time_slot}"
    
    def test_add_course_with_all_fields(self, course_service, sample_time_slot):
        """Test adding a course with all fields."""
        course_dto = CourseDTO(
            id=str(uuid.uuid4()),
            name="Advanced Algorithms",
            capacity=20,
            instructor_id="staff123",
            time_slot=sample_time_slot
        )
        
        course = course_service.add_course(course_dto)
        
        assert course.name == "Advanced Algorithms", f"Expected course name to be 'Advanced Algorithms', but got: {course.name}"
        assert course.capacity == 20, f"Expected course capacity to be 20, but got: {course.capacity}"
        assert course.instructor_id == "staff123", f"Expected course instructor_id to be 'staff123', but got: {course.instructor_id}"
        assert course.time_slot == sample_time_slot, f"Expected course time_slot to be {sample_time_slot}, but got: {course.time_slot}"
    
    def test_add_course_duplicate_raises_error(self, course_service, sample_course_dto):
        """Test that adding a duplicate course raises ValueError."""
        # Add course first time
        course_service.add_course(sample_course_dto)
        
        # Try to add the same course again
        with pytest.raises(ValueError) as exc_info:
            course_service.add_course(sample_course_dto)
        
        assert "Failed to add course" in str(exc_info.value), f"Expected error message to contain 'Failed to add course', but got: {str(exc_info.value)}"
    
    def test_get_course_found(self, course_service, sample_course_dto):
        """Test retrieving an existing course."""
        added_course = course_service.add_course(sample_course_dto)
        
        retrieved_course = course_service.get_course(added_course.id)
        
        assert retrieved_course is not None, f"Expected get_course to return a course entity, but got None"
        assert retrieved_course.id == added_course.id, f"Expected retrieved course id to be {added_course.id}, but got: {retrieved_course.id}"
        assert retrieved_course.name == sample_course_dto.name, f"Expected retrieved course name to be {sample_course_dto.name}, but got: {retrieved_course.name}"
    
    def test_get_course_not_found_raises_error(self, course_service):
        """Test retrieving a non-existent course raises ValueError."""
        with pytest.raises(ValueError) as exc_info:
            course_service.get_course("nonexistent-id")
        
        assert "Course with ID nonexistent-id not found" in str(exc_info.value), f"Expected error message to contain 'Course with ID nonexistent-id not found', but got: {str(exc_info.value)}"
    
    def test_get_all_courses_populated(self, course_service):
        """Test getting all courses when multiple exist."""
        course_dto1 = CourseDTO(id=str(uuid.uuid4()), name="Course 1")
        course_dto2 = CourseDTO(id=str(uuid.uuid4()), name="Course 2")
        
        course1 = course_service.add_course(course_dto1)
        course2 = course_service.add_course(course_dto2)
        
        all_courses = course_service.get_all_courses()
        
        assert len(all_courses) == 2, f"Expected get_all_courses to return 2 courses, but got: {len(all_courses)}"
        course_ids = {c.id for c in all_courses}
        assert course1.id in course_ids, f"Expected course1 id {course1.id} to be in returned courses, but course_ids were: {course_ids}"
        assert course2.id in course_ids, f"Expected course2 id {course2.id} to be in returned courses, but course_ids were: {course_ids}"
    
    def test_remove_course_existing(self, course_service, sample_course_dto):
        """Test removing an existing course."""
        course = course_service.add_course(sample_course_dto)
        course_id = course.id
        
        # Verify it exists
        assert course_service.get_course(course_id) is not None, f"Expected course {course_id} to exist before removal, but get_course returned None"
        
        # Remove it
        course_service.remove_course(course_id)
        
        # Verify it's gone
        with pytest.raises(ValueError):
            course_service.get_course(course_id)
    
    def test_remove_course_not_found_raises_error(self, course_service):
        """Test removing a non-existent course raises ValueError."""
        with pytest.raises(ValueError) as exc_info:
            course_service.remove_course("nonexistent-id")
        
        assert "Course with ID nonexistent-id not found" in str(exc_info.value), f"Expected error message to contain 'Course with ID nonexistent-id not found', but got: {str(exc_info.value)}"
    
    def test_remove_course_with_enrollments(self, course_service, storage_system, sample_course_dto):
        """Test removing a course that has enrollments."""
        # Add course
        course = course_service.add_course(sample_course_dto)
        
        # Add a student (using storage system directly for test setup)
        from src.core.dto import StudentDTO, EnrollmentDTO
        student_dto = StudentDTO(user_id="student123", name="Test Student")
        storage_system.student_storage.add(student_dto)
        
        # Create enrollment
        enrollment_dto = EnrollmentDTO(
            id="enroll123",
            student_id="student123",
            course_id=course.id,
            status="enrolled"
        )
        storage_system.enrollment_storage.add(enrollment_dto)
        
        # Verify enrollment exists
        enrollments = storage_system.enrollment_storage.get_by_course_id(course.id)
        assert len(enrollments) == 1, f"Expected 1 enrollment before course removal, but found: {len(enrollments)}"
        
        # Remove course
        course_service.remove_course(course.id)
        
        # Verify course and enrollments are gone
        with pytest.raises(ValueError):
            course_service.get_course(course.id)
        enrollments_after = storage_system.enrollment_storage.get_by_course_id(course.id)
        assert len(enrollments_after) == 0, f"Expected 0 enrollments after course removal, but found: {len(enrollments_after)}"
    
    def test_course_service_persistence(self, temp_data_dir):
        """Test that courses persist across service instances."""
        course_dto = CourseDTO(id=str(uuid.uuid4()), name="Persistent Course")
        
        # Create first service instance and add course
        storage1 = StorageSystem(temp_data_dir)
        service1 = CourseService(storage1)
        course = service1.add_course(course_dto)
        course_id = course.id
        
        # Create second service instance with same data directory
        storage2 = StorageSystem(temp_data_dir)
        service2 = CourseService(storage2)
        
        # Verify course persists
        retrieved_course = service2.get_course(course_id)
        assert retrieved_course is not None, f"Expected course to persist across service instances, but get_course returned None"
        assert retrieved_course.name == "Persistent Course", f"Expected persistent course name to be 'Persistent Course', but got: {retrieved_course.name}" 