"""Simple storage system orchestrator."""

from pathlib import Path

from src.core.entities import Course, Staff, Student
from src.core.storage import CourseStorage, EnrollmentStorage, StaffStorage, StudentStorage


class StorageSystem:
    """Coordinates storage and assembles entities with relationships."""
    def __init__(self, data_dir: Path) -> None:
        """Initialize storage system with data directory."""
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self.student_storage = StudentStorage(self.data_dir / "students.json")
        self.staff_storage = StaffStorage(self.data_dir / "staff.json")
        self.course_storage = CourseStorage(self.data_dir / "courses.json")
        self.enrollment_storage = EnrollmentStorage(self.data_dir / "enrollments.json")
    
    
    def get_student(self, student_id: str) -> Student | None:
        """Retrieve a Student entity by user_id, including enrolled and completed courses."""
        
        student_data = self.student_storage.get_by_id(student_id)
        if student_data is None:
            return None
        user_id = student_data.user_id
        name = student_data.name
        enrolled_courses_ids = [
            e.course_id
            for e in self.enrollment_storage.get_by_student_id(student_id)
            if e.status == "enrolled"
        ]
        completed_courses = {
            e.course_id: e.grade
            for e in self.enrollment_storage.get_by_student_id(student_id)
            if e.status == "completed" and e.grade is not None
        }
        return Student(
            user_id=user_id,
            name=name,
            enrolled_courses_ids=enrolled_courses_ids,
            completed_courses=completed_courses
        )

    def get_staff(self, staff_id: str) -> Staff | None:
        """Retrieve a Staff entity by user_id, including name department and assigned course ids"""

        staff_data = self.staff_storage.get_by_id(staff_id)
        if staff_data is None:
            return None
        user_id = staff_data.user_id
        name = staff_data.name
        department = staff_data.department
        assigned_courses_ids = [
            course.id
            for course in self.course_storage.get_all()
            if course.instructor_id == staff_id
        ]
        return Staff(
            user_id=user_id,
            name=name,
            department=department,
            assigned_courses_ids=assigned_courses_ids
        )
    
    def get_course(self, course_id: str) -> Course | None:
        """Retrieve a Course entity by id, including instructor and enrolled students."""
        course_data = self.course_storage.get_by_id(course_id)
        if course_data is None:
            return None
        id = course_data.id
        name = course_data.name
        time_slot = course_data.time_slot
        capacity = course_data.capacity
        instructor_id = course_data.instructor_id

        enrolled_students_ids = [
            e.student_id
            for e in self.enrollment_storage.get_by_course_id(course_id)
            if e.status == "enrolled"
        ]

        return Course(
            id=id,
            name=name,
            time_slot=time_slot,
            capacity=capacity,
            instructor_id=instructor_id,
            enrolled_students_ids=enrolled_students_ids
        )
    
    def get_all_students(self) -> list[Student | None]:
        """Retrieve all Student entities."""
        students_data = self.student_storage.get_all()
        return [
            self.get_student(student.user_id)
            for student in students_data
            if self.get_student(student.user_id) is not None
        ]
    
    def get_all_staff(self) -> list[Staff | None]:
        """Retrieve all Staff entities."""
        staff_data = self.staff_storage.get_all()
        return [
            self.get_staff(staff.user_id)
            for staff in staff_data
            if self.get_staff(staff.user_id) is not None
        ]
    
    def get_all_courses(self) -> list[Course | None]:
        """Retrieve all Course entities."""
        courses_data = self.course_storage.get_all()
        return [
            self.get_course(course.id)
            for course in courses_data
            if self.get_course(course.id) is not None
        ]

        

