"""
Tests for the read-only entities layer.

Tests all entity classes focusing on read-only business logic,
properties, and query methods without mutation operations.
Updated for ID-based relationships instead of full object references.
"""

import pytest
from src.core.entities import Student, Staff, Course
from src.core.dto.course_dto import TimeSlotDTO


class TestStudent:
    def test_creates_with_user_id(self):
        student = Student(user_id="s1001", name="Alice Smith")
        assert student.user_id == "s1001", f"Expected Student user_id to be 's1001', but got: {student.user_id}"
    
    def test_creates_with_name(self):
        student = Student(user_id="s1001", name="Alice Smith")
        assert student.name == "Alice Smith", f"Expected Student name to be 'Alice Smith', but got: {student.name}"
    
    def test_creates_with_empty_enrolled_courses(self):
        student = Student(user_id="s1001", name="Alice Smith")
        assert student.enrolled_courses_ids == [], f"Expected Student enrolled_courses_ids to be empty list, but got: {student.enrolled_courses_ids}"
    
    def test_creates_with_empty_completed_courses(self):
        student = Student(user_id="s1001", name="Alice Smith")
        assert student.completed_courses == {}, f"Expected Student completed_courses to be empty dict, but got: {student.completed_courses}"
    
    def test_is_enrolled_in_returns_true(self):
        student = Student(user_id="s1001", name="Alice", enrolled_courses_ids=["CS101"])
        assert student.is_enrolled_in("CS101"), f"Expected Student to be enrolled in CS101, but is_enrolled_in returned False"
    
    def test_is_enrolled_in_returns_false(self):
        student = Student(user_id="s1001", name="Alice", enrolled_courses_ids=["CS101"])
        assert not student.is_enrolled_in("CS999"), f"Expected Student NOT to be enrolled in CS999, but is_enrolled_in returned True"
    
    def test_has_completed_returns_true(self):
        student = Student(user_id="s1001", name="Alice", completed_courses={"CS100": "A"})
        assert student.has_completed("CS100"), f"Expected Student to have completed CS100, but has_completed returned False"
    
    def test_has_completed_returns_false(self):
        student = Student(user_id="s1001", name="Alice", completed_courses={"CS100": "A"})
        assert not student.has_completed("CS999"), f"Expected Student NOT to have completed CS999, but has_completed returned True"
    
    def test_get_grade_returns_grade(self):
        student = Student(user_id="s1001", name="Alice", completed_courses={"CS100": "A"})
        assert student.get_grade("CS100") == "A", f"Expected Student grade for CS100 to be 'A', but got: {student.get_grade('CS100')}"
    
    def test_get_grade_returns_none(self):
        student = Student(user_id="s1001", name="Alice")
        assert student.get_grade("CS999") is None, f"Expected Student grade for CS999 to be None, but got: {student.get_grade('CS999')}"
    
    def test_get_current_course_load_empty(self):
        student = Student(user_id="s1001", name="Alice")
        assert student.get_current_course_load() == 0, f"Expected Student current course load to be 0, but got: {student.get_current_course_load()}"
    
    def test_get_current_course_load_two_courses(self):
        student = Student(user_id="s1001", name="Alice", enrolled_courses_ids=["CS101", "CS201"])
        assert student.get_current_course_load() == 2, f"Expected Student current course load to be 2, but got: {student.get_current_course_load()}"

    def test_view_transcript_returns_copy_not_reference(self):
        """Test that view_transcript returns a copy, not the exact object."""
        completed_courses = {"CS100": "A", "CS101": "B+", "CS201": "A-"}
        student = Student(user_id="s1001", name="Alice", completed_courses=completed_courses)
        
        transcript = student.view_transcript()
        
        # Verify it returns the same content
        assert transcript == completed_courses, f"Expected transcript to equal completed_courses {completed_courses}, but got: {transcript}"
        
        # Verify it's not the same object (different memory address)
        assert id(transcript) != id(completed_courses), f"Expected transcript to be a copy (different object), but got same object reference"
        
    def test_view_transcript_empty_returns_empty_copy(self):
        """Test that view_transcript returns an empty copy when no completed courses."""
        student = Student(user_id="s1001", name="Alice")
        
        transcript = student.view_transcript()
        
        assert transcript == {}, f"Expected empty transcript to be empty dict, but got: {transcript}"
        assert transcript is not student.completed_courses, f"Expected transcript to be a copy, not reference to student.completed_courses"


class TestStaff:
    def test_creates_with_user_id(self):
        staff = Staff(user_id="p2001", name="Dr. White", department="CS")
        assert staff.user_id == "p2001", f"Expected Staff user_id to be 'p2001', but got: {staff.user_id}"
    
    def test_creates_with_name(self):
        staff = Staff(user_id="p2001", name="Dr. White", department="CS")
        assert staff.name == "Dr. White", f"Expected Staff name to be 'Dr. White', but got: {staff.name}"
    
    def test_creates_with_department(self):
        staff = Staff(user_id="p2001", name="Dr. White", department="CS")
        assert staff.department == "CS", f"Expected Staff department to be 'CS', but got: {staff.department}"
    
    def test_creates_with_empty_assigned_courses(self):
        staff = Staff(user_id="p2001", name="Dr. White", department="CS")
        assert staff.assigned_courses_ids == [], f"Expected Staff assigned_courses_ids to be empty list, but got: {staff.assigned_courses_ids}"
    
    def test_is_assigned_to_returns_true(self):
        staff = Staff(user_id="p2001", name="Dr. White", department="CS", assigned_courses_ids=["CS101"])
        assert staff.is_assigned_to("CS101"), f"Expected Staff to be assigned to CS101, but is_assigned_to returned False"
    
    def test_is_assigned_to_returns_false(self):
        staff = Staff(user_id="p2001", name="Dr. White", department="CS", assigned_courses_ids=["CS101"])
        assert not staff.is_assigned_to("CS999"), f"Expected Staff NOT to be assigned to CS999, but is_assigned_to returned True"
    
    def test_get_course_load_empty(self):
        staff = Staff(user_id="p2001", name="Dr. White", department="CS")
        assert staff.get_course_load() == 0, f"Expected Staff course load to be 0, but got: {staff.get_course_load()}"
    
    def test_get_course_load_two_courses(self):
        staff = Staff(user_id="p2001", name="Dr. White", department="CS", assigned_courses_ids=["CS101", "CS201"])
        assert staff.get_course_load() == 2, f"Expected Staff course load to be 2, but got: {staff.get_course_load()}"


class TestCourse:
    def test_creates_with_id(self):
        course = Course(id="CS101", name="Programming")
        assert course.id == "CS101", f"Expected Course id to be 'CS101', but got: {course.id}"
    
    def test_creates_with_name(self):
        course = Course(id="CS101", name="Programming")
        assert course.name == "Programming", f"Expected Course name to be 'Programming', but got: {course.name}"
    
    def test_creates_with_default_capacity(self):
        course = Course(id="CS101", name="Programming")
        assert course.capacity == 30, f"Expected Course default capacity to be 30, but got: {course.capacity}"
    
    def test_creates_with_no_instructor(self):
        course = Course(id="CS101", name="Programming")
        assert course.instructor_id is None, f"Expected Course instructor_id to be None by default, but got: {course.instructor_id}"
    
    def test_creates_with_empty_enrolled_students(self):
        course = Course(id="CS101", name="Programming")
        assert course.enrolled_students_ids == [], f"Expected Course enrolled_students_ids to be empty list, but got: {course.enrolled_students_ids}"
    
    def test_current_enrollment_count_empty(self):
        course = Course(id="CS101", name="Programming")
        assert course.current_enrollment_count == 0, f"Expected Course current_enrollment_count to be 0, but got: {course.current_enrollment_count}"
    
    def test_current_enrollment_count_two(self):
        course = Course(id="CS101", name="Programming", enrolled_students_ids=["s1001", "s1002"])
        assert course.current_enrollment_count == 2, f"Expected Course current_enrollment_count to be 2, but got: {course.current_enrollment_count}"
    
    def test_is_full_false(self):
        course = Course(id="CS101", name="Programming", capacity=30, enrolled_students_ids=["s1001"])
        assert not course.is_full, f"Expected Course with 1/30 students NOT to be full, but is_full returned True"
    
    def test_is_full_true(self):
        course = Course(id="CS101", name="Programming", capacity=1, enrolled_students_ids=["s1001"])
        assert course.is_full, f"Expected Course with 1/1 students to be full, but is_full returned False"
    
    def test_is_student_enrolled_true(self):
        course = Course(id="CS101", name="Programming", enrolled_students_ids=["s1001"])
        assert course.is_student_enrolled("s1001"), f"Expected Course to have student s1001 enrolled, but is_student_enrolled returned False"
    
    def test_is_student_enrolled_false(self):
        course = Course(id="CS101", name="Programming", enrolled_students_ids=["s1001"])
        assert not course.is_student_enrolled("s9999"), f"Expected Course NOT to have student s9999 enrolled, but is_student_enrolled returned True"
    
    def test_time_conflict_same_time(self):
        timeslot = TimeSlotDTO(weekday=1, start_time="09:00:00", duration=5400)
        course1 = Course(id="CS101", name="Course 1", time_slot=timeslot)
        course2 = Course(id="CS102", name="Course 2", time_slot=timeslot)
        
        assert course1.has_time_conflict(course2), f"Expected courses with same time slot to have conflict, but has_time_conflict returned False"
    
    def test_no_time_conflict_different_days(self):
        timeslot1 = TimeSlotDTO(weekday=1, start_time="09:00:00", duration=5400)
        timeslot2 = TimeSlotDTO(weekday=2, start_time="09:00:00", duration=5400)
        course1 = Course(id="CS101", name="Course 1", time_slot=timeslot1)
        course2 = Course(id="CS102", name="Course 2", time_slot=timeslot2)
        
        assert not course1.has_time_conflict(course2), f"Expected courses on different days NOT to have conflict, but has_time_conflict returned True"

    def test_time_conflict_partial_overlap_start(self):
        """Test conflict when second course starts before first course ends."""
        # First course: 09:00-10:30 (90 minutes = 5400 seconds)
        timeslot1 = TimeSlotDTO(weekday=1, start_time="09:00:00", duration=5400)
        # Second course: 10:00-11:30 (starts 1 hour after first, overlaps for 30 minutes)
        timeslot2 = TimeSlotDTO(weekday=1, start_time="10:00:00", duration=5400)
        
        course1 = Course(id="CS101", name="Course 1", time_slot=timeslot1)
        course2 = Course(id="CS102", name="Course 2", time_slot=timeslot2)
        
        assert course1.has_time_conflict(course2), f"Expected courses with partial overlap (09:00-10:30 vs 10:00-11:30) to have conflict, but has_time_conflict returned False"
        assert course2.has_time_conflict(course1), f"Expected time conflict to be symmetric, but course2.has_time_conflict(course1) returned False"  # Should be symmetric

    def test_time_conflict_partial_overlap_end(self):
        """Test conflict when first course starts before second course ends."""
        # First course: 10:00-11:30
        timeslot1 = TimeSlotDTO(weekday=1, start_time="10:00:00", duration=5400)
        # Second course: 09:00-10:30 (ends 30 minutes after first starts)
        timeslot2 = TimeSlotDTO(weekday=1, start_time="09:00:00", duration=5400)
        
        course1 = Course(id="CS101", name="Course 1", time_slot=timeslot1)
        course2 = Course(id="CS102", name="Course 2", time_slot=timeslot2)
        
        assert course1.has_time_conflict(course2), f"Expected courses with partial overlap (10:00-11:30 vs 09:00-10:30) to have conflict, but has_time_conflict returned False"
        assert course2.has_time_conflict(course1), f"Expected time conflict to be symmetric, but course2.has_time_conflict(course1) returned False"  # Should be symmetric

    def test_no_time_conflict_adjacent_courses(self):
        """Test no conflict when courses are adjacent (end time = start time)."""
        # First course: 09:00-10:30
        timeslot1 = TimeSlotDTO(weekday=1, start_time="09:00:00", duration=5400)
        # Second course: 10:30-12:00 (starts exactly when first ends)
        timeslot2 = TimeSlotDTO(weekday=1, start_time="10:30:00", duration=5400)
        
        course1 = Course(id="CS101", name="Course 1", time_slot=timeslot1)
        course2 = Course(id="CS102", name="Course 2", time_slot=timeslot2)
        
        assert not course1.has_time_conflict(course2), f"Expected adjacent courses (09:00-10:30 then 10:30-12:00) NOT to have conflict, but has_time_conflict returned True"
        assert not course2.has_time_conflict(course1), f"Expected adjacent courses to have symmetric no-conflict, but course2.has_time_conflict(course1) returned True"  # Should be symmetric

    def test_time_conflict_one_course_contains_other(self):
        """Test conflict when one course time completely contains another."""
        # Long course: 09:00-12:00 (3 hours = 10800 seconds)
        timeslot1 = TimeSlotDTO(weekday=1, start_time="09:00:00", duration=10800)
        # Short course: 10:00-11:00 (1 hour = 3600 seconds) - completely inside
        timeslot2 = TimeSlotDTO(weekday=1, start_time="10:00:00", duration=3600)
        
        course1 = Course(id="CS101", name="Long Course", time_slot=timeslot1)
        course2 = Course(id="CS102", name="Short Course", time_slot=timeslot2)
        
        assert course1.has_time_conflict(course2), f"Expected long course (09:00-12:00) to conflict with contained short course (10:00-11:00), but has_time_conflict returned False"
        assert course2.has_time_conflict(course1), f"Expected time conflict to be symmetric when one course contains another, but course2.has_time_conflict(course1) returned False"  # Should be symmetric

    def test_no_time_conflict_when_one_has_no_timeslot(self):
        """Test no conflict when one course has no time slot."""
        timeslot = TimeSlotDTO(weekday=1, start_time="09:00:00", duration=5400)
        course1 = Course(id="CS101", name="Course 1", time_slot=timeslot)
        course2 = Course(id="CS102", name="Course 2", time_slot=None)
        
        assert not course1.has_time_conflict(course2), f"Expected course with timeslot NOT to conflict with course without timeslot, but has_time_conflict returned True"
        assert not course2.has_time_conflict(course1), f"Expected course without timeslot NOT to conflict with course with timeslot, but has_time_conflict returned True"

    def test_no_time_conflict_when_both_have_no_timeslot(self):
        """Test no conflict when both courses have no time slots."""
        course1 = Course(id="CS101", name="Course 1", time_slot=None)
        course2 = Course(id="CS102", name="Course 2", time_slot=None)
        
        assert not course1.has_time_conflict(course2), f"Expected courses without timeslots NOT to have conflict, but has_time_conflict returned True"
        assert not course2.has_time_conflict(course1), f"Expected courses without timeslots to have symmetric no-conflict, but course2.has_time_conflict(course1) returned True"
        