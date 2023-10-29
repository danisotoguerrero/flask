CREATE DATABASE IF NOT EXISTS  db_api_flask;
USE db_api_flask;
CREATE TABLE IF NOT EXISTS person(
    id INT(10) NOT NULL AUTO_INCREMENT,
    name VARCHAR(255) NOT NULL,
    surname VARCHAR(255) NOT NULL,
    dni INT(8) NOT NULL,
    email VARCHAR(255) NOT NULL,
    PRIMARY KEY (id)
) 
INSERT INTO person VALUES
(1, 'Juan', 'Álvarez' , 12345678, 'juan@mail.com'),
(2, 'Ana', 'Perez' , 87654321, 'ana@mail.com');

CREATE TABLE IF NOT EXISTS users(
    id INT(10) NOT NULL AUTO_INCREMENT,
    username VARCHAR(255) NOT NULL,
    password VARCHAR(255) NOT NULL,
    PRIMARY KEY (id)
) 

INSERT INTO users VALUES
(1, 'carlos', 'pass');
