"""
Tests for StaffStorage.

Tests persistence (operations change the file) and correctness (return values, uniqueness).
"""

import json
import tempfile
import pytest
from pathlib import Path

from src.core.storage import StaffStorage
from src.core.dto import StaffDTO


@pytest.fixture
def temp_dir():
    """Create a temporary directory for test files."""
    with tempfile.TemporaryDirectory() as temp_dir:
        yield Path(temp_dir)


@pytest.fixture
def staff_storage(temp_dir):
    """Create a StaffStorage instance with temporary file."""
    return StaffStorage(temp_dir / "staff.json")


@pytest.fixture
def sample_staff():
    """Create a sample staff DTO."""
    return StaffDTO(
        user_id="p2001", 
        name="Dr. Emily White", 
        department="Computer Science"
    )


class TestStaffStoragePersistence:
    """Tests that operations actually change the file."""
    
    def test_add_changes_file(self, staff_storage, sample_staff):
        """Test that adding a staff member changes the file content."""
        file_path = staff_storage.file_path
        
        # Initially empty
        with open(file_path, 'r') as f:
            initial_data = json.load(f)
        assert initial_data == [], f"Expected file to be initially empty, but found: {initial_data}"
        
        # Add staff
        staff_storage.add(sample_staff)
        
        # File should now contain the staff member
        with open(file_path, 'r') as f:
            updated_data = json.load(f)
        assert len(updated_data) == 1, f"Expected file to contain 1 staff member after adding, but found {len(updated_data)} staff members"
        assert updated_data[0]["user_id"] == "p2001", f"Expected staff user_id to be 'p2001', but found: {updated_data[0]['user_id']}"
        assert updated_data[0]["name"] == "Dr. Emily White", f"Expected staff name to be 'Dr. Emily White', but found: {updated_data[0]['name']}"
    
    def test_update_changes_file(self, staff_storage, sample_staff):
        """Test that updating a staff member changes the file content."""
        file_path = staff_storage.file_path
        
        # Add initial staff
        staff_storage.add(sample_staff)
        
        # Update staff
        updated_staff = StaffDTO(
            user_id="p2001", 
            name="Dr. Emily Brown", 
            department="Mathematics"
        )
        staff_storage.update(updated_staff)
        
        # File should reflect the update
        with open(file_path, 'r') as f:
            data = json.load(f)
        assert len(data) == 1, f"Expected file to contain 1 staff member after update, but found {len(data)} staff members"
        assert data[0]["name"] == "Dr. Emily Brown", f"Expected updated staff name to be 'Dr. Emily Brown', but found: {data[0]['name']}"
        assert data[0]["department"] == "Mathematics", f"Expected updated staff department to be 'Mathematics', but found: {data[0]['department']}"
    
    def test_delete_changes_file(self, staff_storage, sample_staff):
        """Test that deleting a staff member changes the file content."""
        file_path = staff_storage.file_path
        
        # Add staff
        staff_storage.add(sample_staff)
        
        # Verify staff exists in file
        with open(file_path, 'r') as f:
            data = json.load(f)
        assert len(data) == 1, f"Expected file to contain 1 staff member before deletion, but found {len(data)} staff members"
        
        # Delete staff
        staff_storage.delete("p2001")
        
        # File should be empty
        with open(file_path, 'r') as f:
            data = json.load(f)
        assert data == [], f"Expected file to be empty after deletion, but found: {data}"


class TestStaffStorageCorrectness:
    """Tests that methods return expected values and IDs are unique."""
    
    def test_add_returns_correct_value(self, staff_storage, sample_staff):
        """Test that add returns the added staff member."""
        result = staff_storage.add(sample_staff)
        assert result == sample_staff, f"Expected add to return the added staff member {sample_staff}, but got: {result}"
    
    def test_add_duplicate_raises_error(self, staff_storage, sample_staff):
        """Test that adding duplicate ID raises error."""
        staff_storage.add(sample_staff)
        
        duplicate = StaffDTO(
            user_id="p2001", 
            name="Different Name", 
            department="Different Dept"
        )
        with pytest.raises(ValueError, match="p2001.*already exists"):
            staff_storage.add(duplicate)
    
    def test_get_by_id_returns_correct_staff(self, staff_storage, sample_staff):
        """Test that get_by_id returns the correct staff member."""
        staff_storage.add(sample_staff)
        
        result = staff_storage.get_by_id("p2001")
        assert result == sample_staff, f"Expected get_by_id to return {sample_staff}, but got: {result}"
    
    def test_get_by_id_nonexistent_returns_none(self, staff_storage):
        """Test that get_by_id returns None for nonexistent ID."""
        result = staff_storage.get_by_id("nonexistent")
        assert result is None, f"Expected get_by_id to return None for nonexistent ID, but got: {result}"
    
    def test_update_returns_correct_value(self, staff_storage, sample_staff):
        """Test that update returns the updated staff member."""
        staff_storage.add(sample_staff)
        
        updated_staff = StaffDTO(
            user_id="p2001", 
            name="Dr. Emily Brown", 
            department="Mathematics"
        )
        result = staff_storage.update(updated_staff)
        assert result == updated_staff, f"Expected update to return the updated staff member {updated_staff}, but got: {result}"
    
    def test_update_nonexistent_raises_error(self, staff_storage):
        """Test that updating nonexistent staff member raises error."""
        staff = StaffDTO(
            user_id="p2001", 
            name="Dr. Emily White", 
            department="Computer Science"
        )
        
        with pytest.raises(ValueError, match="p2001.*not found"):
            staff_storage.update(staff)
    
    def test_delete_existing_returns_true(self, staff_storage, sample_staff):
        """Test that deleting existing staff member returns True."""
        staff_storage.add(sample_staff)
        
        result = staff_storage.delete("p2001")
        assert result is True, f"Expected delete to return True for existing staff member, but got: {result}"
    
    def test_delete_nonexistent_returns_false(self, staff_storage):
        """Test that deleting nonexistent staff member returns False."""
        result = staff_storage.delete("nonexistent")
        assert result is False, f"Expected delete to return False for nonexistent staff member, but got: {result}"
    