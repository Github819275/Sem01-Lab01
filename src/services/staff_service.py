"""Staff service module for the University Course Management System."""
from src.core import StorageSystem
from src.core.dto import StaffDTO
from src.core.entities import Staff


class StaffService:
    """Service class to handle staff management logic."""
    
    def __init__(self, storage_system: StorageSystem) -> None:
        """Initialize the StaffService with required dependencies."""
        self.storage_system = storage_system
    
    def get_all_staff(self) -> list[Staff | None]:
        """Retrieve all staff entities from storage."""
        return self.storage_system.get_all_staff()

    def add_staff(self, staff_dto: StaffDTO) -> Staff | None:
        """Add a new staff member to the storage system."""
        staff_storage = self.storage_system.staff_storage

        # Check if staff already exists
        if staff_storage.get_by_id(staff_dto.user_id) is not None:
            raise ValueError(f"Staff with ID {staff_dto.user_id} already exists")

        # Add the staff
        staff_storage.add(staff_dto)
        return self.storage_system.get_staff(staff_dto.user_id)

    def get_staff(self, staff_id: str) -> Staff:
        """Retrieve a staff member by their ID."""
        staff = self.storage_system.get_staff(staff_id)
        if staff is None:
            raise ValueError(f"Staff with ID {staff_id} not found")
        return staff

    def staff_exists(self, staff_id: str) -> bool:
        """Check whether a staff member exists in the system."""
        staff_storage = self.storage_system.staff_storage
        return staff_storage.get_by_id(staff_id) is not None

    def remove_staff(self, staff_id: str) -> None:
        """Remove a staff member by their ID."""
        staff_storage = self.storage_system.staff_storage
        if staff_storage.get_by_id(staff_id) is None:
            raise ValueError(f"Staff with ID {staff_id} not found")

        
        staff_storage.delete(staff_id)

    # def remove()