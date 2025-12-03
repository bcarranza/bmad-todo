"""CRUD operations for tasks"""

from typing import Optional
from sqlalchemy.orm import Session
from sqlalchemy import desc, asc

from app.models.task import Task
from app.schemas.task import TaskCreate, TaskUpdate


def create_task(db: Session, task: TaskCreate) -> Task:
    """Create a new task"""
    db_task = Task(
        title=task.title,
        description=task.description,
        due_date=task.due_date,
        completed=False
    )
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task


def get_task(db: Session, task_id: int) -> Optional[Task]:
    """Get a single task by ID"""
    return db.query(Task).filter(Task.id == task_id).first()


def get_tasks(
    db: Session,
    status: Optional[str] = None,
    order: Optional[str] = "newest",
    skip: int = 0,
    limit: int = 100
) -> list[Task]:
    """
    Get all tasks with optional filtering and ordering.
    
    Args:
        db: Database session
        status: Filter by status ('completed', 'pending', or None for all)
        order: Sort order ('newest', 'oldest', 'due_date')
        skip: Number of records to skip (for pagination)
        limit: Maximum number of records to return
    
    Returns:
        List of tasks
    """
    query = db.query(Task)
    
    # Apply status filter
    if status == "completed":
        query = query.filter(Task.completed == True)
    elif status == "pending":
        query = query.filter(Task.completed == False)
    
    # Apply ordering
    if order == "oldest":
        query = query.order_by(asc(Task.created_at))
    elif order == "due_date":
        # Tasks with due dates first (ascending), then tasks without due dates
        query = query.order_by(Task.due_date.asc().nulls_last(), desc(Task.created_at))
    else:  # newest (default)
        query = query.order_by(desc(Task.created_at))
    
    return query.offset(skip).limit(limit).all()


def update_task(db: Session, task_id: int, task_update: TaskUpdate) -> Optional[Task]:
    """Update an existing task"""
    db_task = get_task(db, task_id)
    if not db_task:
        return None
    
    # Update only provided fields
    update_data = task_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_task, field, value)
    
    db.commit()
    db.refresh(db_task)
    return db_task


def toggle_task_completion(db: Session, task_id: int) -> Optional[Task]:
    """Toggle task completion status"""
    db_task = get_task(db, task_id)
    if not db_task:
        return None
    
    db_task.completed = not db_task.completed
    db.commit()
    db.refresh(db_task)
    return db_task


def delete_task(db: Session, task_id: int) -> bool:
    """
    Delete a task.
    
    Returns:
        True if task was deleted, False if task not found
    """
    db_task = get_task(db, task_id)
    if not db_task:
        return False
    
    db.delete(db_task)
    db.commit()
    return True


def count_tasks(db: Session, status: Optional[str] = None) -> int:
    """Count tasks with optional status filter"""
    query = db.query(Task)
    
    if status == "completed":
        query = query.filter(Task.completed == True)
    elif status == "pending":
        query = query.filter(Task.completed == False)
    
    return query.count()

