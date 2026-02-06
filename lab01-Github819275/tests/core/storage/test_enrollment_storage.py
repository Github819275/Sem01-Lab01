"""
Tests for EnrollmentStorage.

Tests persistence (operations change the file) and correctness (return values, uniqueness).
"""

import json
import tempfile
import pytest
from pathlib import Path

from src.core.storage import EnrollmentStorage
from src.core.dto import EnrollmentDTO


@pytest.fixture
def temp_dir():
    """Create a temporary directory for test files."""
    with tempfile.TemporaryDirectory() as temp_dir:
        yield Path(temp_dir)


@pytest.fixture
def enrollment_storage(temp_dir):
    """Create an EnrollmentStorage instance with temporary file."""
    return EnrollmentStorage(temp_dir / "enrollments.json")


@pytest.fixture
def sample_enrollment():
    """Create a sample enrollment DTO."""
    return EnrollmentDTO(
        id="enr_001",
        student_id="s1001",
        course_id="CS101",
        status="enrolled"
    )


class TestEnrollmentStoragePersistence:
    """Tests that operations actually change the file."""
    
    def test_add_changes_file(self, enrollment_storage, sample_enrollment):
        """Test that adding an enrollment changes the file content."""
        file_path = enrollment_storage.file_path
        
        # Initially empty
        with open(file_path, 'r') as f:
            initial_data = json.load(f)
        assert initial_data == [], f"Expected file to be initially empty, but found: {initial_data}"
        
        # Add enrollment
        enrollment_storage.add(sample_enrollment)
        
        # File should now contain the enrollment
        with open(file_path, 'r') as f:
            updated_data = json.load(f)
        assert len(updated_data) == 1, f"Expected file to contain 1 enrollment after adding, but found {len(updated_data)} enrollments"
        assert updated_data[0]["id"] == "enr_001", f"Expected enrollment ID to be 'enr_001', but found: {updated_data[0]['id']}"
        assert updated_data[0]["student_id"] == "s1001", f"Expected student ID to be 's1001', but found: {updated_data[0]['student_id']}"
        assert updated_data[0]["course_id"] == "CS101", f"Expected course ID to be 'CS101', but found: {updated_data[0]['course_id']}"
    
    def test_update_changes_file(self, enrollment_storage, sample_enrollment):
        """Test that updating an enrollment changes the file content."""
        file_path = enrollment_storage.file_path
        
        # Add initial enrollment
        enrollment_storage.add(sample_enrollment)
        
        # Update enrollment
        updated_enrollment = EnrollmentDTO(
            id="enr_001",
            student_id="s1001",
            course_id="CS101",
            status="completed",
            grade="A"
        )
        enrollment_storage.update(updated_enrollment)
        
        # File should reflect the update
        with open(file_path, 'r') as f:
            data = json.load(f)
        assert len(data) == 1, f"Expected file to contain 1 enrollment after update, but found {len(data)} enrollments"
        assert data[0]["status"] == "completed", f"Expected updated enrollment status to be 'completed', but found: {data[0]['status']}"
        assert data[0]["grade"] == "A", f"Expected updated enrollment grade to be 'A', but found: {data[0]['grade']}"
    
    def test_delete_changes_file(self, enrollment_storage, sample_enrollment):
        """Test that deleting an enrollment changes the file content."""
        file_path = enrollment_storage.file_path
        
        # Add enrollment
        enrollment_storage.add(sample_enrollment)
        
        # Verify enrollment exists in file
        with open(file_path, 'r') as f:
            data = json.load(f)
        assert len(data) == 1, f"Expected file to contain 1 enrollment before deletion, but found {len(data)} enrollments"
        
        # Delete enrollment
        enrollment_storage.delete("enr_001")
        
        # File should be empty
        with open(file_path, 'r') as f:
            data = json.load(f)
        assert data == [], f"Expected file to be empty after deletion, but found: {data}"


class TestEnrollmentStorageCorrectness:
    """Tests that methods return expected values and IDs are unique."""
    
    def test_add_returns_correct_value(self, enrollment_storage, sample_enrollment):
        """Test that add returns the added enrollment."""
        result = enrollment_storage.add(sample_enrollment)
        assert result == sample_enrollment, f"Expected add to return the added enrollment {sample_enrollment}, but got: {result}"
    
    def test_add_duplicate_raises_error(self, enrollment_storage, sample_enrollment):
        """Test that adding duplicate ID raises error."""
        enrollment_storage.add(sample_enrollment)
        
        with pytest.raises(ValueError, match="enr_001.*already exists"):
            enrollment_storage.add(sample_enrollment)
    
    def test_get_by_id_returns_correct_enrollment(self, enrollment_storage, sample_enrollment):
        """Test that get_by_id returns the correct enrollment."""
        enrollment_storage.add(sample_enrollment)
        
        result = enrollment_storage.get_by_id(sample_enrollment.id)
        assert result == sample_enrollment, f"Expected get_by_id to return {sample_enrollment}, but got: {result}"
    
    def test_get_by_id_nonexistent_returns_none(self, enrollment_storage):
        """Test that get_by_id returns None for nonexistent ID."""
        result = enrollment_storage.get_by_id("nonexistent")
        assert result is None, f"Expected get_by_id to return None for nonexistent ID, but got: {result}"
    
    def test_update_returns_correct_value(self, enrollment_storage, sample_enrollment):
        """Test that update returns the updated enrollment."""
        enrollment_storage.add(sample_enrollment)
        
        updated_enrollment = EnrollmentDTO(
            id="enr_001",
            student_id="s1001",
            course_id="CS101",
            status="completed",
            grade="A"
        )
        result = enrollment_storage.update(updated_enrollment)
        assert result == updated_enrollment, f"Expected update to return the updated enrollment {updated_enrollment}, but got: {result}"
    
    def test_update_nonexistent_raises_error(self, enrollment_storage):
        """Test that updating nonexistent enrollment raises error."""
        enrollment = EnrollmentDTO(
            id="enr_001",
            student_id="s1001",
            course_id="CS101",
            status="enrolled"
        )
        
        with pytest.raises(ValueError, match="enr_001.*not found"):
            enrollment_storage.update(enrollment)
    
    def test_delete_existing_returns_true(self, enrollment_storage, sample_enrollment):
        """Test that deleting existing enrollment returns True."""
        enrollment_storage.add(sample_enrollment)
        
        result = enrollment_storage.delete("enr_001")
        assert result is True, f"Expected delete to return True for existing enrollment, but got: {result}"
    
    def test_delete_nonexistent_returns_false(self, enrollment_storage):
        """Test that deleting nonexistent enrollment returns False."""
        result = enrollment_storage.delete("nonexistent")
        assert result is False, f"Expected delete to return False for nonexistent enrollment, but got: {result}"
    
    def test_get_by_student_id_returns_correct_enrollments(self, enrollment_storage):
        """Test that get_by_student_id returns correct enrollments."""
        enrollment1 = EnrollmentDTO(id="enr_001", student_id="s1001", course_id="CS101", status="enrolled")
        enrollment2 = EnrollmentDTO(id="enr_002", student_id="s1001", course_id="CS201", status="completed", grade="A")
        enrollment3 = EnrollmentDTO(id="enr_003", student_id="s1002", course_id="CS101", status="enrolled")
        
        enrollment_storage.add(enrollment1)
        enrollment_storage.add(enrollment2)
        enrollment_storage.add(enrollment3)
        
        result = enrollment_storage.get_by_student_id("s1001")
        assert len(result) == 2, f"Expected to find 2 enrollments for student s1001, but found: {len(result)}"
        assert enrollment1 in result, f"Expected enrollment1 {enrollment1} to be in results, but it was missing from: {result}"
        assert enrollment2 in result, f"Expected enrollment2 {enrollment2} to be in results, but it was missing from: {result}"
        assert enrollment3 not in result, f"Expected enrollment3 {enrollment3} NOT to be in results for student s1001, but it was found in: {result}"
    
    def test_get_by_course_id_returns_correct_enrollments(self, enrollment_storage):
        """Test that get_by_course_id returns correct enrollments."""
        enrollment1 = EnrollmentDTO(id="enr_001", student_id="s1001", course_id="CS101", status="enrolled")
        enrollment2 = EnrollmentDTO(id="enr_002", student_id="s1002", course_id="CS101", status="enrolled")
        enrollment3 = EnrollmentDTO(id="enr_003", student_id="s1001", course_id="CS201", status="completed", grade="B")
        
        enrollment_storage.add(enrollment1)
        enrollment_storage.add(enrollment2)
        enrollment_storage.add(enrollment3)
        
        result = enrollment_storage.get_by_course_id("CS101")
        assert len(result) == 2, f"Expected to find 2 enrollments for course CS101, but found: {len(result)}"
        assert enrollment1 in result, f"Expected enrollment1 {enrollment1} to be in results, but it was missing from: {result}"
        assert enrollment2 in result, f"Expected enrollment2 {enrollment2} to be in results, but it was missing from: {result}"
        assert enrollment3 not in result, f"Expected enrollment3 {enrollment3} NOT to be in results for course CS101, but it was found in: {result}" 