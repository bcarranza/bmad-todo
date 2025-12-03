# TODO App - Deployment Guide

This guide covers deploying the TODO App to various environments.

## Table of Contents

- [Prerequisites](#prerequisites)
- [Local Development](#local-development)
- [Database Setup](#database-setup)
- [Running Tests](#running-tests)
- [Production Deployment](#production-deployment)
- [Docker Deployment](#docker-deployment)
- [Environment Variables](#environment-variables)
- [Troubleshooting](#troubleshooting)

## Prerequisites

- Python 3.11 or higher
- pip (Python package manager)
- Git
- PostgreSQL (for production) or SQLite (for development)

## Local Development

### 1. Clone and Setup

```bash
# Clone repository
git clone <repository-url>
cd bmad-todo/backend

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

# Install dependencies
pip install -r requirements-dev.txt
```

### 2. Initialize Database

```bash
# Run migrations
alembic upgrade head
```

### 3. Start Development Server

```bash
# Start server with auto-reload
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

The application will be available at:
- Frontend: http://localhost:8000
- API Docs: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Database Setup

### SQLite (Development)

SQLite is used by default. The database file (`todo.db`) will be created automatically in the `backend` directory when you run migrations.

No additional setup required!

### PostgreSQL (Production)

1. **Install PostgreSQL**

```bash
# macOS (with Homebrew)
brew install postgresql
brew services start postgresql

# Ubuntu/Debian
sudo apt-get install postgresql postgresql-contrib
sudo systemctl start postgresql

# Create database
createdb todo_app
```

2. **Update Configuration**

Edit `backend/app/database.py`:

```python
SQLALCHEMY_DATABASE_URL = "postgresql://username:password@localhost/todo_app"
```

Or use environment variable (recommended):

```bash
export DATABASE_URL="postgresql://username:password@localhost/todo_app"
```

3. **Install PostgreSQL Driver**

```bash
pip install psycopg2-binary
```

4. **Update Alembic Configuration**

Edit `backend/alembic.ini`:

```ini
sqlalchemy.url = postgresql://username:password@localhost/todo_app
```

5. **Run Migrations**

```bash
alembic upgrade head
```

## Running Tests

```bash
# Install test dependencies
pip install -r requirements-dev.txt

# Run all tests
pytest

# Run with coverage
pytest --cov=app --cov-report=html tests/

# Run specific test file
pytest tests/test_tasks.py

# Run with verbose output
pytest -v
```

View coverage report by opening `htmlcov/index.html` in your browser.

## Production Deployment

### Option 1: Traditional Server (VPS/Cloud VM)

1. **Server Setup**

```bash
# Update system
sudo apt-get update
sudo apt-get upgrade -y

# Install Python and dependencies
sudo apt-get install -y python3.11 python3.11-venv python3-pip postgresql nginx

# Create app user
sudo useradd -m -s /bin/bash todoapp
sudo su - todoapp
```

2. **Application Setup**

```bash
# Clone repository
git clone <repository-url> /home/todoapp/app
cd /home/todoapp/app/backend

# Create virtual environment
python3.11 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
pip install gunicorn

# Set up database
alembic upgrade head
```

3. **Configure Systemd Service**

Create `/etc/systemd/system/todoapp.service`:

```ini
[Unit]
Description=TODO App FastAPI
After=network.target

[Service]
User=todoapp
Group=todoapp
WorkingDirectory=/home/todoapp/app/backend
Environment="PATH=/home/todoapp/app/backend/venv/bin"
ExecStart=/home/todoapp/app/backend/venv/bin/gunicorn -w 4 -k uvicorn.workers.UvicornWorker app.main:app --bind 0.0.0.0:8000

[Install]
WantedBy=multi-user.target
```

Start the service:

```bash
sudo systemctl daemon-reload
sudo systemctl start todoapp
sudo systemctl enable todoapp
sudo systemctl status todoapp
```

4. **Configure Nginx**

Create `/etc/nginx/sites-available/todoapp`:

```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

Enable and restart Nginx:

```bash
sudo ln -s /etc/nginx/sites-available/todoapp /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

5. **SSL with Let's Encrypt**

```bash
sudo apt-get install certbot python3-certbot-nginx
sudo certbot --nginx -d your-domain.com
```

### Option 2: Platform as a Service (PaaS)

#### Heroku

1. Create `Procfile`:

```
web: uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

2. Create `runtime.txt`:

```
python-3.11.6
```

3. Deploy:

```bash
heroku create your-app-name
heroku addons:create heroku-postgresql:mini
git push heroku main
heroku run alembic upgrade head
heroku open
```

#### Railway.app

1. Connect your GitHub repository
2. Add PostgreSQL database
3. Set environment variables
4. Railway will auto-deploy on push

#### Render.com

1. Create new Web Service
2. Connect repository
3. Build command: `pip install -r requirements.txt`
4. Start command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
5. Add PostgreSQL database
6. Deploy!

## Docker Deployment

### 1. Create Dockerfile

Create `backend/Dockerfile`:

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . .

# Run migrations and start server
CMD alembic upgrade head && uvicorn app.main:app --host 0.0.0.0 --port 8000
```

### 2. Create docker-compose.yml

Create `docker-compose.yml` in project root:

```yaml
version: '3.8'

services:
  db:
    image: postgres:15
    environment:
      POSTGRES_USER: todoapp
      POSTGRES_PASSWORD: changeme
      POSTGRES_DB: todoapp
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"

  web:
    build: ./backend
    command: sh -c "alembic upgrade head && uvicorn app.main:app --host 0.0.0.0 --port 8000"
    volumes:
      - ./backend:/app
    ports:
      - "8000:8000"
    depends_on:
      - db
    environment:
      DATABASE_URL: postgresql://todoapp:changeme@db:5432/todoapp

volumes:
  postgres_data:
```

### 3. Run with Docker

```bash
# Build and start
docker-compose up -d

# View logs
docker-compose logs -f

# Stop
docker-compose down
```

## Environment Variables

Create a `.env` file in the `backend` directory:

```env
# Database
DATABASE_URL=sqlite:///./todo.db
# Or for PostgreSQL:
# DATABASE_URL=postgresql://user:password@localhost/dbname

# Application
APP_ENV=production
DEBUG=False

# CORS (comma-separated origins)
ALLOWED_ORIGINS=https://yourdomain.com,https://www.yourdomain.com

# Security (optional)
SECRET_KEY=your-secret-key-here
```

Load environment variables in `app/database.py`:

```python
import os
from dotenv import load_dotenv

load_dotenv()

SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./todo.db")
```

## Troubleshooting

### Port Already in Use

```bash
# Find process using port 8000
lsof -i :8000

# Kill the process
kill -9 <PID>
```

### Database Connection Errors

```bash
# Check PostgreSQL status
sudo systemctl status postgresql

# Test connection
psql -U username -d dbname -h localhost

# Check connection string format
# PostgreSQL: postgresql://user:password@host:port/dbname
# SQLite: sqlite:///./database.db
```

### Migration Errors

```bash
# Check current migration version
alembic current

# View migration history
alembic history

# Rollback one migration
alembic downgrade -1

# Reset to specific revision
alembic downgrade <revision_id>

# Re-run migrations
alembic upgrade head
```

### Static Files Not Loading

Ensure `static` directory exists and contains files:

```bash
ls -la backend/static/
```

Check FastAPI static mount in `main.py`:

```python
app.mount("/static", StaticFiles(directory="static"), name="static")
```

### Permission Errors

```bash
# Fix file permissions
chmod -R 755 /path/to/app
chown -R todoapp:todoapp /path/to/app
```

## Performance Optimization

### 1. Use Production ASGI Server

Use Gunicorn with Uvicorn workers:

```bash
gunicorn -w 4 -k uvicorn.workers.UvicornWorker app.main:app --bind 0.0.0.0:8000
```

### 2. Database Connection Pooling

For PostgreSQL, use connection pooling:

```python
from sqlalchemy.pool import QueuePool

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    poolclass=QueuePool,
    pool_size=20,
    max_overflow=0
)
```

### 3. Enable Gzip Compression

Add to `main.py`:

```python
from fastapi.middleware.gzip import GZipMiddleware

app.add_middleware(GZipMiddleware, minimum_size=1000)
```

### 4. Cache Static Assets

Configure Nginx to cache static files:

```nginx
location /static/ {
    expires 1y;
    add_header Cache-Control "public, immutable";
}
```

## Monitoring

### Health Checks

```bash
# Check application health
curl http://localhost:8000/health
```

### Logs

```bash
# Systemd service logs
sudo journalctl -u todoapp -f

# Docker logs
docker-compose logs -f web

# Application logs (if configured)
tail -f /var/log/todoapp/app.log
```

## Backup and Recovery

### Backup SQLite Database

```bash
# Copy database file
cp todo.db todo.db.backup

# Or use SQLite backup command
sqlite3 todo.db ".backup 'todo.db.backup'"
```

### Backup PostgreSQL Database

```bash
# Dump database
pg_dump -U username dbname > backup.sql

# Restore database
psql -U username dbname < backup.sql
```

## Security Checklist

- [ ] Use environment variables for sensitive data
- [ ] Enable HTTPS (SSL/TLS certificates)
- [ ] Set strong PostgreSQL passwords
- [ ] Configure CORS with specific origins (not `*`)
- [ ] Keep dependencies updated
- [ ] Use firewall to restrict database access
- [ ] Regular security audits
- [ ] Monitor application logs
- [ ] Implement rate limiting (if needed)
- [ ] Regular backups

---

**Need Help?** Check the main [README.md](../README.md) or open an issue on GitHub.

