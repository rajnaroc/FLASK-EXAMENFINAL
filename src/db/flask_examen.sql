DROP DATABASE IF EXISTS flask_examentienda;

CREATE DATABASE flask_examentienda;

USE flask_examentienda;

CREATE TABLE user(
    id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(30),
    password VARCHAR(255),
    fullname VARCHAR(25)
);

CREATE TABLE productos(
    id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(15),
    precio float,
    cantidad INT,
    user_id INT UNSIGNED,
    FOREIGN KEY (user_id) REFERENCES user(id)
);