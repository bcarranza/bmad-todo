"""Integration tests for task API endpoints"""

from datetime import date
import pytest


def test_create_task(client):
    """Test POST /api/tasks - create a new task"""
    response = client.post(
        "/api/tasks",
        json={
            "title": "Test Task",
            "description": "Test Description",
            "due_date": "2025-12-31"
        }
    )
    
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Test Task"
    assert data["description"] == "Test Description"
    assert data["due_date"] == "2025-12-31"
    assert data["completed"] is False
    assert "id" in data
    assert "created_at" in data
    assert "updated_at" in data


def test_create_task_minimal(client):
    """Test creating a task with only title"""
    response = client.post(
        "/api/tasks",
        json={"title": "Minimal Task"}
    )
    
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Minimal Task"
    assert data["description"] is None
    assert data["due_date"] is None


def test_create_task_invalid(client):
    """Test creating a task with invalid data"""
    response = client.post(
        "/api/tasks",
        json={"description": "No title"}  # Missing required title
    )
    
    assert response.status_code == 422  # Validation error


def test_list_tasks_empty(client):
    """Test GET /api/tasks when no tasks exist"""
    response = client.get("/api/tasks")
    
    assert response.status_code == 200
    data = response.json()
    assert data["tasks"] == []
    assert data["total"] == 0


def test_list_tasks(client):
    """Test GET /api/tasks - list all tasks"""
    # Create some tasks
    client.post("/api/tasks", json={"title": "Task 1"})
    client.post("/api/tasks", json={"title": "Task 2"})
    client.post("/api/tasks", json={"title": "Task 3"})
    
    response = client.get("/api/tasks")
    
    assert response.status_code == 200
    data = response.json()
    assert len(data["tasks"]) == 3
    assert data["total"] == 3


def test_list_tasks_filter_completed(client):
    """Test filtering tasks by completed status"""
    # Create tasks
    response1 = client.post("/api/tasks", json={"title": "Task 1"})
    task1_id = response1.json()["id"]
    client.post("/api/tasks", json={"title": "Task 2"})
    
    # Mark one as completed
    client.patch(f"/api/tasks/{task1_id}/complete")
    
    # Get only completed tasks
    response = client.get("/api/tasks?status=completed")
    
    assert response.status_code == 200
    data = response.json()
    assert len(data["tasks"]) == 1
    assert data["tasks"][0]["completed"] is True


def test_list_tasks_filter_pending(client):
    """Test filtering tasks by pending status"""
    # Create tasks
    response1 = client.post("/api/tasks", json={"title": "Task 1"})
    task1_id = response1.json()["id"]
    client.post("/api/tasks", json={"title": "Task 2"})
    
    # Mark one as completed
    client.patch(f"/api/tasks/{task1_id}/complete")
    
    # Get only pending tasks
    response = client.get("/api/tasks?status=pending")
    
    assert response.status_code == 200
    data = response.json()
    assert len(data["tasks"]) == 1
    assert data["tasks"][0]["completed"] is False


def test_list_tasks_order_oldest(client):
    """Test ordering tasks by oldest first"""
    client.post("/api/tasks", json={"title": "Task 1"})
    client.post("/api/tasks", json={"title": "Task 2"})
    client.post("/api/tasks", json={"title": "Task 3"})
    
    response = client.get("/api/tasks?order=oldest")
    
    assert response.status_code == 200
    data = response.json()
    assert data["tasks"][0]["title"] == "Task 1"
    assert data["tasks"][1]["title"] == "Task 2"
    assert data["tasks"][2]["title"] == "Task 3"


def test_get_task(client):
    """Test GET /api/tasks/{id} - get single task"""
    # Create a task
    response = client.post("/api/tasks", json={"title": "Get Task Test"})
    task_id = response.json()["id"]
    
    # Retrieve it
    response = client.get(f"/api/tasks/{task_id}")
    
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == task_id
    assert data["title"] == "Get Task Test"


def test_get_task_not_found(client):
    """Test getting a non-existent task"""
    response = client.get("/api/tasks/99999")
    
    assert response.status_code == 404
    data = response.json()
    assert "not found" in data["detail"].lower()


def test_update_task(client):
    """Test PUT /api/tasks/{id} - update task"""
    # Create a task
    response = client.post("/api/tasks", json={"title": "Original Title"})
    task_id = response.json()["id"]
    
    # Update it
    response = client.put(
        f"/api/tasks/{task_id}",
        json={"title": "Updated Title", "description": "New Description"}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Updated Title"
    assert data["description"] == "New Description"


def test_update_task_partial(client):
    """Test partial update of task"""
    # Create a task
    response = client.post(
        "/api/tasks",
        json={"title": "Title", "description": "Description"}
    )
    task_id = response.json()["id"]
    
    # Update only description
    response = client.put(
        f"/api/tasks/{task_id}",
        json={"description": "New Description"}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Title"  # Unchanged
    assert data["description"] == "New Description"  # Changed


def test_update_task_not_found(client):
    """Test updating a non-existent task"""
    response = client.put(
        "/api/tasks/99999",
        json={"title": "New Title"}
    )
    
    assert response.status_code == 404


def test_toggle_completion(client):
    """Test PATCH /api/tasks/{id}/complete - toggle completion"""
    # Create a task
    response = client.post("/api/tasks", json={"title": "Task"})
    task_id = response.json()["id"]
    
    # Toggle to complete
    response = client.patch(f"/api/tasks/{task_id}/complete")
    assert response.status_code == 200
    assert response.json()["completed"] is True
    
    # Toggle back to incomplete
    response = client.patch(f"/api/tasks/{task_id}/complete")
    assert response.status_code == 200
    assert response.json()["completed"] is False


def test_toggle_completion_not_found(client):
    """Test toggling completion for non-existent task"""
    response = client.patch("/api/tasks/99999/complete")
    
    assert response.status_code == 404


def test_delete_task(client):
    """Test DELETE /api/tasks/{id} - delete task"""
    # Create a task
    response = client.post("/api/tasks", json={"title": "Task to Delete"})
    task_id = response.json()["id"]
    
    # Delete it
    response = client.delete(f"/api/tasks/{task_id}")
    assert response.status_code == 204
    
    # Verify it's gone
    response = client.get(f"/api/tasks/{task_id}")
    assert response.status_code == 404


def test_delete_task_not_found(client):
    """Test deleting a non-existent task"""
    response = client.delete("/api/tasks/99999")
    
    assert response.status_code == 404


def test_health_check(client):
    """Test health check endpoint"""
    response = client.get("/health")
    
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["service"] == "todo-app"

