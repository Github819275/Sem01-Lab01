"""
Tests for CourseStorage.

Tests persistence (operations change the file) and correctness (return values, uniqueness).
"""

import json
import tempfile
import pytest
from pathlib import Path

from src.core.storage import CourseStorage
from src.core.dto import CourseDTO, TimeSlotDTO


@pytest.fixture
def temp_dir():
    """Create a temporary directory for test files."""
    with tempfile.TemporaryDirectory() as temp_dir:
        yield Path(temp_dir)


@pytest.fixture
def course_storage(temp_dir):
    """Create a CourseStorage instance with temporary file."""
    return CourseStorage(temp_dir / "courses.json")


@pytest.fixture
def sample_course():
    """Create a sample course DTO."""
    timeslot = TimeSlotDTO(weekday=1, start_time="09:00:00", duration=5400)
    return CourseDTO(
        id="CS101",
        name="Introduction to Programming",
        time_slot=timeslot,
        capacity=50,
        instructor_id="p001"
    )


class TestCourseStoragePersistence:
    """Tests that operations actually change the file."""
    
    def test_add_changes_file(self, course_storage, sample_course):
        """Test that adding a course changes the file content."""
        file_path = course_storage.file_path
        
        # Initially empty
        with open(file_path, 'r') as f:
            initial_data = json.load(f)
        assert initial_data == [], f"Expected file to be initially empty, but found: {initial_data}"
        
        # Add course
        course_storage.add(sample_course)
        
        # File should now contain the course
        with open(file_path, 'r') as f:
            updated_data = json.load(f)
        assert len(updated_data) == 1, f"Expected file to contain 1 course after adding, but found {len(updated_data)} courses"
        assert updated_data[0]["id"] == "CS101", f"Expected course ID to be 'CS101', but found: {updated_data[0]['id']}"
        assert updated_data[0]["name"] == "Introduction to Programming", f"Expected course name to be 'Introduction to Programming', but found: {updated_data[0]['name']}"
    
    def test_update_changes_file(self, course_storage, sample_course):
        """Test that updating a course changes the file content."""
        file_path = course_storage.file_path
        
        # Add initial course
        course_storage.add(sample_course)
        
        # Update course
        updated_course = CourseDTO(
            id="CS101",
            name="Advanced Programming",
            capacity=30,
            instructor_id="p002"
        )
        course_storage.update(updated_course)
        
        # File should reflect the update
        with open(file_path, 'r') as f:
            data = json.load(f)
        assert len(data) == 1, f"Expected file to contain 1 course after update, but found {len(data)} courses"
        assert data[0]["name"] == "Advanced Programming", f"Expected updated course name to be 'Advanced Programming', but found: {data[0]['name']}"
        assert data[0]["capacity"] == 30, f"Expected updated course capacity to be 30, but found: {data[0]['capacity']}"
    
    def test_delete_changes_file(self, course_storage, sample_course):
        """Test that deleting a course changes the file content."""
        file_path = course_storage.file_path
        
        # Add course
        course_storage.add(sample_course)
        
        # Verify course exists in file
        with open(file_path, 'r') as f:
            data = json.load(f)
        assert len(data) == 1, f"Expected file to contain 1 course before deletion, but found {len(data)} courses"
        
        # Delete course
        course_storage.delete("CS101")
        
        # File should be empty
        with open(file_path, 'r') as f:
            data = json.load(f)
        assert data == [], f"Expected file to be empty after deletion, but found: {data}"


class TestCourseStorageCorrectness:
    """Tests that methods return expected values and IDs are unique."""
    
    def test_add_returns_correct_value(self, course_storage, sample_course):
        """Test that add returns the added course."""
        result = course_storage.add(sample_course)
        assert result == sample_course, f"Expected add to return the added course {sample_course}, but got: {result}"
    
    def test_add_duplicate_raises_error(self, course_storage, sample_course):
        """Test that adding duplicate ID raises error."""
        course_storage.add(sample_course)
        
        duplicate = CourseDTO(
            id="CS101",
            name="Different Course",
            capacity=25
        )
        with pytest.raises(ValueError, match="CS101.*already exists"):
            course_storage.add(duplicate)
    
    def test_get_by_id_returns_correct_course(self, course_storage, sample_course):
        """Test that get_by_id returns the correct course."""
        course_storage.add(sample_course)
        
        result = course_storage.get_by_id("CS101")
        assert result == sample_course, f"Expected get_by_id to return {sample_course}, but got: {result}"
    
    def test_get_by_id_nonexistent_returns_none(self, course_storage):
        """Test that get_by_id returns None for nonexistent ID."""
        result = course_storage.get_by_id("nonexistent")
        assert result is None, f"Expected get_by_id to return None for nonexistent ID, but got: {result}"
    
    def test_update_returns_correct_value(self, course_storage, sample_course):
        """Test that update returns the updated course."""
        course_storage.add(sample_course)
        
        updated_course = CourseDTO(
            id="CS101",
            name="Advanced Programming",
            capacity=30,
            instructor_id="p002"
        )
        result = course_storage.update(updated_course)
        assert result == updated_course, f"Expected update to return the updated course {updated_course}, but got: {result}"
    
    def test_update_nonexistent_raises_error(self, course_storage):
        """Test that updating nonexistent course raises error."""
        course = CourseDTO(
            id="CS101",
            name="Introduction to Programming",
            capacity=50
        )
        
        with pytest.raises(ValueError, match="CS101.*not found"):
            course_storage.update(course)
    
    def test_delete_existing_returns_true(self, course_storage, sample_course):
        """Test that deleting existing course returns True."""
        course_storage.add(sample_course)
        
        result = course_storage.delete("CS101")
        assert result is True, f"Expected delete to return True for existing course, but got: {result}"
    
    def test_delete_nonexistent_returns_false(self, course_storage):
        """Test that deleting nonexistent course returns False."""
        result = course_storage.delete("nonexistent")
        assert result is False, f"Expected delete to return False for nonexistent course, but got: {result}"
    