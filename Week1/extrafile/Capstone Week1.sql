-- creating database in mysql (CLI)

CREATE DATABASE sales;

USE sales; -- switching the database to use

CREATE TABLE sales_data (
	product_id INT NOT NULL,
	customer_id INT NOT NULL,
	price FLOAT NOT NULL,
	quantity INT NOT NULL,
	timestamp datetime NOT NULL);

SHOW DATABASES; -- checking if the database created and exist

SHOW TABLES; -- checking if the table is created and exist

