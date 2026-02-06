# University Course Management System

---

## Project Overview

You will build a **terminal‑based University Course Management System** in **pure Python 3.12**.
The codebase deliberately grows in carefully‑scoped *milestones* so you can focus on one architectural layer at a time.
By the end you will have:

1. Fully‑typed **DTOs** validated by *Pydantic v2*
2. JSON‑backed **storage classes** that persist DTOs transparently
3. Rich **domain entities** and a **`StorageSystem`** that assembles relationships on‑demand
4. Stateless **services** and bespoke **exceptions** that capture business rules
5. *(Bonus)* A **Click**‑powered **CLI** with menus, colour, and interactive prompts


### Objective

This project aims on practicing the basic concepts of Python. \
You'll practice things from OOP and usage of Pydantic to working with JSON files and ensuring that the code is well-structured and easy to understand.

---

## Roadmap

| #               | Deliverable                                                                                                                                      |
| --------------- | ------------------------------------------------------------------------------------------------------------------------------------------------ |
| **1**           | **Data Transfer Objects (DTOs)** — `StudentDTO`, `StaffDTO`, `CourseDTO`, `TimeSlotDTO`, `EnrollmentDTO` (Pydantic models)                       |
| **2**           | **Storage Layer** — `BaseStorage` (abstract, already implemented for students), plus `{Student, Staff, Course, Enrollment}Storage` JSON backends |
| **3**           | **Domain Layer** — Rich entities (`Student`, `Staff`, `Course`) with behaviour; `StorageSystem` to assemble relationships                        |
| **4**           | **Services & Exceptions** — Service classes for each domain area; enrollment uses custom exception hierarchy                                     |
| **5** *(Bonus)* | **Command-Line Interface** — Any natural Click-based UX you like                                                                                 |

---

### 1. Data Transfer Objects (DTOs)

Use **Pydantic v2** ([link](https://docs.pydantic.dev/latest/)) for validation/typing.

* **StudentDTO**: `user_id: str`, `name: str`
* **StaffDTO**: `user_id: str`, `name: str`, `department: str`
* **TimeSlotDTO**: `weekday: int (1–7)`, `start_time: str ("HH:MM")`, `duration: int (minutes)`
* **CourseDTO**: `id: str`, `name: str`, `time_slot: TimeSlotDTO | None`, `capacity: int = 30`, `instructor_id: str | None`
* **EnrollmentDTO**: `id: str`, `student_id: str`, `course_id: str`, `status: str`, `grade: str | None`

Keep them logic‑free—just schemas.

---

### 2. Storage Layer

Reminder: Pydantic models give you `model_dump()` / `model_validate()` for easy **JSON→DTO / DTO→JSON**.

* **`BaseStorage[T]`**: handles file IO; already done for students (no edits needed). You extend it for others.
  Methods you provide in subclasses: `get_by_id`, `get_all`, `add`, (optionally `update`, `delete`).
* Implement one storage per DTO: `StudentStorage`, `StaffStorage`, `CourseStorage`, `EnrollmentStorage`.

**Important**: Try reduce code duplication as much as possible. Your initial implementation might include almost identical code for all derived storages.

---

### 3. Domain Layer (Entities & StorageSystem)

Entities mirror DTO fields but **add behaviour**:

* **Student**: `is_enrolled_in(course_id)`, `has_completed(course_id)`, `get_grade(course_id)`, `view_transcript()`, etc.
* **Staff**: `is_assigned_to(course_id)`, `get_course_load()`.
* **Course**: `is_full`, `current_enrollment_count`, `is_student_enrolled(student_id)`, `has_time_conflict(other_course)`.

**Time conflict examples** (same weekday & overlapping times → conflict):

```text
Course A: Mon 10:00, 90min   → covers 10:00–11:30
Course B: Mon 11:15, 60min   → overlap (11:15–11:30)  ⇒ conflict
Course C: Tue 10:00, 90min   → different weekday      ⇒ no conflict
Course D: Mon 11:30, 30min   → start == A end         ⇒ no conflict
```

**StorageSystem**: central orchestrator that

* pulls DTOs from storages,
* builds Entities with resolved relationships (e.g., course knows enrolled students’ IDs),
* exposes `get_student`, `get_course`, `get_staff`, and `get_all_*` helpers.

---

### 4. Services & Exceptions

Services are thin, stateless facades over `StorageSystem`, enforcing business rules:

* **StudentService / StaffService / CourseService**: CRUD + simple queries.
* **EnrollmentService**: enroll, drop, complete; must raise domain‑specific exceptions on errors.

Exception hierarchy (keep it simple):

```
EnrollmentError
├─ ScheduleConflictError
├─ CourseFullError
├─ AlreadyEnrolledError
└─ CourseNotFoundError
```

Use them inside `EnrollmentService`.

---

### 5. Command-Line Interface (Bonus)

Free‑form: build a **Click** menu or commands you find natural.
Leverage services; do not talk to storages directly.
Concise, user-friendly output is enough—no strict spec.

---

## General Requirements


| Area            | Requirement                                                                                                                                                                                                                               |
| --------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Typing**      | Run `pyrefly check src --search-path .` with **zero errors**. Use `# pyrefly: ignore[CODE]` *sparingly*|
| **Linting**     | `ruff check .` must exit **0**. The default profile in **pyproject.toml** is enforced.|
| **Tests**       | `pytest` must pass for the milestone you claim to complete.                                                                                                                                                                               |

**Important**: Launch the checkers above in `lab01_course_management` directory.


---

## Grading (base 100 pts + bonus 50 pts)

| Part                            |  Total  | Correctness |  Style |
| ------------------------------- | :-----: | :---------: | :----: |
| 1. Data Transfer Objects        |    15   |      10     |    5   |
| 2. Storage Layer                |    30   |      20     |   10   |
| 3. Domain Layer & StorageSystem |    30   |      15     |   15   |
| 4. Services & Exceptions        |    25   |      15     |   10   |
| **Subtotal**                    | **100** |    **60**   | **40** |
| 5. **CLI (Bonus)**              |  **50** |      25     |   25   |

*Bonus points are added on top of the 100‑point base.*

**Important:** Both tests and pyrefly/ruff checks have to pass. Otherwise, you get **zero points**.

---

## Hints & Best Practices

* **Model → Storage → Service**: implement in that order; later layers depend only on earlier ones.
* **DTO vs Entity**: DTOs are *pure data* (no logic). Entities extend DTOs by composition or inheritance and may include helper methods, calculated properties, etc.
* **Suppressing Pyrefly**: sometimes is acceptable since it's not always correct.
  * overload resolution (`# pyrefly: ignore[no-matching-overload]`)
  ```python
  class SomeClass(BaseModel):
    limited_number: int = Field(ge=1, le=7)  # pyrefly: ignore[no-matching-overload]
  ```
  Here is the problem either with the type checker or the pydantic library. The type checker can't find the overload for the `Field` class with the `ge` and `le` arguments.
  * bad return types (`# pyrefly: ignore[bad-return]`)
  ```python
  def read_something() -> str: # pyrefly: ignore[bad-return]
    while True:
      user_input = input("Enter something: ")
      if is_valid(user_input):
        return user_input
  ```
  Here pyrefly can't verify that we return a string, so we ignore the error.
  * Important: you should always add a comment to explain why you are ignoring the error.

---

## Flow

### Getting started

* Install [uv](https://docs.astral.sh/uv/)
* Run `uv sync`
* Run `uv run pytest` to run the tests.
  * Alternative: activate the virtual environment and run `pytest`
* You're ready to go!

### Before submission

1. Run `pytest` to ensure all tests pass.
  - Hint: you can run a specific test with `pytest <test_name>` (e.g. `tests/core/` or `"tests/core/test_dto.py::TestStudentDTO::test_student_dto_is_basemodel_subclass"`)
  - Hint: you can use `-vv` option to get more verbose output.
2. Run `pyrefly check src --search-path .` to ensure all types are correct.
3. Run `uv run ruff check .` to ensure all code is linted.
  - Hint: you can use `uv run ruff check --fix` to fix some of the linting errors.

**Important:** By default, commands like `pytest` and `pyrefly` will not work. You need to activate the virtual environment (`.venv`) or run them with `uv run` prefix (e.g. `uv run pytest tests/core/test_dto.py`).

#### Testing
**Important:** You have to uncomment the tests in the `pyproject.toml` file for parts you want to submit.

For example, if you have done part 1 and part 2, `pyproject.toml` should look like this:
```toml
[tool.pytest.ini_options]
testpaths = [
  # Part 1: DTOs
  "tests/core/test_dto.py",

  # Part 2: Storage Layer
  "tests/core/storage/*.py",

  # Part 3: Domain Layer
  # "tests/core/test_storage_system.py",
  # "tests/core/test_entities.py",

  # Part 4: Services & Exceptions (all tests should pass)
  # "tests"
]
```

**Super important:** Make sure you don't change any tests (`tests/`); if you do, you'll get 0 points.

### Submission

**Important:** The assignment consists of 2 stages. At first, you will turn in your initial solution. Then, you'll recieve feedback on correctness and style. At second stage, you can improve your solution (based on the feedback).

**How to submit:**
* Clone the repository (you'll have your own copy on github classroom)
* Make your changes / Check that all tests and pyrefly/ruff checks pass (see `Before submission` section)
  * Note: you shouldn't change any tests (`tests/`); if you do, you'll get 0 points.
* Commit / Push
  * Note: you don't need to worry about git branches
* Check that pipeline have passed successfully
* Wait for the feedback

Stage 2 is equivalent to re-submitting your solution.

---

## Deadlines

Check the main page / announcements group for the deadlines.

---

### Good luck & happy coding!

*Remember: small, well‑tested steps beat big untested jumps.*
