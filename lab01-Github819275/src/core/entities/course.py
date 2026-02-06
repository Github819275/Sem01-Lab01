

"""Course entity with read-only business logic."""


from datetime import datetime, timedelta

from pydantic import BaseModel, Field

from src.core.dto.course_dto import TimeSlotDTO


class Course(BaseModel):
    """Course entity with enrolled students and scheduling."""
    
    id: str
    name: str
    capacity: int = 30
    instructor_id: str | None = None
    enrolled_students_ids: list[str] = []
    time_slot: TimeSlotDTO | None = None

    @property
    def current_enrollment_count(self) -> int:
        """Return the current number of enrolled students."""
        return len(self.enrolled_students_ids)

    @property
    def is_full(self) -> bool:
        """Return True if the course is full (enrollment >= capacity)."""
        return self.current_enrollment_count >= self.capacity

    def is_student_enrolled(self, student_id: str) -> bool:
        """Return True if a given student is enrolled in this course."""
        return student_id in self.enrolled_students_ids

    def has_time_conflict(self, other_course: "Course") -> bool:
        """Return True if this course has a time conflict with another course."""
        if not self.time_slot or not other_course.time_slot:
            return False

        if self.time_slot.weekday != other_course.time_slot.weekday:
            return False

        fmt = "%H:%M:%S"
        start_a = datetime.strptime(self.time_slot.start_time, fmt)
        end_a = start_a + timedelta(seconds=self.time_slot.duration)

        start_b = datetime.strptime(other_course.time_slot.start_time, fmt)
        end_b = start_b + timedelta(seconds=other_course.time_slot.duration)

        return start_a < end_b and start_b < end_a