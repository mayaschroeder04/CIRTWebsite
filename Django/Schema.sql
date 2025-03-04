-- @block
CREATE TABLE Users(
    id INT PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(150) UNIQUE NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL, -- Hashed password security
    role ENUM('student', 'admin') DEFAULT 'student',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- @block
CREATE TABLE Documents(
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    author VARCHAR(255) NOT NULL,
    upload_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    file_url VARCHAR(2083) NOT NULL, -- S3 URL for the file
    file_size INT,
    file_type VARCHAR(50),
    status ENUM('pending', 'rejected', 'approved') DEFAULT 'pending',
    reviewed_by VARCHAR(255),
    review_date TIMESTAMP NULL,
    desription TEXT,
    user_id INT,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE SET NULL
);

-- @block
CREATE TABLE Document_Reviews(
    id INT AUTO_INCREMENT PRIMARY KEY,
    document_id INT,
    reviewed_by INT,
    review_status ENUM('approved', 'rejected'),
    review_comments TEXT,
    review_date TIMESTAMP DEFAULT  CURRENT_TIMESTAMP,
    FOREIGN KEY (document_id) REFERENCES Documents(id) ON DELETE CASCADE,
    FOREIGN KEY (reviewed_by) REFERENCES Users(id) ON DELETE SET NULL
);

-- @block
CREATE TABLE document_permissions(
    id INT AUTO_INCREMENT PRIMARY KEY,
    document_id INT,
    user_id INT,
    access_level ENUM('view', 'edit', 'admin') DEFAULT 'view',
    FOREIGN KEY (document_id) REFERENCES Documents(id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES Users(id)  ON DELETE CASCADE
);

