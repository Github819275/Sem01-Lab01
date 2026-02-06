[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-22041afd0340ce965d47ae6ef1cefeee28c7c493a6346c4f15d667ab976d596c.svg)](https://classroom.github.com/a/DzcsczjU)
# University Course Management System

A lightweight Python application that demonstrates a **full‑stack, terminal‑based workflow** for managing university courses, students, and staff.  Everything—from data validation to business rules—is handled in‑memory and persisted to simple JSON, so you can explore the whole stack without a database.

---

## ✨ Key Capabilities

| Area                  | Highlights                                                                                                                                         |
| --------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------- |
| **User Management**   | • Add / remove students and staff <br>• Persist user metadata (department, office, etc.)                                                           |
| **Course Management** | • Create, list, or delete courses <br>• Time‑slot helper that prevents overlapping schedules <br>• Capacity control & automatic enrolment counters |
| **Enrolment Rules**   | • Prerequisite validation <br>• Schedule‑conflict detection <br>• Capacity checks & graceful errors                                                |
| **Student Tools**     | • View & manage current timetable <br>• Self‑service enrol / drop <br>• Auto‑generated transcript of completed courses                             |
| **Staff Tools**       | • View all users & courses in one place <br>• One‑prompt course creation wizard                                                                    |
| **Persistence**       | • All data serialised to `data/data.json` <br>• One‑line helper to (re)load sample data                                                            |

---

## 📂 Project Layout

```
.
├── data/
│   ├── sample_data.json   # seeded at first run
│   └── data.json          # live data after the first save
├── src/
│   ├── cli/               # Click‑powered command‑line UI
│   ├── exceptions/        # Domain‑specific errors
│   ├── models/            # Pydantic entities (Course, User, …)
│   ├── persistence/       # JSON (de)serialisation helpers
│   ├── services/          # Business logic (enrolment, courses, users)
│   └── storage/           # In‑memory singletons backing the services
├── run.py                 # entry‑point wrapper
└── README.md
```

### How the pieces fit together

1. **Models** validate all incoming data (Pydantic).
2. **Storage** singletons keep an in‑memory “source of truth”.
3. **Services** implement business rules and call `persistence.save_data()`.
4. **CLI** presents a friendly menu that orchestrates the services.

---

## 👥 Sample Accounts

| Role    | ID      | Name              |
| ------- | ------- | ----------------- |
| Student | `s1001` | Alice Smith       |
| Student | `s1002` | Bob Johnson       |
| Staff   | `p2001` | Dr. Emily White   |
| Staff   | `p2002` | Dr. Michael Green |

Use the IDs above at the **Login** prompt to explore the menus immediately.

---

## 🛠  Development Notes

* **Minimum Python:** 3.12.
* **Dependencies:** kept minimal—only `click` (CLI) and `pydantic` (validation).
* **Tests:** not included, but the codebase is designed for unit‑testing at the service layer.
* **Styling / Linting:** follow `black` (PEP 8 + formatting) & `ruff` (fast linter) if you add them.
