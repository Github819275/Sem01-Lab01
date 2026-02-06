"""
Command-line entry point for the University Course Management System.

How to run:
    python3 -m src.cli.main (ubuntu)

Usage pattern:
    python3 -m src.cli.main <group> <command> [arguments]
    python3 -m src.cli.main <group> - will give all the subgroup commands

Main groups:
    student      Manage students
    course       Manage courses
    staff        Manage staff
    enrollment   Manage course enrollments

Examples:
    python3 -m src.cli.main student add "S1001" "Alice Smith"
    python3 -m src.cli.main course get-all
    python3 -m src.cli.main enrollment add "S1001" "CSC108"

Use --help after any group or command for details:
    python3 -m src.cli.main --help
    python3 -m src.cli.main student --help
    python3 -m src.cli.main student add --help
"""

from typing import Optional

import click

from src.cli.cli_interface import CLI

# Instantiate CLI
cli: CLI = CLI()


@click.group()
def app() -> None:
    """****University Course Management System****"""
    pass


# ----- STUDENT COMMANDS -----
@app.group()
def student() -> None:
    """Commands related to students."""
    pass


@student.command("add")
@click.argument("student_id")
@click.argument("name")
def add_student(student_id: str, name: str) -> None:
    """Add a new student. Parameters are 1) student_id and 2) name."""
    cli.add_student(student_id, name)


@student.command("get-student")
@click.argument("student_id")
def get_student(student_id: str) -> None:
    """Get the name of a student whose ID is known."""
    cli.get_student(student_id)


@student.command("student-exists")
@click.argument("student_id")
def student_exists(student_id: str) -> None:
    """Check if a student exists before searching."""
    cli.student_exists(student_id)


@student.command("delete")
@click.argument("student_id")
def remove_student(student_id: str) -> None:
    """Remove a student and their enrollments."""
    cli.remove_student(student_id)


@student.command("get-all")
def get_all_students() -> None:
    """Get a list of all current students."""
    cli.get_all_students()


@student.command("get-transcript")
@click.argument("student_id")
def get_transcript(student_id: str) -> None:
    """Return a list of the courses and respective grades."""
    cli.get_transcript(student_id)


# ----- COURSE COMMANDS -----
@app.group()
def course() -> None:
    """Commands related to courses."""
    pass


@course.command("get-all")
def get_all_courses() -> None:
    """Get a list of all current courses."""
    cli.get_all_courses()


@course.command("add")
@click.argument("course_id")
@click.argument("name")
@click.option("--start-time", default="09:00", help="Start time (e.g., 09:00)")
@click.option("--weekday", default=1, type=int, help="Weekday number (0=Mon ... 6=Sun)")
@click.option("--duration", default=1, type=int, help="Duration in hours")
@click.option("--capacity", default=30, type=int, help="Max number of students")
@click.option("--instructor-id", default="", help="Instructor ID (optional)")
def add_course(
    course_id: str,
    name: str,
    start_time: str,
    weekday: int,
    duration: int,
    capacity: int,
    instructor_id: str
) -> None:
    """Add a new course."""
    cli.add_course(course_id, name, start_time, weekday, duration, capacity, instructor_id)


@course.command("get")
@click.argument("course_id")
def get_course(course_id: str) -> None:
    """Get details of a course."""
    cli.get_course(course_id)


@course.command("delete")
@click.argument("course_id")
def delete_course(course_id: str) -> None:
    """Delete a course and associated enrollments."""
    cli.remove_course(course_id)


# ----- STAFF COMMANDS -----
@app.group()
def staff() -> None:
    """Commands related to staff."""
    pass


@staff.command("add")
@click.argument("staff_id")
@click.argument("name")
@click.argument("department")
def add_staff(staff_id: str, name: str, department: str) -> None:
    """Add a new staff member."""
    cli.add_staff(staff_id, name, department)


@staff.command("get")
@click.argument("staff_id")
def get_staff(staff_id: str) -> None:
    """Get details of a staff member."""
    cli.get_staff(staff_id)


@staff.command("exists")
@click.argument("staff_id")
def staff_exists(staff_id: str) -> None:
    """Check if a staff member exists."""
    cli.staff_exists(staff_id)


@staff.command("delete")
@click.argument("staff_id")
def delete_staff(staff_id: str) -> None:
    """Remove a staff member."""
    cli.remove_staff(staff_id)


@staff.command("get-all")
def get_all_staff() -> None:
    """List all staff members."""
    cli.get_all_staff()


# ----- ENROLLMENT COMMANDS -----
@app.group()
def enrollment() -> None:
    """Commands related to student course enrollments."""
    pass


@enrollment.command("add")
@click.argument("student_id")
@click.argument("course_id")
def enroll_student(student_id: str, course_id: str) -> None:
    """Enroll a student in a course."""
    cli.enroll(student_id, course_id)


@enrollment.command("drop")
@click.argument("student_id")
@click.argument("course_id")
def drop_student(student_id: str, course_id: str) -> None:
    """Drop a student from a course."""
    cli.drop(student_id, course_id)


@enrollment.command("complete")
@click.argument("student_id")
@click.argument("course_id")
@click.argument("grade")
def complete_course(student_id: str, course_id: str, grade: str) -> None:
    """Mark a course as completed with a grade."""
    cli.complete_course(student_id, course_id, grade)


@enrollment.command("student")
@click.argument("student_id")
def get_enrollments_for_student(student_id: str) -> None:
    """View all enrollments for a student."""
    cli.get_student_enrollments(student_id)


@enrollment.command("course")
@click.argument("course_id")
def get_enrollments_for_course(course_id: str) -> None:
    """View all enrollments for a course."""
    cli.get_course_enrollments(course_id)


if __name__ == "__main__":
    app()
