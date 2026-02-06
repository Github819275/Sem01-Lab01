"""Command-line interface for the University Course Management System."""

from pathlib import Path

from src.core import StorageSystem
from src.core.dto import CourseDTO, StaffDTO, StudentDTO, TimeSlotDTO
from src.services import CourseService, EnrollmentService, StaffService, StudentService


class CLI:
    """Provides command methods that are called from the Click CLI."""

    def __init__(self) -> None:
        """Initialize services and shared storage."""
        self.storage_system = StorageSystem(Path("data"))

        self.student_service = StudentService(self.storage_system)
        self.course_service = CourseService(self.storage_system)
        self.staff_service = StaffService(self.storage_system)
        self.enrollment_service = EnrollmentService(self.storage_system)

    # ----------------- STUDENT COMMANDS -----------------
    def add_student(self, user_id: str, name: str) -> None:
        """Add a new student."""
        student = StudentDTO(user_id=user_id, name=name)
        self.student_service.add_student(student)
        print(f"Added student {name} with id {user_id}")

    def get_student(self, user_id: str) -> None:
        """Retrieve a student by ID."""
        student = self.student_service.get_student(user_id)
        print(f"Student with ID {user_id} has name {student.name}")

    def student_exists(self, user_id: str) -> None:
        """Check if a student exists."""
        exists = self.student_service.student_exists(user_id)
        print(f"Student exists: {exists}")

    def remove_student(self, user_id: str) -> None:
        """Remove a student and associated enrollments."""
        self.student_service.remove_student(user_id)
        print(f"Removed student {user_id}")

    def get_all_students(self) -> None:
        """Print all students."""
        students = self.student_service.get_all_students()
        for student in students:
            if student is None:
                continue
            print(f"{student.user_id} - {student.name}")

    def get_transcript(self, user_id: str) -> None:
        """Print completed courses and grades."""
        transcript = self.student_service.get_transcript(user_id)
        if not transcript:
            print("No completed courses.")
        for course_id, grade in transcript.items():
            print(f"{course_id}: {grade}")

    # ----------------- COURSE COMMANDS -----------------
    def get_all_courses(self) -> None:
        """Print all courses."""
        courses = self.course_service.get_all_courses()
        for course in courses:
            if course is None:
                continue
            print(f"{course.id} - {course.name}")

    def add_course(
        self,
        course_id: str,
        name: str,
        start_time: str,
        weekday: int,
        duration: int,
        capacity: int = 30,
        instructor_id: str = ""
    ) -> None:
        """Add a new course."""
        course = CourseDTO(
            id=course_id,
            name=name,
            capacity=capacity,
            instructor_id=instructor_id,
            time_slot=TimeSlotDTO(weekday=weekday, start_time=start_time, duration=duration),
        )
        self.course_service.add_course(course)
        print(f"Added course {course_id}")

    def get_course(self, course_id: str) -> None:
        """Print course details."""
        course = self.course_service.get_course(course_id)
        if course is None:
            print(f"Course {course_id} not found")
            return
        print(f"{course.id} - {course.name}, Capacity: {course.capacity}, Instructor: {course.instructor_id}")

    def remove_course(self, course_id: str) -> None:
        """Remove a course and associated enrollments."""
        self.course_service.remove_course(course_id)
        print(f"Removed course {course_id}")

    # ----------------- STAFF COMMANDS -----------------
    def add_staff(self, staff_id: str, name: str, department: str) -> None:
        """Add a new staff member."""
        staff = StaffDTO(user_id=staff_id, name=name, department=department)
        self.staff_service.add_staff(staff)
        print(f"Added staff {name} with ID {staff_id} and department: {department}")

    def get_staff(self, staff_id: str) -> None:
        """Print staff details."""
        staff = self.staff_service.get_staff(staff_id)
        print(f"{staff.user_id} - {staff.name}")

    def staff_exists(self, staff_id: str) -> None:
        """Check if staff exists."""
        exists = self.staff_service.staff_exists(staff_id)
        print(f"Staff exists: {exists}")

    def remove_staff(self, staff_id: str) -> None:
        """Remove staff."""
        self.staff_service.remove_staff(staff_id)
        print(f"Removed staff {staff_id}")

    def get_all_staff(self) -> None:
        """Print all staff."""
        staff_list = self.staff_service.get_all_staff()
        for staff in staff_list:
            if staff is None:
                continue
            print(f"{staff.user_id} - {staff.name}")


    # ----------------- ENROLLMENT COMMANDS -----------------
    def enroll(self, student_id: str, course_id: str) -> None:
        """Enroll a student in a course."""
        self.enrollment_service.enroll_student_in_course(student_id, course_id)
        print(f"Enrolled {student_id} in {course_id}")

    def drop(self, student_id: str, course_id: str) -> None:
        """Drop a student from a course."""
        self.enrollment_service.drop_course(student_id, course_id)
        print(f"Dropped {student_id} from {course_id}")

    def complete_course(self, student_id: str, course_id: str, grade: str) -> None:
        """Record a final grade for a course."""
        self.enrollment_service.complete_course(student_id, course_id, grade)
        print(f"{student_id} completed {course_id} with grade {grade}")

    def get_student_enrollments(self, student_id: str) -> None:
        """Print all enrollments for a student."""
        enrollments = self.enrollment_service.get_student_enrollments(student_id)
        for e in enrollments:
            print(f"{e.course_id} - {e.status} - {e.grade}")

    def get_course_enrollments(self, course_id: str) -> None:
        """Print all enrollments for a course."""
        enrollments = self.enrollment_service.get_course_enrollments(course_id)
        for e in enrollments:
            print(f"{e.student_id} - {e.status} - {e.grade}")
