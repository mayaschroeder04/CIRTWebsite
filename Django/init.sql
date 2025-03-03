CREATE TABLE IF NOT EXISTS web_pages (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255),
    html_content TEXT
);

INSERT INTO web_pages (title, html_content)
VALUES ('main', '$(cat /docker-entrypoint-initdb.d/main.html)');


CREATE DATABASE IF NOT EXISTS criminology_db;
CREATE USER 'admin'@'%' IDENTIFIED BY 'adminpassword';
GRANT ALL PRIVILEGES ON criminology_db.* TO 'admin'@'%';
FLUSH PRIVILEGES;
