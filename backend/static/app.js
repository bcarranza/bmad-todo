// API Base URL
const API_BASE = '/api';

// State
let currentFilter = 'all';
let currentOrder = 'newest';

// DOM Elements
const addTaskForm = document.getElementById('add-task-form');
const editTaskForm = document.getElementById('edit-task-form');
const tasksList = document.getElementById('tasks-list');
const emptyState = document.getElementById('empty-state');
const loading = document.getElementById('loading');
const errorMessage = document.getElementById('error-message');
const taskCount = document.getElementById('task-count');
const filterButtons = document.querySelectorAll('.filter-btn');
const sortOrder = document.getElementById('sort-order');
const editModal = document.getElementById('edit-modal');
const closeModal = document.getElementById('close-modal');
const cancelEdit = document.getElementById('cancel-edit');

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    loadTasks();
    setupEventListeners();
});

// Event Listeners
function setupEventListeners() {
    // Add task form
    addTaskForm.addEventListener('submit', handleAddTask);
    
    // Edit task form
    editTaskForm.addEventListener('submit', handleEditTask);
    
    // Filter buttons
    filterButtons.forEach(btn => {
        btn.addEventListener('click', () => {
            currentFilter = btn.dataset.filter;
            filterButtons.forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            loadTasks();
        });
    });
    
    // Sort order
    sortOrder.addEventListener('change', (e) => {
        currentOrder = e.target.value;
        loadTasks();
    });
    
    // Modal close handlers
    closeModal.addEventListener('click', () => hideEditModal());
    cancelEdit.addEventListener('click', () => hideEditModal());
    
    // Click outside modal to close
    editModal.addEventListener('click', (e) => {
        if (e.target === editModal) {
            hideEditModal();
        }
    });
}

// API Functions
async function apiRequest(url, options = {}) {
    showLoading();
    hideError();
    
    try {
        const response = await fetch(`${API_BASE}${url}`, {
            headers: {
                'Content-Type': 'application/json',
                ...options.headers
            },
            ...options
        });
        
        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || 'An error occurred');
        }
        
        // Handle 204 No Content
        if (response.status === 204) {
            return null;
        }
        
        return await response.json();
    } catch (error) {
        showError(error.message);
        throw error;
    } finally {
        hideLoading();
    }
}

async function loadTasks() {
    try {
        const statusParam = currentFilter !== 'all' ? `?status=${currentFilter}` : '';
        const orderParam = statusParam ? `&order=${currentOrder}` : `?order=${currentOrder}`;
        const url = `/tasks${statusParam}${orderParam}`;
        
        const data = await apiRequest(url);
        renderTasks(data.tasks);
        updateTaskCount(data.total);
    } catch (error) {
        console.error('Error loading tasks:', error);
    }
}

async function createTask(taskData) {
    return await apiRequest('/tasks', {
        method: 'POST',
        body: JSON.stringify(taskData)
    });
}

async function updateTask(taskId, taskData) {
    return await apiRequest(`/tasks/${taskId}`, {
        method: 'PUT',
        body: JSON.stringify(taskData)
    });
}

async function toggleTaskCompletion(taskId) {
    return await apiRequest(`/tasks/${taskId}/complete`, {
        method: 'PATCH'
    });
}

async function deleteTask(taskId) {
    return await apiRequest(`/tasks/${taskId}`, {
        method: 'DELETE'
    });
}

// Handlers
async function handleAddTask(e) {
    e.preventDefault();
    
    const formData = new FormData(addTaskForm);
    const taskData = {
        title: formData.get('title'),
        description: formData.get('description') || null,
        due_date: formData.get('due_date') || null
    };
    
    try {
        await createTask(taskData);
        addTaskForm.reset();
        await loadTasks();
    } catch (error) {
        console.error('Error creating task:', error);
    }
}

async function handleEditTask(e) {
    e.preventDefault();
    
    const taskId = document.getElementById('edit-task-id').value;
    const formData = new FormData(editTaskForm);
    
    const taskData = {
        title: formData.get('title'),
        description: formData.get('description') || null,
        due_date: formData.get('due_date') || null
    };
    
    try {
        await updateTask(taskId, taskData);
        hideEditModal();
        await loadTasks();
    } catch (error) {
        console.error('Error updating task:', error);
    }
}

async function handleToggleCompletion(taskId) {
    try {
        await toggleTaskCompletion(taskId);
        await loadTasks();
    } catch (error) {
        console.error('Error toggling task:', error);
    }
}

async function handleDeleteTask(taskId) {
    if (!confirm('Are you sure you want to delete this task?')) {
        return;
    }
    
    try {
        await deleteTask(taskId);
        await loadTasks();
    } catch (error) {
        console.error('Error deleting task:', error);
    }
}

function handleEditClick(task) {
    document.getElementById('edit-task-id').value = task.id;
    document.getElementById('edit-task-title').value = task.title;
    document.getElementById('edit-task-description').value = task.description || '';
    document.getElementById('edit-task-due-date').value = task.due_date || '';
    
    showEditModal();
}

// UI Functions
function renderTasks(tasks) {
    if (tasks.length === 0) {
        tasksList.innerHTML = '';
        emptyState.style.display = 'block';
        return;
    }
    
    emptyState.style.display = 'none';
    tasksList.innerHTML = tasks.map(task => createTaskHTML(task)).join('');
    
    // Attach event listeners to task elements
    tasks.forEach(task => {
        const taskElement = document.querySelector(`[data-task-id="${task.id}"]`);
        
        const checkbox = taskElement.querySelector('.task-checkbox');
        checkbox.addEventListener('change', () => handleToggleCompletion(task.id));
        
        const editBtn = taskElement.querySelector('.edit-btn');
        editBtn.addEventListener('click', () => handleEditClick(task));
        
        const deleteBtn = taskElement.querySelector('.delete-btn');
        deleteBtn.addEventListener('click', () => handleDeleteTask(task.id));
    });
}

function createTaskHTML(task) {
    const completedClass = task.completed ? 'completed' : '';
    const dueDate = task.due_date ? `
        <span class="task-due-date">📅 Due: ${formatDate(task.due_date)}</span>
    ` : '';
    
    const description = task.description ? `
        <p class="task-description">${escapeHtml(task.description)}</p>
    ` : '';
    
    return `
        <div class="task-item ${completedClass}" data-task-id="${task.id}">
            <div class="task-header">
                <input 
                    type="checkbox" 
                    class="task-checkbox" 
                    ${task.completed ? 'checked' : ''}
                >
                <div class="task-content">
                    <h3 class="task-title">${escapeHtml(task.title)}</h3>
                    ${description}
                    <div class="task-meta">
                        ${dueDate}
                        <span>Created: ${formatDateTime(task.created_at)}</span>
                    </div>
                </div>
            </div>
            <div class="task-actions">
                <button class="btn btn-secondary btn-small edit-btn">✏️ Edit</button>
                <button class="btn btn-danger btn-small delete-btn">🗑️ Delete</button>
            </div>
        </div>
    `;
}

function updateTaskCount(count) {
    const text = count === 1 ? '1 task' : `${count} tasks`;
    taskCount.textContent = text;
}

function showEditModal() {
    editModal.style.display = 'flex';
}

function hideEditModal() {
    editModal.style.display = 'none';
    editTaskForm.reset();
}

function showLoading() {
    loading.style.display = 'block';
}

function hideLoading() {
    loading.style.display = 'none';
}

function showError(message) {
    errorMessage.textContent = `❌ Error: ${message}`;
    errorMessage.style.display = 'block';
}

function hideError() {
    errorMessage.style.display = 'none';
}

// Utility Functions
function formatDate(dateString) {
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'short',
        day: 'numeric'
    });
}

function formatDateTime(dateTimeString) {
    const date = new Date(dateTimeString);
    return date.toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'short',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
    });
}

function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

