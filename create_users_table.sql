-- Create a database named 'career_counselling'
CREATE DATABASE IF NOT EXISTS career_counselling;

-- Use the created database
USE career_counselling;

-- Create a table to store user signup details
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY, -- Unique ID for each user
    username VARCHAR(255) UNIQUE NOT NULL, -- Username (must be unique)
    password VARCHAR(255) NOT NULL, -- Password (hashed for security)
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP -- Timestamp of account creation
);