-- Run this script to setup a database environment for Michote locally
-- The database created will be for dev purposes only.

CREATE DATABASE IF NOT EXISTS michote_dev_db;
CREATE USER IF NOT EXISTS 'michote_dev'@'localhost' IDENTIFIED BY '@Michote_dev_123';
GRANT ALL PRIVILEGES ON `michote_dev_db`.* TO 'michote_dev'@'localhost';
GRANT SELECT ON `performance_schema`.* TO 'michote_dev'@'localhost';
FLUSH PRIVILEGES;
