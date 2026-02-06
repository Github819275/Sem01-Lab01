"""
Tests for StudentStorage.

Tests persistence (operations change the file) and correctness (return values, uniqueness).
"""

import json
import tempfile
import pytest
from pathlib import Path

from src.core.storage import StudentStorage
from src.core.dto import StudentDTO


@pytest.fixture
def temp_dir():
    """Create a temporary directory for test files."""
    with tempfile.TemporaryDirectory() as temp_dir:
        yield Path(temp_dir)


@pytest.fixture
def student_storage(temp_dir):
    """Create a StudentStorage instance with temporary file."""
    return StudentStorage(temp_dir / "students.json")


@pytest.fixture
def sample_student():
    """Create a sample student DTO."""
    return StudentDTO(user_id="s1001", name="Alice Smith")


class TestStudentStoragePersistence:
    """Tests that operations actually change the file."""
    
    def test_add_changes_file(self, student_storage, sample_student):
        """Test that adding a student changes the file content."""
        file_path = student_storage.file_path
        
        # Initially empty
        with open(file_path, 'r') as f:
            initial_data = json.load(f)
        assert initial_data == [], f"Expected file to be initially empty, but found: {initial_data}"
        
        # Add student
        student_storage.add(sample_student)
        
        # File should now contain the student
        with open(file_path, 'r') as f:
            updated_data = json.load(f)
        assert len(updated_data) == 1, f"Expected file to contain 1 student after adding, but found {len(updated_data)} students"
        assert updated_data[0]["user_id"] == "s1001", f"Expected student user_id to be 's1001', but found: {updated_data[0]['user_id']}"
        assert updated_data[0]["name"] == "Alice Smith", f"Expected student name to be 'Alice Smith', but found: {updated_data[0]['name']}"
    
    def test_update_changes_file(self, student_storage, sample_student):
        """Test that updating a student changes the file content."""
        file_path = student_storage.file_path
        
        # Add initial student
        student_storage.add(sample_student)
        
        # Update student
        updated_student = StudentDTO(user_id="s1001", name="Alice Johnson")
        student_storage.update(updated_student)
        
        # File should reflect the update
        with open(file_path, 'r') as f:
            data = json.load(f)
        assert len(data) == 1, f"Expected file to contain 1 student after update, but found {len(data)} students"
        assert data[0]["name"] == "Alice Johnson", f"Expected updated student name to be 'Alice Johnson', but found: {data[0]['name']}"
    
    def test_delete_changes_file(self, student_storage, sample_student):
        """Test that deleting a student changes the file content."""
        file_path = student_storage.file_path
        
        # Add student
        student_storage.add(sample_student)
        
        # Verify student exists in file
        with open(file_path, 'r') as f:
            data = json.load(f)
        assert len(data) == 1, f"Expected file to contain 1 student before deletion, but found {len(data)} students"
        
        # Delete student
        student_storage.delete("s1001")
        
        # File should be empty
        with open(file_path, 'r') as f:
            data = json.load(f)
        assert data == [], f"Expected file to be empty after deletion, but found: {data}"


class TestStudentStorageCorrectness:
    """Tests that methods return expected values and IDs are unique."""
    
    def test_add_returns_correct_value(self, student_storage, sample_student):
        """Test that add returns the added student."""
        result = student_storage.add(sample_student)
        assert result == sample_student, f"Expected add to return the added student {sample_student}, but got: {result}"
    
    def test_add_duplicate_raises_error(self, student_storage, sample_student):
        """Test that adding duplicate ID raises error."""
        student_storage.add(sample_student)
        
        duplicate = StudentDTO(user_id="s1001", name="Different Name")
        with pytest.raises(ValueError, match="s1001.*already exists"):
            student_storage.add(duplicate)
    
    def test_get_by_id_returns_correct_student(self, student_storage, sample_student):
        """Test that get_by_id returns the correct student."""
        student_storage.add(sample_student)
        
        result = student_storage.get_by_id("s1001")
        assert result == sample_student, f"Expected get_by_id to return {sample_student}, but got: {result}"
    
    def test_get_by_id_nonexistent_returns_none(self, student_storage):
        """Test that get_by_id returns None for nonexistent ID."""
        result = student_storage.get_by_id("nonexistent")
        assert result is None, f"Expected get_by_id to return None for nonexistent ID, but got: {result}"
    
    def test_update_returns_correct_value(self, student_storage, sample_student):
        """Test that update returns the updated student."""
        student_storage.add(sample_student)
        
        updated_student = StudentDTO(user_id="s1001", name="Alice Johnson")
        result = student_storage.update(updated_student)
        assert result == updated_student, f"Expected update to return the updated student {updated_student}, but got: {result}"
    
    def test_update_nonexistent_raises_error(self, student_storage):
        """Test that updating nonexistent student raises error."""
        student = StudentDTO(user_id="s1001", name="Alice Smith")
        
        with pytest.raises(ValueError, match="s1001.*not found"):
            student_storage.update(student)
    
    def test_delete_existing_returns_true(self, student_storage, sample_student):
        """Test that deleting existing student returns True."""
        student_storage.add(sample_student)
        
        result = student_storage.delete("s1001")
        assert result is True, f"Expected delete to return True for existing student, but got: {result}"
    
    def test_delete_nonexistent_returns_false(self, student_storage):
        """Test that deleting nonexistent student returns False."""
        result = student_storage.delete("nonexistent")
        assert result is False, f"Expected delete to return False for nonexistent student, but got: {result}"
    