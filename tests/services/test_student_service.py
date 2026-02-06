"""
Tests for StudentService using the new core storage system.

These tests focus on student-specific functionality following the
single responsibility principle.
"""
import tempfile
import pytest
from pathlib import Path

from src.core import StorageSystem
from src.core.dto import StudentDTO, EnrollmentDTO
from src.core.entities import Student
from src.services.student_service import StudentService


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
def student_service(storage_system):
    """Create a StudentService instance."""
    return StudentService(storage_system)


@pytest.fixture
def sample_student_dto():
    """Create a sample StudentDTO."""
    return StudentDTO(user_id="student123", name="John Doe")


class TestStudentService:
    """Test class for StudentService functionality."""
    
    def test_get_all_students_empty(self, student_service):
        """Test getting all students when none exist."""
        students = student_service.get_all_students()
        assert students == []
    
    def test_add_student_basic(self, student_service, sample_student_dto):
        """Test adding a basic student."""
        student = student_service.add_student(sample_student_dto)
        
        assert student is not None
        assert isinstance(student, Student)
        assert student.user_id == sample_student_dto.user_id
        assert student.name == sample_student_dto.name
        assert student.enrolled_courses_ids == []
        assert student.completed_courses == {}
    
    def test_add_student_duplicate_raises_error(self, student_service, sample_student_dto):
        """Test that adding duplicate student raises ValueError."""
        # Add student first time
        student_service.add_student(sample_student_dto)
        
        # Try to add again
        with pytest.raises(ValueError) as exc_info:
            student_service.add_student(sample_student_dto)
        
        assert f"Student with ID {sample_student_dto.user_id} already exists" in str(exc_info.value)
    
    def test_get_student_found(self, student_service, sample_student_dto):
        """Test retrieving an existing student."""
        added_student = student_service.add_student(sample_student_dto)
        
        retrieved_student = student_service.get_student(sample_student_dto.user_id)
        
        assert retrieved_student is not None
        assert isinstance(retrieved_student, Student)
        assert retrieved_student.user_id == added_student.user_id
        assert retrieved_student.name == added_student.name
    
    def test_get_student_not_found_raises_error(self, student_service):
        """Test retrieving a non-existent student raises ValueError."""
        with pytest.raises(ValueError) as exc_info:
            student_service.get_student("nonexistent-id")
        
        assert "Student with ID nonexistent-id not found" in str(exc_info.value)
    
    def test_get_all_students_populated(self, student_service):
        """Test getting all students when multiple exist."""
        student1_dto = StudentDTO(user_id="student1", name="Student One")
        student2_dto = StudentDTO(user_id="student2", name="Student Two")
        
        student1 = student_service.add_student(student1_dto)
        student2 = student_service.add_student(student2_dto)
        
        students = student_service.get_all_students()
        
        assert len(students) == 2
        assert all(isinstance(s, Student) for s in students)
        student_ids = {s.user_id for s in students}
        assert student_ids == {"student1", "student2"}
    
    def test_student_exists_true(self, student_service, sample_student_dto):
        """Test student existence check for existing student."""
        student_service.add_student(sample_student_dto)
        assert student_service.student_exists(sample_student_dto.user_id) is True
    
    def test_student_exists_false(self, student_service):
        """Test student existence check for non-existent student."""
        assert student_service.student_exists("fake-id") is False
    
    def test_remove_student_basic(self, student_service, sample_student_dto):
        """Test removing a student."""
        student_service.add_student(sample_student_dto)
        student_id = sample_student_dto.user_id
        
        # Verify it exists
        assert student_service.student_exists(student_id) is True
        
        # Remove it
        student_service.remove_student(student_id)
        
        # Verify it's gone
        assert student_service.student_exists(student_id) is False
        with pytest.raises(ValueError):
            student_service.get_student(student_id)
    
    def test_remove_student_not_found_raises_error(self, student_service):
        """Test removing a non-existent student raises ValueError."""
        with pytest.raises(ValueError) as exc_info:
            student_service.remove_student("nonexistent-id")
        
        assert "Student with ID nonexistent-id not found" in str(exc_info.value)
    
    def test_remove_student_with_enrollments(self, student_service, storage_system, sample_student_dto):
        """Test removing a student with enrollments removes the enrollments too."""
        # Add student
        student = student_service.add_student(sample_student_dto)
        
        # Create enrollment (using storage system directly for test setup)
        enrollment_dto = EnrollmentDTO(
            id="enroll123",
            student_id=student.user_id,
            course_id="course123",
            status="enrolled"
        )
        storage_system.enrollment_storage.add(enrollment_dto)
        
        # Verify enrollment exists
        enrollments = storage_system.enrollment_storage.get_by_student_id(student.user_id)
        assert len(enrollments) == 1
        
        # Remove student
        student_service.remove_student(student.user_id)
        
        # Verify student and enrollments are gone
        assert student_service.student_exists(student.user_id) is False
        enrollments_after = storage_system.enrollment_storage.get_by_student_id(student.user_id)
        assert len(enrollments_after) == 0
    
    def test_get_transcript_basic(self, student_service, storage_system, sample_student_dto):
        """Test getting a student's transcript."""
        # Add student
        student = student_service.add_student(sample_student_dto)
        
        # Create completed enrollment (using storage system directly for test setup)
        enrollment_dto = EnrollmentDTO(
            id="enroll123",
            student_id=student.user_id,
            course_id="course123",
            status="completed",
            grade="A"
        )
        storage_system.enrollment_storage.add(enrollment_dto)
        
        # Get transcript
        transcript = student_service.get_transcript(student.user_id)
        
        # For this test, we'll just check that it returns a dictionary
        assert isinstance(transcript, dict)
    
    def test_get_transcript_student_not_found_raises_error(self, student_service):
        """Test getting transcript for non-existent student raises ValueError."""
        with pytest.raises(ValueError) as exc_info:
            student_service.get_transcript("nonexistent-id")
        
        assert "Student with ID nonexistent-id not found" in str(exc_info.value)
    
    def test_student_service_persistence(self, temp_data_dir):
        """Test that students persist across service instances."""
        student_dto = StudentDTO(user_id="persistent_student", name="Persistent Student")
        
        # Create first service instance and add student
        storage1 = StorageSystem(temp_data_dir)
        service1 = StudentService(storage1)
        service1.add_student(student_dto)
        
        # Create second service instance with same data directory
        storage2 = StorageSystem(temp_data_dir)
        service2 = StudentService(storage2)
        
        # Verify student persists
        student = service2.get_student("persistent_student")
        
        assert student is not None
        assert isinstance(student, Student)
        assert student.name == "Persistent Student" 