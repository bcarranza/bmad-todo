"""Task API endpoints"""

from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.crud import task as crud_task
from app.schemas.task import Task, TaskCreate, TaskUpdate, TaskList

router = APIRouter()


@router.post("/tasks", response_model=Task, status_code=status.HTTP_201_CREATED)
def create_task(task: TaskCreate, db: Session = Depends(get_db)):
    """
    Create a new task.
    
    **Parameters:**
    - **title**: Task title (required, 1-255 characters)
    - **description**: Optional task description
    - **due_date**: Optional due date in YYYY-MM-DD format
    
    **Returns:**
    - Created task with ID, timestamps, and completion status
    """
    return crud_task.create_task(db=db, task=task)


@router.get("/tasks", response_model=TaskList)
def list_tasks(
    status: Optional[str] = Query(None, regex="^(completed|pending)$", description="Filter by status"),
    order: Optional[str] = Query("newest", regex="^(newest|oldest|due_date)$", description="Sort order"),
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Maximum records to return"),
    db: Session = Depends(get_db)
):
    """
    List all tasks with optional filtering and ordering.
    
    **Query Parameters:**
    - **status**: Filter by 'completed' or 'pending' (optional)
    - **order**: Sort by 'newest', 'oldest', or 'due_date' (default: newest)
    - **skip**: Pagination offset (default: 0)
    - **limit**: Maximum results (default: 100, max: 1000)
    
    **Returns:**
    - List of tasks and total count
    """
    tasks = crud_task.get_tasks(db=db, status=status, order=order, skip=skip, limit=limit)
    total = crud_task.count_tasks(db=db, status=status)
    return TaskList(tasks=tasks, total=total)


@router.get("/tasks/{task_id}", response_model=Task)
def get_task(task_id: int, db: Session = Depends(get_db)):
    """
    Get a specific task by ID.
    
    **Parameters:**
    - **task_id**: Task identifier
    
    **Returns:**
    - Task details
    
    **Raises:**
    - 404: Task not found
    """
    db_task = crud_task.get_task(db=db, task_id=task_id)
    if db_task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with id {task_id} not found"
        )
    return db_task


@router.put("/tasks/{task_id}", response_model=Task)
def update_task(task_id: int, task: TaskUpdate, db: Session = Depends(get_db)):
    """
    Update an existing task.
    
    **Parameters:**
    - **task_id**: Task identifier
    - **task**: Updated task data (all fields optional)
    
    **Returns:**
    - Updated task
    
    **Raises:**
    - 404: Task not found
    """
    db_task = crud_task.update_task(db=db, task_id=task_id, task_update=task)
    if db_task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with id {task_id} not found"
        )
    return db_task


@router.patch("/tasks/{task_id}/complete", response_model=Task)
def toggle_task_completion(task_id: int, db: Session = Depends(get_db)):
    """
    Toggle task completion status.
    
    **Parameters:**
    - **task_id**: Task identifier
    
    **Returns:**
    - Task with toggled completion status
    
    **Raises:**
    - 404: Task not found
    """
    db_task = crud_task.toggle_task_completion(db=db, task_id=task_id)
    if db_task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with id {task_id} not found"
        )
    return db_task


@router.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id: int, db: Session = Depends(get_db)):
    """
    Delete a task.
    
    **Parameters:**
    - **task_id**: Task identifier
    
    **Raises:**
    - 404: Task not found
    """
    success = crud_task.delete_task(db=db, task_id=task_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with id {task_id} not found"
        )
    return None

