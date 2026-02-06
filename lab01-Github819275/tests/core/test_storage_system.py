"""
Tests for the Storage System.

Tests the main orchestrator that coordinates between different storage classes
and assembles complete entity objects with their relationships.
"""

import tempfile
import pytest
from pathlib import Path

from src.core.storage_system import StorageSystem
from src.core.dto import StudentDTO, StaffDTO, CourseDTO, TimeSlotDTO, EnrollmentDTO
from src.core.entities import Student, Staff, Course
from src.core.storage import StudentStorage, StaffStorage, CourseStorage, EnrollmentStorage


@pytest.fixture
def temp_dir():
    with tempfile.TemporaryDirectory() as temp_dir:
        yield Path(temp_dir)


@pytest.fixture
def storage_system(temp_dir):
    return StorageSystem(temp_dir)


@pytest.fixture
def populated_storage_system(temp_dir):
    system = StorageSystem(temp_dir)
    
    student1 = StudentDTO(user_id="s1001", name="Alice Smith")
    student2 = StudentDTO(user_id="s1002", name="Bob Johnson")
    system.student_storage.add(student1)
    system.student_storage.add(student2)
    
    staff1 = StaffDTO(user_id="p2001", name="Dr. Emily White", department="Computer Science")
    staff2 = StaffDTO(user_id="p2002", name="Dr. Michael Green", department="Mathematics")
    system.staff_storage.add(staff1)
    system.staff_storage.add(staff2)
    
    timeslot1 = TimeSlotDTO(weekday=1, start_time="09:00:00", duration=5400)
    timeslot2 = TimeSlotDTO(weekday=2, start_time="10:30:00", duration=3600)
    
    course1 = CourseDTO(id="CS101", name="Programming", time_slot=timeslot1, 
                       capacity=50, instructor_id="p2001")
    course2 = CourseDTO(id="MATH101", name="Calculus I", time_slot=timeslot2,
                       capacity=60, instructor_id="p2002")
    course3 = CourseDTO(id="CS201", name="Data Structures", capacity=40, 
                       instructor_id="p2001")
    
    system.course_storage.add(course1)
    system.course_storage.add(course2)
    system.course_storage.add(course3)
    
    enrollments = [
        EnrollmentDTO(id="enr_001", student_id="s1001", course_id="CS101", status="enrolled"),
        EnrollmentDTO(id="enr_002", student_id="s1001", course_id="MATH101", status="completed", grade="A"),
        EnrollmentDTO(id="enr_003", student_id="s1002", course_id="CS101", status="enrolled"),
        EnrollmentDTO(id="enr_004", student_id="s1002", course_id="CS201", status="completed", grade="B+"),
    ]
    
    for enrollment in enrollments:
        system.enrollment_storage.add(enrollment)
    
    return system


class TestStorageSystemInit:
    def test_creates_data_directory(self, temp_dir):
        system = StorageSystem(temp_dir)
        assert system.data_dir.exists(), f"Expected StorageSystem to create data directory, but {system.data_dir} does not exist"
    
    def test_creates_student_storage(self, storage_system):
        assert isinstance(storage_system.student_storage, StudentStorage), f"Expected student_storage to be a StudentStorage instance, but got: {type(storage_system.student_storage)}"
    
    def test_creates_staff_storage(self, storage_system):
        assert isinstance(storage_system.staff_storage, StaffStorage), f"Expected staff_storage to be a StaffStorage instance, but got: {type(storage_system.staff_storage)}"
    
    def test_creates_course_storage(self, storage_system):
        assert isinstance(storage_system.course_storage, CourseStorage), f"Expected course_storage to be a CourseStorage instance, but got: {type(storage_system.course_storage)}"
    
    def test_creates_enrollment_storage(self, storage_system):
        assert isinstance(storage_system.enrollment_storage, EnrollmentStorage), f"Expected enrollment_storage to be an EnrollmentStorage instance, but got: {type(storage_system.enrollment_storage)}"


class TestGetStudent:
    def test_returns_none_if_not_found(self, storage_system):
        result = storage_system.get_student("nonexistent")
        assert result is None, f"Expected get_student to return None for nonexistent student, but got: {result}"
    
    def test_returns_student_entity(self, populated_storage_system):
        student = populated_storage_system.get_student("s1001")
        assert isinstance(student, Student), f"Expected get_student to return a Student entity, but got: {type(student)}"
    
    def test_returns_correct_user_id(self, populated_storage_system):
        student = populated_storage_system.get_student("s1001")
        assert student.user_id == "s1001", f"Expected student user_id to be 's1001', but got: {student.user_id}"
    
    def test_returns_correct_name(self, populated_storage_system):
        student = populated_storage_system.get_student("s1001")
        assert student.name == "Alice Smith", f"Expected student name to be 'Alice Smith', but got: {student.name}"
    
    def test_includes_enrolled_courses(self, populated_storage_system):
        student = populated_storage_system.get_student("s1001")
        assert "CS101" in student.enrolled_courses_ids, f"Expected student to be enrolled in CS101, but enrolled_courses_ids was: {student.enrolled_courses_ids}"
    
    def test_includes_completed_courses(self, populated_storage_system):
        student = populated_storage_system.get_student("s1001")
        assert student.completed_courses["MATH101"] == "A", f"Expected student to have completed MATH101 with grade 'A', but completed_courses was: {student.completed_courses}"


class TestGetStaff:
    def test_returns_none_if_not_found(self, storage_system):
        result = storage_system.get_staff("nonexistent")
        assert result is None, f"Expected get_staff to return None for nonexistent staff, but got: {result}"
    
    def test_returns_staff_entity(self, populated_storage_system):
        staff = populated_storage_system.get_staff("p2001")
        assert isinstance(staff, Staff), f"Expected get_staff to return a Staff entity, but got: {type(staff)}"
    
    def test_returns_correct_user_id(self, populated_storage_system):
        staff = populated_storage_system.get_staff("p2001")
        assert staff.user_id == "p2001", f"Expected staff user_id to be 'p2001', but got: {staff.user_id}"
    
    def test_returns_correct_name(self, populated_storage_system):
        staff = populated_storage_system.get_staff("p2001")
        assert staff.name == "Dr. Emily White", f"Expected staff name to be 'Dr. Emily White', but got: {staff.name}"
    
    def test_includes_assigned_courses(self, populated_storage_system):
        staff = populated_storage_system.get_staff("p2001")
        assert "CS101" in staff.assigned_courses_ids, f"Expected staff to be assigned to CS101, but assigned_courses_ids was: {staff.assigned_courses_ids}"
    
    def test_includes_multiple_assigned_courses(self, populated_storage_system):
        staff = populated_storage_system.get_staff("p2001")
        assert "CS201" in staff.assigned_courses_ids, f"Expected staff to be assigned to CS201, but assigned_courses_ids was: {staff.assigned_courses_ids}"


class TestGetCourse:
    def test_returns_none_if_not_found(self, storage_system):
        result = storage_system.get_course("nonexistent")
        assert result is None, f"Expected get_course to return None for nonexistent course, but got: {result}"
    
    def test_returns_course_entity(self, populated_storage_system):
        course = populated_storage_system.get_course("CS101")
        assert isinstance(course, Course), f"Expected get_course to return a Course entity, but got: {type(course)}"
    
    def test_returns_correct_id(self, populated_storage_system):
        course = populated_storage_system.get_course("CS101")
        assert course.id == "CS101", f"Expected course id to be 'CS101', but got: {course.id}"
    
    def test_returns_correct_name(self, populated_storage_system):
        course = populated_storage_system.get_course("CS101")
        assert course.name == "Programming", f"Expected course name to be 'Programming', but got: {course.name}"
    
    def test_includes_instructor_id(self, populated_storage_system):
        course = populated_storage_system.get_course("CS101")
        assert course.instructor_id == "p2001", f"Expected course instructor_id to be 'p2001', but got: {course.instructor_id}"
    
    def test_includes_enrolled_students(self, populated_storage_system):
        course = populated_storage_system.get_course("CS101")
        assert "s1001" in course.enrolled_students_ids, f"Expected course to have student s1001 enrolled, but enrolled_students_ids was: {course.enrolled_students_ids}"
    
    def test_excludes_completed_students(self, populated_storage_system):
        course = populated_storage_system.get_course("MATH101")
        assert "s1001" not in course.enrolled_students_ids, f"Expected course NOT to include completed student s1001 in enrolled_students_ids, but enrolled_students_ids was: {course.enrolled_students_ids}"


class TestGetAllMethods:
    def test_get_all_students_empty(self, storage_system):
        students = storage_system.get_all_students()
        assert len(students) == 0, f"Expected get_all_students to return empty list when no students exist, but got {len(students)} students"
    
    def test_get_all_students_returns_two(self, populated_storage_system):
        students = populated_storage_system.get_all_students()
        assert len(students) == 2, f"Expected get_all_students to return 2 students, but got: {len(students)}"
    
    def test_get_all_staff_empty(self, storage_system):
        staff = storage_system.get_all_staff()
        assert len(staff) == 0, f"Expected get_all_staff to return empty list when no staff exist, but got {len(staff)} staff"
    
    def test_get_all_staff_returns_two(self, populated_storage_system):
        staff = populated_storage_system.get_all_staff()
        assert len(staff) == 2, f"Expected get_all_staff to return 2 staff members, but got: {len(staff)}"
    
    def test_get_all_courses_empty(self, storage_system):
        courses = storage_system.get_all_courses()
        assert len(courses) == 0, f"Expected get_all_courses to return empty list when no courses exist, but got {len(courses)} courses"
    
    def test_get_all_courses_returns_three(self, populated_storage_system):
        courses = populated_storage_system.get_all_courses()
        assert len(courses) == 3, f"Expected get_all_courses to return 3 courses, but got: {len(courses)}"


class TestRelationships:
    def test_student_enrolled_in_course(self, populated_storage_system):
        student = populated_storage_system.get_student("s1001")
        course = populated_storage_system.get_course("CS101")
        
        assert "CS101" in student.enrolled_courses_ids, f"Expected student s1001 to be enrolled in CS101, but enrolled_courses_ids was: {student.enrolled_courses_ids}"
        assert "s1001" in course.enrolled_students_ids, f"Expected course CS101 to have student s1001 enrolled, but enrolled_students_ids was: {course.enrolled_students_ids}"
    
    def test_staff_assigned_to_course(self, populated_storage_system):
        staff = populated_storage_system.get_staff("p2001")
        course = populated_storage_system.get_course("CS101")
        
        assert "CS101" in staff.assigned_courses_ids, f"Expected staff p2001 to be assigned to CS101, but assigned_courses_ids was: {staff.assigned_courses_ids}"
        assert course.instructor_id == "p2001", f"Expected course CS101 to have instructor_id 'p2001', but got: {course.instructor_id}" 