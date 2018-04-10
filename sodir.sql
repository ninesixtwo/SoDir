DROP DATABASE IF EXISTS sodir;

CREATE DATABASE sodir
 CHARACTER SET utf8mb4
 COLLATE utf8mb4_unicode_ci;

USE sodir;

CREATE TABLE users (
    ID INT NOT NULL AUTO_INCREMENT,
    email VARCHAR(255),
    user_name VARCHAR(255) NOT NULL,
    session_id VARCHAR(255),
    login_key VARCHAR(36),
    PRIMARY KEY (ID)
);

CREATE TABLE socials (
    ID INT NOT NULL AUTO_INCREMENT,
    user_id INT NOT NULL,
    url VARCHAR(255) NOT NULL,
    verified BOOLEAN DEFAULT false,
    social_name VARCHAR(255),
    FOREIGN KEY (user_id) REFERENCES users(ID),
    PRIMARY KEY (ID)
);
