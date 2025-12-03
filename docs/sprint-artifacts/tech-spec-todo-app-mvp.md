# Tech-Spec: TODO App MVP

**Created:** 2025-12-02  
**Status:** ✅ Completed  
**Author:** Barry (Quick Flow Solo Dev)  
**Completed:** 2025-12-02

## Overview

### Problem Statement

Build a simple but professionally structured TODO application to:
1. **Practice the full BMAD Method workflow** - from requirements gathering through deployment
2. **Create a portfolio piece** that demonstrates proper project structure, testing, and documentation for small-scale applications

This is a learning project that should be realistic enough to showcase real-world development practices (REST API, database design, testing strategy, deployment) while remaining simple enough to complete quickly.

### Solution

A single-user TODO management application with a **Python FastAPI backend** serving both REST API endpoints and a minimal HTML/JavaScript frontend. Tasks are stored in **SQLite** with the architecture designed for easy migration to PostgreSQL.

**Key Technical Approach:**
- REST API with standard CRUD operations
- SQLAlchemy ORM for database abstraction (enables easy DB migration)
- Pydantic schemas for request/response validation
- Simple server-rendered HTML with vanilla JavaScript for interactivity
- Pytest for comprehensive testing
- Alembic for database migrations

### Scope (In/Out)

**✅ In Scope (v1 - MVP):**
- Create task with title, optional description, optional due date
- Edit existing tasks
- Delete tasks
- Mark tasks as complete/incomplete
- List tasks with filters: all, completed only, pending only
- Basic ordering (newest first or by due date)
- REST API endpoints returning JSON
- Simple HTML/JS frontend served by FastAPI
- SQLite database
- Unit and integration tests
- Basic documentation (README, API docs via FastAPI)
- Local development setup

**❌ Out of Scope (Future versions):**
- User authentication/authorization
- Multi-user support
- Task categories/tags
- Task priorities
- Search functionality
- File attachments
- Notifications/reminders
- Mobile app
- Real-time collaboration
- Production deployment (covered in deployment doc, not code)

## Context for Development

### Codebase Patterns

Since this is a **greenfield project**, we'll establish these patterns:

**1. Project Structure:**
```
bmad-todo/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py              # FastAPI application entry point
│   │   ├── database.py          # Database connection and session management
│   │   ├── models/
│   │   │   ├── __init__.py
│   │   │   └── task.py          # SQLAlchemy Task model
│   │   ├── schemas/
│   │   │   ├── __init__.py
│   │   │   └── task.py          # Pydantic schemas for validation
│   │   ├── crud/
│   │   │   ├── __init__.py
│   │   │   └── task.py          # CRUD operations
│   │   └── routers/
│   │       ├── __init__.py
│   │       ├── tasks.py         # Task API endpoints
│   │       └── frontend.py      # Serve HTML frontend
│   ├── static/
│   │   ├── index.html           # Main UI
│   │   ├── style.css            # Minimal styling
│   │   └── app.js               # Frontend logic
│   ├── tests/
│   │   ├── __init__.py
│   │   ├── conftest.py          # Pytest fixtures
│   │   ├── test_tasks.py        # API endpoint tests
│   │   └── test_crud.py         # CRUD operation tests
│   ├── alembic/                 # Database migrations
│   ├── alembic.ini
│   ├── requirements.txt
│   └── requirements-dev.txt
├── docs/
│   ├── sprint-artifacts/
│   │   └── tech-spec-todo-app-mvp.md  # This file
│   ├── DEPLOYMENT.md            # Deployment guide
│   └── API.md                   # API documentation (auto-generated)
├── README.md
└── .gitignore
```

**2. Code Organization Patterns:**

**Models (SQLAlchemy):**
- One model per file in `app/models/`
- Use declarative base
- Include `created_at` and `updated_at` timestamps
- Use proper column types and constraints

**Schemas (Pydantic):**
- Request schemas: `TaskCreate`, `TaskUpdate`
- Response schemas: `Task`, `TaskList`
- Use Pydantic v2 features
- Enable ORM mode for easy SQLAlchemy integration

**CRUD Operations:**
- Separate CRUD logic from route handlers
- Accept `db: Session` as first parameter
- Return model instances or None
- Keep business logic here

**Routers:**
- RESTful endpoint design
- Proper HTTP status codes
- Dependency injection for database sessions
- Include response models

**3. Naming Conventions:**
- **Files:** snake_case (e.g., `task.py`)
- **Classes:** PascalCase (e.g., `TaskCreate`)
- **Functions:** snake_case (e.g., `create_task`)
- **Variables:** snake_case
- **Constants:** UPPER_SNAKE_CASE

**4. Database Design:**
- Use Alembic for all schema changes
- Never modify the database directly
- Migration naming: `YYYY_MM_DD_descriptive_name`

### Files to Reference

**No existing files** - this is greenfield. But here are the key files we'll create:

| File | Purpose |
|------|---------|
| `backend/app/main.py` | FastAPI app initialization, CORS, routes |
| `backend/app/database.py` | SQLAlchemy engine, session factory |
| `backend/app/models/task.py` | Task ORM model |
| `backend/app/schemas/task.py` | Pydantic validation schemas |
| `backend/app/crud/task.py` | CRUD operations for tasks |
| `backend/app/routers/tasks.py` | REST API endpoints |
| `backend/static/index.html` | Frontend UI |
| `backend/static/app.js` | Frontend JavaScript |
| `backend/tests/conftest.py` | Pytest fixtures (test DB) |
| `backend/requirements.txt` | Python dependencies |

### Technical Decisions

**1. Why FastAPI?**
- Modern, fast, async-capable
- Automatic API documentation (OpenAPI/Swagger)
- Great typing support with Pydantic
- Easy to learn, scales well

**2. Why SQLAlchemy ORM?**
- Database abstraction (SQLite → PostgreSQL is just connection string)
- Type-safe queries
- Industry standard for Python
- Works seamlessly with Alembic for migrations

**3. Why SQLite for v1?**
- Zero configuration
- Single file database
- Perfect for development and small deployments
- Easy migration path to PostgreSQL

**4. Why vanilla JS instead of React?**
- Keeps scope minimal for learning BMAD
- Faster initial development
- Less tooling complexity
- Can always add React later as separate enhancement

**5. Testing Strategy:**
- Pytest for all tests
- Use in-memory SQLite for tests (fast, isolated)
- Test fixtures for database setup/teardown
- Test both CRUD layer and API layer separately

## Implementation Plan

### Tasks

#### Phase 1: Project Setup
- [x] **Task 1.1:** Create project structure (directories, `__init__.py` files)
- [x] **Task 1.2:** Create `requirements.txt` with dependencies (fastapi, uvicorn, sqlalchemy, alembic, pytest, etc.)
- [x] **Task 1.3:** Create `.gitignore` for Python projects
- [x] **Task 1.4:** Create `README.md` with setup instructions

#### Phase 2: Database Layer
- [x] **Task 2.1:** Set up `database.py` with SQLAlchemy engine and session factory
- [x] **Task 2.2:** Create `models/task.py` with Task model (id, title, description, due_date, completed, created_at, updated_at)
- [x] **Task 2.3:** Initialize Alembic and create initial migration
- [x] **Task 2.4:** Create test database fixtures in `tests/conftest.py`

#### Phase 3: Business Logic
- [x] **Task 3.1:** Create Pydantic schemas in `schemas/task.py` (TaskCreate, TaskUpdate, Task, TaskList)
- [x] **Task 3.2:** Implement CRUD operations in `crud/task.py` (create, get, get_all, update, delete, filter by status)
- [x] **Task 3.3:** Write unit tests for CRUD operations

#### Phase 4: API Layer
- [x] **Task 4.1:** Create `main.py` with FastAPI app initialization
- [x] **Task 4.2:** Implement task router in `routers/tasks.py` with all REST endpoints
- [x] **Task 4.3:** Add database dependency injection
- [x] **Task 4.4:** Write integration tests for API endpoints
- [x] **Task 4.5:** Verify OpenAPI documentation is generated correctly

#### Phase 5: Frontend
- [x] **Task 5.1:** Create `static/index.html` with basic UI structure
- [x] **Task 5.2:** Create `static/style.css` with minimal styling
- [x] **Task 5.3:** Create `static/app.js` with API calls and DOM manipulation
- [x] **Task 5.4:** Add static file serving to `main.py`
- [x] **Task 5.5:** Test full flow in browser (create, edit, delete, filter, mark complete)

#### Phase 6: Polish
- [x] **Task 6.1:** Add error handling and validation messages in frontend
- [x] **Task 6.2:** Add loading states in UI
- [x] **Task 6.3:** Ensure all tests are passing
- [x] **Task 6.4:** Update README with API documentation and usage examples
- [x] **Task 6.5:** Create `DEPLOYMENT.md` with deployment instructions

### Acceptance Criteria

**API Functionality:**
- [ ] **AC 1:** Given a POST to `/api/tasks` with `{"title": "Test", "description": "Desc", "due_date": "2025-12-31"}`, when the request completes, then a 201 status is returned with the created task including an `id` and `created_at` timestamp
- [ ] **AC 2:** Given a GET to `/api/tasks`, when the request completes, then a 200 status is returned with a JSON array of all tasks
- [ ] **AC 3:** Given a GET to `/api/tasks?status=completed`, when the request completes, then only tasks with `completed=true` are returned
- [ ] **AC 4:** Given a GET to `/api/tasks?status=pending`, when the request completes, then only tasks with `completed=false` are returned
- [ ] **AC 5:** Given a GET to `/api/tasks/{id}` for an existing task, when the request completes, then a 200 status is returned with that task's details
- [ ] **AC 6:** Given a PUT to `/api/tasks/{id}` with updated fields, when the request completes, then a 200 status is returned with the updated task
- [ ] **AC 7:** Given a PATCH to `/api/tasks/{id}/complete`, when the request completes, then the task's `completed` field is set to `true`
- [ ] **AC 8:** Given a DELETE to `/api/tasks/{id}`, when the request completes, then a 204 status is returned and the task is removed from the database
- [ ] **AC 9:** Given a request for a non-existent task ID, when the request completes, then a 404 status is returned with an error message

**Frontend Functionality:**
- [ ] **AC 10:** Given the user opens the app, when the page loads, then all existing tasks are displayed in a list
- [ ] **AC 11:** Given the user fills the "New Task" form and clicks "Add", when the action completes, then the task appears in the list immediately
- [ ] **AC 12:** Given the user clicks "Edit" on a task, when the edit form appears and the user saves changes, then the task updates in the list
- [ ] **AC 13:** Given the user clicks "Delete" on a task, when the action completes, then the task is removed from the list
- [ ] **AC 14:** Given the user clicks the checkbox on a task, when the action completes, then the task's completed status toggles and the visual state updates
- [ ] **AC 15:** Given the user selects the "Completed" filter, when the filter is applied, then only completed tasks are shown
- [ ] **AC 16:** Given the user selects the "Pending" filter, when the filter is applied, then only pending tasks are shown
- [ ] **AC 17:** Given the user selects the "All" filter, when the filter is applied, then all tasks are shown

**Database & Testing:**
- [ ] **AC 18:** Given the database is SQLite, when the app is reconfigured to use PostgreSQL, then all functionality works without code changes (only connection string change)
- [ ] **AC 19:** Given the test suite is run with `pytest`, when all tests execute, then 100% of tests pass with no failures
- [ ] **AC 20:** Given the test suite includes CRUD tests, when they run, then they use an in-memory SQLite database and don't affect the main database

**Documentation:**
- [ ] **AC 21:** Given a new developer reads the README, when they follow the setup instructions, then they can run the app locally within 5 minutes
- [ ] **AC 22:** Given the FastAPI app is running, when a user visits `/docs`, then they see complete OpenAPI documentation for all endpoints

## Additional Context

### Dependencies

**Production Dependencies:**
```txt
fastapi==0.104.1
uvicorn[standard]==0.24.0
sqlalchemy==2.0.23
alembic==1.12.1
pydantic==2.5.0
python-dotenv==1.0.0
```

**Development Dependencies:**
```txt
pytest==7.4.3
pytest-asyncio==0.21.1
httpx==0.25.1  # For testing FastAPI
black==23.11.0
ruff==0.1.6
```

### Testing Strategy

**1. Unit Tests (CRUD Layer):**
- Test each CRUD function independently
- Use in-memory SQLite database
- Mock external dependencies if any
- Focus on business logic correctness

**2. Integration Tests (API Layer):**
- Use FastAPI's `TestClient`
- Test complete request/response cycle
- Verify status codes, response structure
- Test error cases (404, 422 validation errors)

**3. Test Fixtures:**
```python
# conftest.py pattern
@pytest.fixture
def test_db():
    """Create in-memory test database"""
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    SessionLocal = sessionmaker(bind=engine)
    yield SessionLocal()
    Base.metadata.drop_all(engine)
```

**4. Test Coverage Goal:** Aim for 80%+ coverage on business logic

### API Endpoints Design

**Base URL:** `http://localhost:8000`

| Method | Endpoint | Description | Request Body | Response |
|--------|----------|-------------|--------------|----------|
| GET | `/` | Serve frontend HTML | - | HTML page |
| GET | `/api/tasks` | List all tasks (with optional `?status=completed\|pending` filter) | - | `{"tasks": [...]}` |
| POST | `/api/tasks` | Create new task | `{"title": str, "description": str?, "due_date": date?}` | Task object (201) |
| GET | `/api/tasks/{id}` | Get single task | - | Task object (200) |
| PUT | `/api/tasks/{id}` | Update task | `{"title": str?, "description": str?, "due_date": date?}` | Task object (200) |
| PATCH | `/api/tasks/{id}/complete` | Toggle completion | - | Task object (200) |
| DELETE | `/api/tasks/{id}` | Delete task | - | No content (204) |

**Query Parameters:**
- `status`: Filter tasks by completion status (`completed`, `pending`)
- `order`: Order tasks (`newest`, `oldest`, `due_date`)

### Database Schema

**Table: `tasks`**

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | INTEGER | PRIMARY KEY, AUTOINCREMENT | Unique task identifier |
| title | VARCHAR(255) | NOT NULL | Task title |
| description | TEXT | NULLABLE | Optional task description |
| due_date | DATE | NULLABLE | Optional due date |
| completed | BOOLEAN | NOT NULL, DEFAULT FALSE | Completion status |
| created_at | TIMESTAMP | NOT NULL, DEFAULT NOW | Creation timestamp |
| updated_at | TIMESTAMP | NOT NULL, DEFAULT NOW | Last update timestamp |

**Indexes:**
- Primary key on `id` (automatic)
- Index on `completed` for filtering (optional, add if performance needed)

### Notes

**Future Enhancement Ideas (for later tech-specs):**
- Add React frontend as separate SPA
- Add user authentication with JWT
- Add task categories/tags
- Add PostgreSQL migration guide
- Add Docker deployment
- Add CI/CD pipeline
- Add task priorities
- Add recurring tasks
- Add task search

**Learning Opportunities:**
- REST API design principles
- FastAPI middleware and dependency injection
- SQLAlchemy relationships (if adding categories later)
- Database migrations with Alembic
- Testing strategies (unit vs integration)
- Frontend-backend communication
- Error handling and validation

**PostgreSQL Migration Notes:**
- Change `database.py` connection string from `sqlite:///./todo.db` to `postgresql://user:pass@host/dbname`
- Install `psycopg2-binary` dependency
- Update Alembic `alembic.ini` connection string
- Run migrations: `alembic upgrade head`
- No code changes required in models, CRUD, or routers!

---

**End of Tech-Spec**

