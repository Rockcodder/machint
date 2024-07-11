CREATE DATABASE mydatabase;

USE mydatabase;

CREATE TABLE `users` (
    `user_id` INT NOT NULL AUTO_INCREMENT,
    `email` VARCHAR(100) NOT NULL,
    `password` VARCHAR(100) NOT NULL,
    PRIMARY KEY (`user_id`),
    UNIQUE KEY `email` (`email`)
);

CREATE TABLE `categories` (
    `category_id` INT NOT NULL AUTO_INCREMENT,
    `name` VARCHAR(100) NOT NULL,
    PRIMARY KEY (`category_id`)
);

CREATE TABLE `products` (
    `product_id` INT NOT NULL AUTO_INCREMENT,
    `name` VARCHAR(100) NOT NULL,
    `description` TEXT,
    `price` DECIMAL(10 , 2 ) DEFAULT NULL,
    `image_url` VARCHAR(255) DEFAULT NULL,
    `category_id` INT DEFAULT NULL,
    PRIMARY KEY (`product_id`),
    KEY `category_id` (`category_id`),
    CONSTRAINT `products_ibfk_1` FOREIGN KEY (`category_id`)
        REFERENCES `categories` (`category_id`)
);

CREATE TABLE `user_cart` (
    `cart_id` INT NOT NULL AUTO_INCREMENT,
    `user_id` INT DEFAULT NULL,
    `product_id` INT DEFAULT NULL,
    `quantity` INT DEFAULT '1',
    PRIMARY KEY (`cart_id`),
    KEY `user_id` (`user_id`),
    KEY `product_id` (`product_id`),
    CONSTRAINT `user_cart_ibfk_1` FOREIGN KEY (`user_id`)
        REFERENCES `users` (`user_id`),
    CONSTRAINT `user_cart_ibfk_2` FOREIGN KEY (`product_id`)
        REFERENCES `products` (`product_id`)
);

INSERT INTO `categories` (`name`) VALUES
	('Electronics'),
	('Clothing'),
	('Books')
;

INSERT INTO `products` (`name`, `description`, `price`, `image_url`, `category_id`) VALUES
	('Smartphone', 'High-end smartphone with latest features', '999.99', 'smartphone.jpg', '1'),
	('Laptop', 'Powerful laptop for work and gaming', '1499.99', 'laptop.jpg', '1'),
	('T-shirt', 'Comfortable cotton T-shirt', '19.99', 'tshirt.jpg', '2'),
	('Jeans', 'Classic denim jeans', '39.99', 'jeans.jpg', '2'),
	('Python Programming', 'Introduction to Python programming', '29.99', 'python_book.jpg', '3'),
	('Data Structures and Algorithms', 'Guide to data structures and algorithms', '39.99', 'dsa_book.jpg', '3')
;
