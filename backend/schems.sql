-- Reference DDL for the employees table.
-- Also auto-created by: python -m app.db.seed
-- Kept here for clarity, manual setup, and review.

CREATE DATABASE IF NOT EXISTS employee_directory
    CHARACTER SET utf8mb4
    COLLATE utf8mb4_unicode_ci;

USE employee_directory;

CREATE TABLE IF NOT EXISTS employees (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(150) NOT NULL,
    email VARCHAR(150) NOT NULL,
    department VARCHAR(100) NOT NULL,
    designation VARCHAR(100) NOT NULL,
    date_of_joining DATE NOT NULL,

    CONSTRAINT uq_employees_email UNIQUE (email)
);

-- Indexes to improve name and department filtering.
CREATE INDEX ix_employees_name
    ON employees (name);

CREATE INDEX ix_employees_department
    ON employees (department);