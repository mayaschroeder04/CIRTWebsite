CREATE DATABASE IF NOT EXISTS criminology_db;

-- Switch to the database
USE criminology_db;

-- Create the user if it doesn't exist
CREATE USER IF NOT EXISTS 'admin'@'%' IDENTIFIED BY 'adminpassword';

-- Grant privileges to the user
GRANT ALL PRIVILEGES ON criminology_db.* TO 'admin'@'%';

-- Flush privileges to apply changes
FLUSH PRIVILEGES;

USE criminology_db;
--
-- CREATE TABLE IF NOT EXISTS web_pages (
--     id SERIAL PRIMARY KEY,
--     title VARCHAR(255),
--     html_content TEXT
-- );
--
-- INSERT INTO web_pages (title, html_content)
-- VALUES ('mainpage', '$(cat /docker-entrypoint-initdb.d/main.html)');
