"""Unit tests for CRUD operations"""

from datetime import date
import pytest
from app.crud import task as crud_task
from app.schemas.task import TaskCreate, TaskUpdate


def test_create_task(test_db):
    """Test creating a new task"""
    task_data = TaskCreate(
        title="Test Task",
        description="Test Description",
        due_date=date(2025, 12, 31)
    )
    task = crud_task.create_task(test_db, task_data)
    
    assert task.id is not None
    assert task.title == "Test Task"
    assert task.description == "Test Description"
    assert task.due_date == date(2025, 12, 31)
    assert task.completed is False
    assert task.created_at is not None
    assert task.updated_at is not None


def test_create_task_minimal(test_db):
    """Test creating a task with only required fields"""
    task_data = TaskCreate(title="Minimal Task")
    task = crud_task.create_task(test_db, task_data)
    
    assert task.id is not None
    assert task.title == "Minimal Task"
    assert task.description is None
    assert task.due_date is None
    assert task.completed is False


def test_get_task(test_db):
    """Test retrieving a task by ID"""
    # Create a task
    task_data = TaskCreate(title="Get Task Test")
    created_task = crud_task.create_task(test_db, task_data)
    
    # Retrieve it
    retrieved_task = crud_task.get_task(test_db, created_task.id)
    
    assert retrieved_task is not None
    assert retrieved_task.id == created_task.id
    assert retrieved_task.title == "Get Task Test"


def test_get_task_not_found(test_db):
    """Test retrieving a non-existent task"""
    task = crud_task.get_task(test_db, 99999)
    assert task is None


def test_get_tasks_all(test_db):
    """Test retrieving all tasks"""
    # Create multiple tasks
    crud_task.create_task(test_db, TaskCreate(title="Task 1"))
    crud_task.create_task(test_db, TaskCreate(title="Task 2"))
    crud_task.create_task(test_db, TaskCreate(title="Task 3"))
    
    tasks = crud_task.get_tasks(test_db)
    
    assert len(tasks) == 3


def test_get_tasks_filtered_completed(test_db):
    """Test filtering tasks by completed status"""
    # Create tasks with different completion status
    task1 = crud_task.create_task(test_db, TaskCreate(title="Task 1"))
    crud_task.create_task(test_db, TaskCreate(title="Task 2"))
    
    # Mark one as completed
    crud_task.toggle_task_completion(test_db, task1.id)
    
    # Get only completed tasks
    completed_tasks = crud_task.get_tasks(test_db, status="completed")
    assert len(completed_tasks) == 1
    assert completed_tasks[0].completed is True


def test_get_tasks_filtered_pending(test_db):
    """Test filtering tasks by pending status"""
    # Create tasks
    task1 = crud_task.create_task(test_db, TaskCreate(title="Task 1"))
    crud_task.create_task(test_db, TaskCreate(title="Task 2"))
    
    # Mark one as completed
    crud_task.toggle_task_completion(test_db, task1.id)
    
    # Get only pending tasks
    pending_tasks = crud_task.get_tasks(test_db, status="pending")
    assert len(pending_tasks) == 1
    assert pending_tasks[0].completed is False


def test_get_tasks_ordered_newest(test_db):
    """Test ordering tasks by newest first"""
    task1 = crud_task.create_task(test_db, TaskCreate(title="Task 1"))
    task2 = crud_task.create_task(test_db, TaskCreate(title="Task 2"))
    task3 = crud_task.create_task(test_db, TaskCreate(title="Task 3"))
    
    tasks = crud_task.get_tasks(test_db, order="newest")
    
    # Should be in reverse order of creation
    assert tasks[0].id == task3.id
    assert tasks[1].id == task2.id
    assert tasks[2].id == task1.id


def test_get_tasks_ordered_oldest(test_db):
    """Test ordering tasks by oldest first"""
    task1 = crud_task.create_task(test_db, TaskCreate(title="Task 1"))
    task2 = crud_task.create_task(test_db, TaskCreate(title="Task 2"))
    task3 = crud_task.create_task(test_db, TaskCreate(title="Task 3"))
    
    tasks = crud_task.get_tasks(test_db, order="oldest")
    
    # Should be in order of creation
    assert tasks[0].id == task1.id
    assert tasks[1].id == task2.id
    assert tasks[2].id == task3.id


def test_update_task(test_db):
    """Test updating a task"""
    # Create a task
    task = crud_task.create_task(test_db, TaskCreate(title="Original Title"))
    
    # Update it
    update_data = TaskUpdate(title="Updated Title", description="New Description")
    updated_task = crud_task.update_task(test_db, task.id, update_data)
    
    assert updated_task is not None
    assert updated_task.title == "Updated Title"
    assert updated_task.description == "New Description"


def test_update_task_partial(test_db):
    """Test partial update of a task"""
    # Create a task
    task = crud_task.create_task(
        test_db,
        TaskCreate(title="Title", description="Description")
    )
    
    # Update only description
    update_data = TaskUpdate(description="New Description")
    updated_task = crud_task.update_task(test_db, task.id, update_data)
    
    assert updated_task.title == "Title"  # Unchanged
    assert updated_task.description == "New Description"  # Changed


def test_update_task_not_found(test_db):
    """Test updating a non-existent task"""
    update_data = TaskUpdate(title="New Title")
    result = crud_task.update_task(test_db, 99999, update_data)
    assert result is None


def test_toggle_task_completion(test_db):
    """Test toggling task completion status"""
    # Create a task (starts as incomplete)
    task = crud_task.create_task(test_db, TaskCreate(title="Task"))
    assert task.completed is False
    
    # Toggle to complete
    toggled = crud_task.toggle_task_completion(test_db, task.id)
    assert toggled.completed is True
    
    # Toggle back to incomplete
    toggled_again = crud_task.toggle_task_completion(test_db, task.id)
    assert toggled_again.completed is False


def test_toggle_task_completion_not_found(test_db):
    """Test toggling completion for non-existent task"""
    result = crud_task.toggle_task_completion(test_db, 99999)
    assert result is None


def test_delete_task(test_db):
    """Test deleting a task"""
    # Create a task
    task = crud_task.create_task(test_db, TaskCreate(title="Task to Delete"))
    task_id = task.id
    
    # Delete it
    result = crud_task.delete_task(test_db, task_id)
    assert result is True
    
    # Verify it's gone
    deleted_task = crud_task.get_task(test_db, task_id)
    assert deleted_task is None


def test_delete_task_not_found(test_db):
    """Test deleting a non-existent task"""
    result = crud_task.delete_task(test_db, 99999)
    assert result is False


def test_count_tasks(test_db):
    """Test counting all tasks"""
    crud_task.create_task(test_db, TaskCreate(title="Task 1"))
    crud_task.create_task(test_db, TaskCreate(title="Task 2"))
    crud_task.create_task(test_db, TaskCreate(title="Task 3"))
    
    count = crud_task.count_tasks(test_db)
    assert count == 3


def test_count_tasks_filtered(test_db):
    """Test counting tasks with status filter"""
    task1 = crud_task.create_task(test_db, TaskCreate(title="Task 1"))
    crud_task.create_task(test_db, TaskCreate(title="Task 2"))
    
    # Mark one as completed
    crud_task.toggle_task_completion(test_db, task1.id)
    
    completed_count = crud_task.count_tasks(test_db, status="completed")
    pending_count = crud_task.count_tasks(test_db, status="pending")
    
    assert completed_count == 1
    assert pending_count == 1

