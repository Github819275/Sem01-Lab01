"""Student entity with read-only business logic."""


from ast import Dict

from pydantic import BaseModel, Field


class Student(BaseModel):
    """Student entity with course relationships and academic history."""
    
    user_id: str
    name: str
    enrolled_courses_ids: list[str] = []
    completed_courses: dict[str, str] = {}


    def is_enrolled_in(self, course_id: str) -> bool:
        """Return True if the student is currently enrolled in the given course."""
        return course_id in self.enrolled_courses_ids

    def has_completed(self, course_id: str) -> bool:
        """Return True if the student has completed the given course."""
        return course_id in self.completed_courses

    def get_grade(self, course_id: str) -> str | None:
        """Return the grade for a completed course, or None if not completed."""
        return self.completed_courses.get(course_id)

    def get_current_course_load(self) -> int:
        """Return the number of currently enrolled courses."""
        return len(self.enrolled_courses_ids)

    def view_transcript(self) -> dict[str, str]:
        """Return a copy of the student's completed courses and grades."""
        return self.completed_courses.copy()