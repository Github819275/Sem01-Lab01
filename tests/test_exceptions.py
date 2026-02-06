"""
Tests for exception classes.

Tests the inheritance structure and basic functionality of all exception classes.
"""

import pytest

from src.exceptions import (
    EnrollmentError,
    ScheduleConflictError,
    CourseFullError,
    AlreadyEnrolledError,
    CourseNotFoundError
)


class TestEnrollmentError:
    """Tests for the base EnrollmentError class."""
    
    def test_enrollment_error_is_exception_subclass(self):
        """Test that EnrollmentError is a subclass of Exception."""
        assert issubclass(EnrollmentError, Exception), f"Expected EnrollmentError to be a subclass of Exception, but it is not"
    
    def test_enrollment_error_initialization(self):
        """Test that EnrollmentError can be initialized with a message."""
        error = EnrollmentError("Test error message")
        assert str(error) == "Test error message", f"Expected EnrollmentError message to be 'Test error message', but got: {str(error)}"
    
    def test_enrollment_error_can_be_raised(self):
        """Test that EnrollmentError can be raised and caught."""
        with pytest.raises(EnrollmentError) as exc_info:
            raise EnrollmentError("Test error")
        
        assert str(exc_info.value) == "Test error", f"Expected raised EnrollmentError message to be 'Test error', but got: {str(exc_info.value)}"


class TestScheduleConflictError:
    """Tests for ScheduleConflictError."""
    
    def test_schedule_conflict_error_is_enrollment_error_subclass(self):
        """Test that ScheduleConflictError is a subclass of EnrollmentError."""
        assert issubclass(ScheduleConflictError, EnrollmentError), f"Expected ScheduleConflictError to be a subclass of EnrollmentError, but it is not"
    
    def test_schedule_conflict_error_is_exception_subclass(self):
        """Test that ScheduleConflictError is a subclass of Exception."""
        assert issubclass(ScheduleConflictError, Exception), f"Expected ScheduleConflictError to be a subclass of Exception, but it is not"
    
    def test_schedule_conflict_error_initialization(self):
        """Test that ScheduleConflictError initializes correctly with course codes."""
        error = ScheduleConflictError("CS101", "CS102")
        
        assert error.course1_code == "CS101", f"Expected course1_code to be 'CS101', but got: {error.course1_code}"
        assert error.course2_code == "CS102", f"Expected course2_code to be 'CS102', but got: {error.course2_code}"
        assert str(error) == "Schedule conflict: course CS101 conflicts with course CS102", f"Expected error message to be 'Schedule conflict: course CS101 conflicts with course CS102', but got: {str(error)}"
    
    def test_schedule_conflict_error_can_be_raised(self):
        """Test that ScheduleConflictError can be raised and caught."""
        with pytest.raises(ScheduleConflictError) as exc_info:
            raise ScheduleConflictError("MATH101", "PHYS101")
        
        assert exc_info.value.course1_code == "MATH101", f"Expected course1_code to be 'MATH101', but got: {exc_info.value.course1_code}"
        assert exc_info.value.course2_code == "PHYS101", f"Expected course2_code to be 'PHYS101', but got: {exc_info.value.course2_code}"


class TestCourseFullError:
    """Tests for CourseFullError."""
    
    def test_course_full_error_is_enrollment_error_subclass(self):
        """Test that CourseFullError is a subclass of EnrollmentError."""
        assert issubclass(CourseFullError, EnrollmentError), f"Expected CourseFullError to be a subclass of EnrollmentError, but it is not"
    
    def test_course_full_error_is_exception_subclass(self):
        """Test that CourseFullError is a subclass of Exception."""
        assert issubclass(CourseFullError, Exception), f"Expected CourseFullError to be a subclass of Exception, but it is not"
    
    def test_course_full_error_initialization(self):
        """Test that CourseFullError initializes correctly with course code."""
        error = CourseFullError("CS101")
        
        assert error.course_code == "CS101", f"Expected course_code to be 'CS101', but got: {error.course_code}"
        assert str(error) == "Course CS101 is full and cannot accept more enrollments", f"Expected error message to be 'Course CS101 is full and cannot accept more enrollments', but got: {str(error)}"
    
    def test_course_full_error_can_be_raised(self):
        """Test that CourseFullError can be raised and caught."""
        with pytest.raises(CourseFullError) as exc_info:
            raise CourseFullError("MATH201")
        
        assert exc_info.value.course_code == "MATH201", f"Expected course_code to be 'MATH201', but got: {exc_info.value.course_code}"


class TestAlreadyEnrolledError:
    """Tests for AlreadyEnrolledError."""
    
    def test_already_enrolled_error_is_enrollment_error_subclass(self):
        """Test that AlreadyEnrolledError is a subclass of EnrollmentError."""
        assert issubclass(AlreadyEnrolledError, EnrollmentError), f"Expected AlreadyEnrolledError to be a subclass of EnrollmentError, but it is not"
    
    def test_already_enrolled_error_is_exception_subclass(self):
        """Test that AlreadyEnrolledError is a subclass of Exception."""
        assert issubclass(AlreadyEnrolledError, Exception), f"Expected AlreadyEnrolledError to be a subclass of Exception, but it is not"
    
    def test_already_enrolled_error_initialization(self):
        """Test that AlreadyEnrolledError initializes correctly with course code."""
        error = AlreadyEnrolledError("CS101")
        
        assert error.course_code == "CS101", f"Expected course_code to be 'CS101', but got: {error.course_code}"
        assert str(error) == "Student is already enrolled in course CS101", f"Expected error message to be 'Student is already enrolled in course CS101', but got: {str(error)}"
    
    def test_already_enrolled_error_can_be_raised(self):
        """Test that AlreadyEnrolledError can be raised and caught."""
        with pytest.raises(AlreadyEnrolledError) as exc_info:
            raise AlreadyEnrolledError("PHYS101")
        
        assert exc_info.value.course_code == "PHYS101", f"Expected course_code to be 'PHYS101', but got: {exc_info.value.course_code}"


class TestCourseNotFoundError:
    """Tests for CourseNotFoundError."""
    
    def test_course_not_found_error_is_enrollment_error_subclass(self):
        """Test that CourseNotFoundError is a subclass of EnrollmentError."""
        assert issubclass(CourseNotFoundError, EnrollmentError), f"Expected CourseNotFoundError to be a subclass of EnrollmentError, but it is not"
    
    def test_course_not_found_error_is_exception_subclass(self):
        """Test that CourseNotFoundError is a subclass of Exception."""
        assert issubclass(CourseNotFoundError, Exception), f"Expected CourseNotFoundError to be a subclass of Exception, but it is not"
    
    def test_course_not_found_error_initialization(self):
        """Test that CourseNotFoundError initializes correctly with course code."""
        error = CourseNotFoundError("CS999")
        
        assert error.course_code == "CS999", f"Expected course_code to be 'CS999', but got: {error.course_code}"
        assert str(error) == "Course CS999 not found", f"Expected error message to be 'Course CS999 not found', but got: {str(error)}"
    
    def test_course_not_found_error_can_be_raised(self):
        """Test that CourseNotFoundError can be raised and caught."""
        with pytest.raises(CourseNotFoundError) as exc_info:
            raise CourseNotFoundError("NONEXISTENT")
        
        assert exc_info.value.course_code == "NONEXISTENT", f"Expected course_code to be 'NONEXISTENT', but got: {exc_info.value.course_code}"


class TestExceptionHierarchy:
    """Tests for the overall exception hierarchy."""
    
    def test_all_enrollment_exceptions_inherit_from_enrollment_error(self):
        """Test that all specific enrollment exceptions inherit from EnrollmentError."""
        enrollment_exceptions = [
            ScheduleConflictError,
            CourseFullError,
            AlreadyEnrolledError,
            CourseNotFoundError
        ]
        
        for exception_class in enrollment_exceptions:
            assert issubclass(exception_class, EnrollmentError), f"Expected {exception_class.__name__} to be a subclass of EnrollmentError, but it is not"
    
    def test_all_exceptions_inherit_from_exception(self):
        """Test that all exception classes ultimately inherit from Exception."""
        all_exceptions = [
            EnrollmentError,
            ScheduleConflictError,
            CourseFullError,
            AlreadyEnrolledError,
            CourseNotFoundError
        ]
        
        for exception_class in all_exceptions:
            assert issubclass(exception_class, Exception), f"Expected {exception_class.__name__} to be a subclass of Exception, but it is not"
    
    def test_enrollment_error_can_catch_all_enrollment_exceptions(self):
        """Test that EnrollmentError can catch all specific enrollment exceptions."""
        exceptions_to_test = [
            ScheduleConflictError("CS101", "CS102"),
            CourseFullError("CS101"),
            AlreadyEnrolledError("CS101"),
            CourseNotFoundError("CS999")
        ]
        
        for exc in exceptions_to_test:
            with pytest.raises(EnrollmentError):
                raise exc 