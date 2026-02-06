"""
Tests for StaffService using the new core storage system.

These tests focus on staff-specific functionality following the
single responsibility principle.
"""
import tempfile
import pytest
from pathlib import Path

from src.core import StorageSystem
from src.core.dto import StaffDTO
from src.core.entities import Staff
from src.services.staff_service import StaffService


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
def staff_service(storage_system):
    """Create a StaffService instance."""
    return StaffService(storage_system)


@pytest.fixture
def sample_staff_dto():
    """Create a sample StaffDTO."""
    return StaffDTO(user_id="staff456", name="Dr. Jane Smith", department="Computer Science")


class TestStaffService:
    """Test class for StaffService functionality."""
    
    def test_get_all_staff_empty(self, staff_service):
        """Test getting all staff when none exist."""
        staff = staff_service.get_all_staff()
        assert staff == []
    
    def test_add_staff_basic(self, staff_service, sample_staff_dto):
        """Test adding a basic staff member."""
        staff = staff_service.add_staff(sample_staff_dto)
        
        assert staff is not None
        assert isinstance(staff, Staff)
        assert staff.user_id == sample_staff_dto.user_id
        assert staff.name == sample_staff_dto.name
        assert staff.department == sample_staff_dto.department
        assert staff.assigned_courses_ids == []
    
    def test_add_staff_duplicate_raises_error(self, staff_service, sample_staff_dto):
        """Test that adding duplicate staff raises ValueError."""
        # Add staff first time
        staff_service.add_staff(sample_staff_dto)
        
        # Try to add again
        with pytest.raises(ValueError) as exc_info:
            staff_service.add_staff(sample_staff_dto)
        
        assert f"Staff with ID {sample_staff_dto.user_id} already exists" in str(exc_info.value)
    
    def test_get_staff_found(self, staff_service, sample_staff_dto):
        """Test retrieving an existing staff member."""
        added_staff = staff_service.add_staff(sample_staff_dto)
        
        retrieved_staff = staff_service.get_staff(sample_staff_dto.user_id)
        
        assert retrieved_staff is not None
        assert isinstance(retrieved_staff, Staff)
        assert retrieved_staff.user_id == added_staff.user_id
        assert retrieved_staff.name == added_staff.name
        assert retrieved_staff.department == added_staff.department
    
    def test_get_staff_not_found_raises_error(self, staff_service):
        """Test retrieving a non-existent staff member raises ValueError."""
        with pytest.raises(ValueError) as exc_info:
            staff_service.get_staff("nonexistent-id")
        
        assert "Staff with ID nonexistent-id not found" in str(exc_info.value)
    
    def test_get_all_staff_populated(self, staff_service):
        """Test getting all staff when multiple exist."""
        staff1_dto = StaffDTO(user_id="staff1", name="Staff One", department="CS")
        staff2_dto = StaffDTO(user_id="staff2", name="Staff Two", department="Math")
        
        staff1 = staff_service.add_staff(staff1_dto)
        staff2 = staff_service.add_staff(staff2_dto)
        
        staff = staff_service.get_all_staff()
        
        assert len(staff) == 2
        assert all(isinstance(s, Staff) for s in staff)
        staff_ids = {s.user_id for s in staff}
        assert staff_ids == {"staff1", "staff2"}
    
    def test_staff_exists_true(self, staff_service, sample_staff_dto):
        """Test staff existence check for existing staff."""
        staff_service.add_staff(sample_staff_dto)
        assert staff_service.staff_exists(sample_staff_dto.user_id) is True
    
    def test_staff_exists_false(self, staff_service):
        """Test staff existence check for non-existent staff."""
        assert staff_service.staff_exists("fake-id") is False
    
    def test_remove_staff_basic(self, staff_service, sample_staff_dto):
        """Test removing a staff member."""
        staff_service.add_staff(sample_staff_dto)
        staff_id = sample_staff_dto.user_id
        
        # Verify it exists
        assert staff_service.staff_exists(staff_id) is True
        
        # Remove it
        staff_service.remove_staff(staff_id)
        
        # Verify it's gone
        assert staff_service.staff_exists(staff_id) is False
        with pytest.raises(ValueError):
            staff_service.get_staff(staff_id)
    
    def test_remove_staff_not_found_raises_error(self, staff_service):
        """Test removing a non-existent staff member raises ValueError."""
        with pytest.raises(ValueError) as exc_info:
            staff_service.remove_staff("nonexistent-id")
        
        assert "Staff with ID nonexistent-id not found" in str(exc_info.value)
    
    def test_staff_service_persistence(self, temp_data_dir):
        """Test that staff persist across service instances."""
        staff_dto = StaffDTO(user_id="persistent_staff", name="Persistent Staff", department="CS")
        
        # Create first service instance and add staff
        storage1 = StorageSystem(temp_data_dir)
        service1 = StaffService(storage1)
        service1.add_staff(staff_dto)
        
        # Create second service instance with same data directory
        storage2 = StorageSystem(temp_data_dir)
        service2 = StaffService(storage2)
        
        # Verify staff persists
        staff = service2.get_staff("persistent_staff")
        
        assert staff is not None
        assert isinstance(staff, Staff)
        assert staff.name == "Persistent Staff"
        assert staff.department == "CS" 