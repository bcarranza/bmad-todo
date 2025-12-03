# TODO App MVP

A simple but professionally structured TODO application built with FastAPI, SQLAlchemy, and vanilla JavaScript.

**Purpose:** Practice the full BMAD Method workflow and create a portfolio piece demonstrating proper project structure, testing, and documentation.

## Features

- ✅ Create tasks with title, description, and due date
- ✅ Edit and delete tasks
- ✅ Mark tasks as complete/incomplete
- ✅ Filter tasks (all, completed, pending)
- ✅ Order tasks (newest, oldest, by due date)
- ✅ REST API with automatic documentation
- ✅ Comprehensive test coverage

## Tech Stack

- **Backend:** Python 3.11+, FastAPI
- **Database:** SQLite (designed for easy PostgreSQL migration)
- **ORM:** SQLAlchemy 2.0
- **Migrations:** Alembic
- **Testing:** Pytest
- **Frontend:** HTML5, CSS3, Vanilla JavaScript

## Quick Start

### Prerequisites

- Python 3.11 or higher
- pip (Python package manager)

### Installation

1. **Clone the repository**
```bash
git clone <repository-url>
cd bmad-todo
```

2. **Create and activate virtual environment**
```bash
cd backend
python -m venv venv

# On macOS/Linux:
source venv/bin/activate

# On Windows:
venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Initialize database**
```bash
# Run migrations
alembic upgrade head
```

5. **Start the development server**
```bash
uvicorn app.main:app --reload
```

6. **Open your browser**
- Application: http://localhost:8000
- API Documentation: http://localhost:8000/docs
- Alternative API Docs: http://localhost:8000/redoc

## Development

### Running Tests

```bash
# Install dev dependencies
pip install -r requirements-dev.txt

# Run all tests
pytest

# Run with coverage
pytest --cov=app tests/

# Run specific test file
pytest tests/test_tasks.py
```

### Code Formatting

```bash
# Format code with Black
black app/ tests/

# Lint with Ruff
ruff check app/ tests/
```

### Database Migrations

```bash
# Create a new migration
alembic revision --autogenerate -m "description"

# Apply migrations
alembic upgrade head

# Rollback one migration
alembic downgrade -1
```

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Serve frontend HTML |
| GET | `/api/tasks` | List all tasks (supports `?status=` and `?order=` filters) |
| POST | `/api/tasks` | Create new task |
| GET | `/api/tasks/{id}` | Get single task |
| PUT | `/api/tasks/{id}` | Update task |
| PATCH | `/api/tasks/{id}/complete` | Toggle task completion |
| DELETE | `/api/tasks/{id}` | Delete task |

### Example API Usage

**Create a task:**
```bash
curl -X POST http://localhost:8000/api/tasks \
  -H "Content-Type: application/json" \
  -d '{"title": "Learn FastAPI", "description": "Complete tutorial", "due_date": "2025-12-31"}'
```

**List all tasks:**
```bash
curl http://localhost:8000/api/tasks
```

**Filter completed tasks:**
```bash
curl http://localhost:8000/api/tasks?status=completed
```

## Project Structure

```
bmad-todo/
├── backend/
│   ├── app/
│   │   ├── main.py              # FastAPI application
│   │   ├── database.py          # Database connection
│   │   ├── models/              # SQLAlchemy models
│   │   ├── schemas/             # Pydantic schemas
│   │   ├── crud/                # Database operations
│   │   └── routers/             # API endpoints
│   ├── static/                  # Frontend files
│   ├── tests/                   # Test suite
│   ├── alembic/                 # Database migrations
│   └── requirements.txt
├── docs/
│   └── sprint-artifacts/
│       └── tech-spec-todo-app-mvp.md
└── README.md
```

## Migrating to PostgreSQL

The application is designed for easy database migration:

1. Install PostgreSQL driver:
```bash
pip install psycopg2-binary
```

2. Update connection string in `app/database.py`:
```python
SQLALCHEMY_DATABASE_URL = "postgresql://user:password@localhost/dbname"
```

3. Run migrations:
```bash
alembic upgrade head
```

No code changes required! 🎉

## Contributing

This is a learning/portfolio project. Feel free to fork and experiment!

## License

MIT

## Documentation

- [Tech Spec](docs/sprint-artifacts/tech-spec-todo-app-mvp.md) - Complete technical specification
- [API Docs](http://localhost:8000/docs) - Interactive API documentation (when server is running)

---

**Built with the BMAD Method** - From requirements to deployment, following professional development practices.

