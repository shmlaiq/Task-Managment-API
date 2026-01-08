"""
Test-Driven Development (TDD) tests for Task Management API.

These tests are written FIRST (RED phase) before implementation.
"""

import pytest


class TestHealthCheck:
    """Health check endpoint tests."""

    def test_health_check(self, client):
        """Test health check endpoint returns healthy status."""
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json() == {"status": "healthy"}


class TestCreateTask:
    """CREATE operation tests - POST /tasks/"""

    def test_create_task_minimal(self, client):
        """Test creating a task with only required field (title)."""
        response = client.post("/tasks/", json={
            "title": "Complete project"
        })
        assert response.status_code == 201
        data = response.json()
        assert data["title"] == "Complete project"
        assert data["status"] == "pending"
        assert data["priority"] == "medium"
        assert "id" in data
        assert "created_at" in data

    def test_create_task_full(self, client):
        """Test creating a task with all fields."""
        response = client.post("/tasks/", json={
            "title": "Deploy application",
            "description": "Deploy the app to production server",
            "status": "in_progress",
            "priority": "urgent",
            "due_date": "2025-12-31T23:59:59"
        })
        assert response.status_code == 201
        data = response.json()
        assert data["title"] == "Deploy application"
        assert data["description"] == "Deploy the app to production server"
        assert data["status"] == "in_progress"
        assert data["priority"] == "urgent"
        assert "2025-12-31" in data["due_date"]

    def test_create_task_with_high_priority(self, client):
        """Test creating a task with high priority."""
        response = client.post("/tasks/", json={
            "title": "Fix critical bug",
            "priority": "high"
        })
        assert response.status_code == 201
        assert response.json()["priority"] == "high"

    def test_create_task_missing_title(self, client):
        """Test creating a task without title returns validation error."""
        response = client.post("/tasks/", json={
            "description": "No title provided"
        })
        assert response.status_code == 422

    def test_create_task_invalid_status(self, client):
        """Test creating a task with invalid status returns validation error."""
        response = client.post("/tasks/", json={
            "title": "Test task",
            "status": "invalid_status"
        })
        assert response.status_code == 422

    def test_create_task_invalid_priority(self, client):
        """Test creating a task with invalid priority returns validation error."""
        response = client.post("/tasks/", json={
            "title": "Test task",
            "priority": "super_urgent"
        })
        assert response.status_code == 422


class TestReadTasks:
    """READ operation tests - GET /tasks/"""

    def test_read_tasks_empty(self, client):
        """Test reading tasks when database is empty."""
        response = client.get("/tasks/")
        assert response.status_code == 200
        assert response.json() == []

    def test_read_tasks_with_data(self, client):
        """Test reading tasks when database has data."""
        # Create tasks
        client.post("/tasks/", json={"title": "Task 1"})
        client.post("/tasks/", json={"title": "Task 2"})
        client.post("/tasks/", json={"title": "Task 3"})

        response = client.get("/tasks/")
        assert response.status_code == 200
        assert len(response.json()) == 3

    def test_read_tasks_pagination_limit(self, client):
        """Test reading tasks with limit parameter."""
        # Create 5 tasks
        for i in range(5):
            client.post("/tasks/", json={"title": f"Task {i}"})

        response = client.get("/tasks/?limit=2")
        assert response.status_code == 200
        assert len(response.json()) == 2

    def test_read_tasks_pagination_skip(self, client):
        """Test reading tasks with skip parameter."""
        # Create 5 tasks
        for i in range(5):
            client.post("/tasks/", json={"title": f"Task {i}"})

        response = client.get("/tasks/?skip=3")
        assert response.status_code == 200
        assert len(response.json()) == 2

    def test_read_tasks_pagination_skip_and_limit(self, client):
        """Test reading tasks with both skip and limit."""
        # Create 10 tasks
        for i in range(10):
            client.post("/tasks/", json={"title": f"Task {i}"})

        response = client.get("/tasks/?skip=2&limit=3")
        assert response.status_code == 200
        assert len(response.json()) == 3


class TestReadTask:
    """READ single task tests - GET /tasks/{id}"""

    def test_read_task_success(self, client):
        """Test reading a single task by ID."""
        # Create a task
        create_response = client.post("/tasks/", json={
            "title": "Test Task",
            "description": "A test task"
        })
        task_id = create_response.json()["id"]

        # Read the task
        response = client.get(f"/tasks/{task_id}")
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == task_id
        assert data["title"] == "Test Task"
        assert data["description"] == "A test task"

    def test_read_task_not_found(self, client):
        """Test reading a non-existent task returns 404."""
        response = client.get("/tasks/99999")
        assert response.status_code == 404
        assert "not found" in response.json()["detail"].lower()


class TestUpdateTask:
    """UPDATE operation tests - PATCH /tasks/{id}"""

    def test_update_task_title(self, client):
        """Test updating task title."""
        # Create a task
        create_response = client.post("/tasks/", json={"title": "Original Title"})
        task_id = create_response.json()["id"]

        # Update the task
        response = client.patch(f"/tasks/{task_id}", json={
            "title": "Updated Title"
        })
        assert response.status_code == 200
        assert response.json()["title"] == "Updated Title"

    def test_update_task_status(self, client):
        """Test updating task status."""
        # Create a task
        create_response = client.post("/tasks/", json={"title": "Test Task"})
        task_id = create_response.json()["id"]

        # Update status to completed
        response = client.patch(f"/tasks/{task_id}", json={
            "status": "completed"
        })
        assert response.status_code == 200
        assert response.json()["status"] == "completed"

    def test_update_task_priority(self, client):
        """Test updating task priority."""
        # Create a task
        create_response = client.post("/tasks/", json={"title": "Test Task"})
        task_id = create_response.json()["id"]

        # Update priority to urgent
        response = client.patch(f"/tasks/{task_id}", json={
            "priority": "urgent"
        })
        assert response.status_code == 200
        assert response.json()["priority"] == "urgent"

    def test_update_task_multiple_fields(self, client):
        """Test updating multiple fields at once."""
        # Create a task
        create_response = client.post("/tasks/", json={"title": "Test Task"})
        task_id = create_response.json()["id"]

        # Update multiple fields
        response = client.patch(f"/tasks/{task_id}", json={
            "title": "New Title",
            "description": "New Description",
            "status": "in_progress",
            "priority": "high"
        })
        assert response.status_code == 200
        data = response.json()
        assert data["title"] == "New Title"
        assert data["description"] == "New Description"
        assert data["status"] == "in_progress"
        assert data["priority"] == "high"

    def test_update_task_not_found(self, client):
        """Test updating a non-existent task returns 404."""
        response = client.patch("/tasks/99999", json={"title": "New Title"})
        assert response.status_code == 404

    def test_update_task_invalid_status(self, client):
        """Test updating task with invalid status returns validation error."""
        # Create a task
        create_response = client.post("/tasks/", json={"title": "Test Task"})
        task_id = create_response.json()["id"]

        response = client.patch(f"/tasks/{task_id}", json={
            "status": "invalid_status"
        })
        assert response.status_code == 422


class TestDeleteTask:
    """DELETE operation tests - DELETE /tasks/{id}"""

    def test_delete_task_success(self, client):
        """Test deleting a task."""
        # Create a task
        create_response = client.post("/tasks/", json={"title": "To Be Deleted"})
        task_id = create_response.json()["id"]

        # Delete the task
        response = client.delete(f"/tasks/{task_id}")
        assert response.status_code == 204

        # Verify task is deleted
        get_response = client.get(f"/tasks/{task_id}")
        assert get_response.status_code == 404

    def test_delete_task_not_found(self, client):
        """Test deleting a non-existent task returns 404."""
        response = client.delete("/tasks/99999")
        assert response.status_code == 404


class TestTaskStatusTransitions:
    """Test task status workflow."""

    def test_status_pending_to_in_progress(self, client):
        """Test transitioning from pending to in_progress."""
        create_response = client.post("/tasks/", json={"title": "Test"})
        task_id = create_response.json()["id"]
        assert create_response.json()["status"] == "pending"

        response = client.patch(f"/tasks/{task_id}", json={"status": "in_progress"})
        assert response.status_code == 200
        assert response.json()["status"] == "in_progress"

    def test_status_in_progress_to_completed(self, client):
        """Test transitioning from in_progress to completed."""
        create_response = client.post("/tasks/", json={
            "title": "Test",
            "status": "in_progress"
        })
        task_id = create_response.json()["id"]

        response = client.patch(f"/tasks/{task_id}", json={"status": "completed"})
        assert response.status_code == 200
        assert response.json()["status"] == "completed"

    def test_status_to_cancelled(self, client):
        """Test transitioning to cancelled status."""
        create_response = client.post("/tasks/", json={"title": "Test"})
        task_id = create_response.json()["id"]

        response = client.patch(f"/tasks/{task_id}", json={"status": "cancelled"})
        assert response.status_code == 200
        assert response.json()["status"] == "cancelled"


class TestTaskPriorities:
    """Test task priority levels."""

    @pytest.mark.parametrize("priority", ["low", "medium", "high", "urgent"])
    def test_create_task_with_all_priorities(self, client, priority):
        """Test creating tasks with all valid priority levels."""
        response = client.post("/tasks/", json={
            "title": f"Task with {priority} priority",
            "priority": priority
        })
        assert response.status_code == 201
        assert response.json()["priority"] == priority
