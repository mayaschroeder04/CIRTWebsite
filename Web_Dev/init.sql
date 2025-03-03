-- init.sql
CREATE DATABASE IF NOT EXISTS criminology_db;
CREATE USER 'admin'@'%' IDENTIFIED BY 'adminpassword';
GRANT ALL PRIVILEGES ON criminology_db.* TO 'admin'@'%';
FLUSH PRIVILEGES;