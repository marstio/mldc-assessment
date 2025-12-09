CREATE DATABASE IF NOT EXISTS task_manager_db;
USE task_manager_db;

-- Tasks Table
CREATE TABLE IF NOT EXISTS tasks (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    due_date DATE,
    priority ENUM('Low', 'Medium', 'High') DEFAULT 'Medium',
    status ENUM('Pending', 'In Progress', 'Completed') DEFAULT 'Pending',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO tasks (title, description, due_date, priority, status)
VALUES ('Finish Assessment', 'Implement and submit the Python Task Manager', '2025-12-09', 'High', 'In Progress');