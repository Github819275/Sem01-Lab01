"""
Tests for Data Transfer Objects (DTOs).

Tests the basic functionality of all DTO classes including BaseModel inheritance
and basic initialization.
"""

import pytest
from pydantic import BaseModel

from src.core.dto import StudentDTO, StaffDTO, CourseDTO, TimeSlotDTO, EnrollmentDTO


class TestStudentDTO:
    """Tests for StudentDTO."""
    
    def test_student_dto_is_basemodel_subclass(self):
        """Test that StudentDTO is a subclass of BaseModel."""
        assert issubclass(StudentDTO, BaseModel), f"Expected StudentDTO to be a subclass of BaseModel, but it is not"
    
    def test_student_dto_initialization(self):
        """Test that StudentDTO initialization works as expected."""
        student = StudentDTO(
            user_id="s1001",
            name="Alice Smith"
        )
        assert student.user_id == "s1001", f"Expected StudentDTO user_id to be 's1001', but got: {student.user_id}"
        assert student.name == "Alice Smith", f"Expected StudentDTO name to be 'Alice Smith', but got: {student.name}"


class TestStaffDTO:
    """Tests for StaffDTO."""
    
    def test_staff_dto_is_basemodel_subclass(self):
        """Test that StaffDTO is a subclass of BaseModel."""
        assert issubclass(StaffDTO, BaseModel), f"Expected StaffDTO to be a subclass of BaseModel, but it is not"
    
    def test_staff_dto_initialization(self):
        """Test that StaffDTO initialization works as expected."""
        staff = StaffDTO(
            user_id="p2001",
            name="Dr. Emily White",
            department="Computer Science"
        )
        assert staff.user_id == "p2001", f"Expected StaffDTO user_id to be 'p2001', but got: {staff.user_id}"
        assert staff.name == "Dr. Emily White", f"Expected StaffDTO name to be 'Dr. Emily White', but got: {staff.name}"
        assert staff.department == "Computer Science", f"Expected StaffDTO department to be 'Computer Science', but got: {staff.department}"


class TestTimeSlotDTO:
    """Tests for TimeSlotDTO."""
    
    def test_timeslot_dto_is_basemodel_subclass(self):
        """Test that TimeSlotDTO is a subclass of BaseModel."""
        assert issubclass(TimeSlotDTO, BaseModel), f"Expected TimeSlotDTO to be a subclass of BaseModel, but it is not"
    
    def test_timeslot_dto_initialization(self):
        """Test that TimeSlotDTO initialization works as expected."""
        timeslot = TimeSlotDTO(
            weekday=1,  # Monday
            start_time="09:00:00",
            duration=5400  # 1.5 hours in seconds
        )
        assert timeslot.weekday == 1, f"Expected TimeSlotDTO weekday to be 1, but got: {timeslot.weekday}"
        assert timeslot.start_time == "09:00:00", f"Expected TimeSlotDTO start_time to be '09:00:00', but got: {timeslot.start_time}"
        assert timeslot.duration == 5400, f"Expected TimeSlotDTO duration to be 5400, but got: {timeslot.duration}"


class TestCourseDTO:
    """Tests for CourseDTO."""
    
    def test_course_dto_is_basemodel_subclass(self):
        """Test that CourseDTO is a subclass of BaseModel."""
        assert issubclass(CourseDTO, BaseModel), f"Expected CourseDTO to be a subclass of BaseModel, but it is not"
    
    def test_course_dto_initialization(self):
        """Test that CourseDTO initialization works as expected."""
        timeslot = TimeSlotDTO(weekday=1, start_time="09:00:00", duration=5400)
        course = CourseDTO(
            id="CS201",
            name="Data Structures", 
            time_slot=timeslot,
            capacity=40,
            instructor_id="p001"
        )
        assert course.id == "CS201", f"Expected CourseDTO id to be 'CS201', but got: {course.id}"
        assert course.name == "Data Structures", f"Expected CourseDTO name to be 'Data Structures', but got: {course.name}"
        assert course.time_slot == timeslot, f"Expected CourseDTO time_slot to be {timeslot}, but got: {course.time_slot}"
        assert course.capacity == 40, f"Expected CourseDTO capacity to be 40, but got: {course.capacity}"
        assert course.instructor_id == "p001", f"Expected CourseDTO instructor_id to be 'p001', but got: {course.instructor_id}"


class TestEnrollmentDTO:
    """Tests for EnrollmentDTO."""
    
    def test_enrollment_dto_is_basemodel_subclass(self):
        """Test that EnrollmentDTO is a subclass of BaseModel."""
        assert issubclass(EnrollmentDTO, BaseModel), f"Expected EnrollmentDTO to be a subclass of BaseModel, but it is not"
    
    def test_enrollment_dto_initialization(self):
        """Test that EnrollmentDTO initialization works as expected."""
        enrollment = EnrollmentDTO(
            id="enr_001",
            student_id="s1001",
            course_id="CS101",
            status="enrolled"
        )
        assert enrollment.id == "enr_001", f"Expected EnrollmentDTO id to be 'enr_001', but got: {enrollment.id}"
        assert enrollment.student_id == "s1001", f"Expected EnrollmentDTO student_id to be 's1001', but got: {enrollment.student_id}"
        assert enrollment.course_id == "CS101", f"Expected EnrollmentDTO course_id to be 'CS101', but got: {enrollment.course_id}"
        assert enrollment.status == "enrolled", f"Expected EnrollmentDTO status to be 'enrolled', but got: {enrollment.status}"
        assert enrollment.grade is None, f"Expected EnrollmentDTO grade to be None by default, but got: {enrollment.grade}" 