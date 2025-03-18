-- @block
USE criminology_db;

CREATE TABLE IF NOT EXISTS users(
    id INT PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(150) UNIQUE NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL, -- Hashed password security
    role ENUM('student', 'admin') DEFAULT 'student',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);



-- @block
CREATE TABLE IF NOT EXISTS categories (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) UNIQUE NOT NULL
);

-- @block
CREATE TABLE IF NOT EXISTS subcategories (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) UNIQUE NOT NULL,
    category_id INT NOT NULL,
    FOREIGN KEY (category_id) REFERENCES categories(id) ON DELETE CASCADE
);


-- @block
CREATE TABLE IF NOT EXISTS documents (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    category_id INT NULL,  -- Category id to represent the
    subcategory_id INT NULL, -- Controlled subcategories
    author VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    file_url VARCHAR(2083) NOT NULL,
    file_size INT,
    file_type VARCHAR(50),
    status ENUM('pending', 'rejected', 'approved') DEFAULT 'pending',
    reviewed_by INT,
    review_date TIMESTAMP NULL,
    description TEXT,
    user_id INT,
    visibility ENUM('public', 'restricted', 'admin-only') DEFAULT 'admin-only',
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE SET NULL,
    FOREIGN KEY (category_id) REFERENCES categories(id) ON DELETE SET NULL,
    FOREIGN KEY (subcategory_id) REFERENCES subcategories(id) ON DELETE SET NULL
);


-- @block
CREATE TABLE IF NOT EXISTS document_Reviews(
    id INT AUTO_INCREMENT PRIMARY KEY,
    document_id INT,
    reviewed_by INT,
    review_status ENUM('approved', 'rejected'),
    review_comments TEXT,
    review_date TIMESTAMP DEFAULT  CURRENT_TIMESTAMP,
    FOREIGN KEY (document_id) REFERENCES documents(id) ON DELETE CASCADE,
    FOREIGN KEY (reviewed_by) REFERENCES users(id) ON DELETE SET NULL
);

-- @block
CREATE TABLE IF NOT EXISTS document_permissions(
    id INT AUTO_INCREMENT PRIMARY KEY,
    document_id INT,
    user_id INT,
    access_level ENUM('view', 'edit', 'admin') DEFAULT 'view',
    FOREIGN KEY (document_id) REFERENCES documents(id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES users(id)  ON DELETE CASCADE
);