"""Enrollment exception module for the University Course Management System."""


class EnrollmentError(Exception):
    """Base class for all enrollment-related errors."""
    pass


class ScheduleConflictError(EnrollmentError):
    """Raised when a student tries to enroll in a course that conflicts in time with another."""
    def __init__(self, course_id_1: str, course_id_2: str) -> None:
        """Initialize with the conflicting course IDs."""
        self.course1_code = course_id_1
        self.course2_code = course_id_2
        super().__init__(f"Schedule conflict: course {course_id_1} conflicts with course {course_id_2}")
            


class CourseFullError(EnrollmentError):
    """Raised when a student tries to enroll in a course that is already full."""
    def __init__(self, course_id: str) -> None:
        """Initialize with the full course ID."""
        self.course_code = course_id
        super().__init__(f"Course {course_id} is full and cannot accept more enrollments")


class AlreadyEnrolledError(EnrollmentError):
    """Raised when a student tries to enroll in a course they are already enrolled in."""
    def __init__(self, course_id: str) -> None:
        """Initialize with the course ID."""
        self.course_code = course_id
        super().__init__(f"Student is already enrolled in course {course_id}")


class CourseNotFoundError(EnrollmentError):
    """Raised when the specified course cannot be found."""
    def __init__(self, course_id: str) -> None:
        """Initialize with the missing course ID."""
        self.course_code = course_id
        super().__init__(f"Course {course_id} not found")
