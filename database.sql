CREATE DATABASE IF NOT EXISTS hostel_complaints;
USE hostel_complaints;

-- Users Table
CREATE TABLE users (
    user_id INT PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    role ENUM('student', 'warden') NOT NULL,
    room_number VARCHAR(10),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Complaints Table
CREATE TABLE complaints (
    complaint_id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    room_number VARCHAR(10) NOT NULL,
    category VARCHAR(50) NOT NULL,
    description TEXT NOT NULL,
    predicted_category VARCHAR(50),
    priority ENUM('High', 'Medium', 'Low') DEFAULT 'Medium',
    status ENUM('Pending', 'In Progress', 'Resolved') DEFAULT 'Pending',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NULL,
    resolved_at TIMESTAMP NULL,
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);

-- Insert Demo Users
-- Password for both: student123 and warden123 (hashed with bcrypt)
INSERT INTO users (username, password, role, room_number) VALUES
('student', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYIxKHOyLWG', 'student', '201'),
('warden', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYIxKHOyLWG', 'warden', NULL);

-- Insert some sample complaints for testing
INSERT INTO complaints (user_id, room_number, category, description, priority, status) VALUES
(1, '201', 'Plumbing', 'Water leaking from bathroom tap', 'High', 'Pending'),
(1, '201', 'Electrical', 'Ceiling fan not working properly', 'Medium', 'In Progress');