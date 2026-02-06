"""Staff entity with read-only business logic."""



from pydantic import BaseModel, Field


class Staff(BaseModel):
    """Staff entity with assigned courses."""
    
    user_id: str
    name: str
    department: str
    assigned_courses_ids: list[str] = []

    def is_assigned_to(self, course_id: str) -> bool:
        """Return True if the staff member is assigned to the given course."""
        return course_id in self.assigned_courses_ids

    def get_course_load(self) -> int:
        """Return the number of courses this staff member is assigned to."""
        return len(self.assigned_courses_ids)