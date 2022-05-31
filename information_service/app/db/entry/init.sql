CREATE DATABASE IF NOT EXISTS url_db;
USE url_db;

DROP TABLE IF EXISTS Key_url;
DROP TABLE IF EXISTS Token_url;
DROP TABLE IF EXISTS Http_url;
DROP TABLE IF EXISTS Value_url;
DROP TABLE IF EXISTS Basic_url;


CREATE TABLE IF NOT EXISTS Basic_url( 
        metric_id INT AUTO_INCREMENT PRIMARY KEY NOT NULL,
        url VARCHAR(500) NOT NULL,
        user_id INT NOT NULL,
        value VARCHAR(100) NOT NULL,
        tag VARCHAR(100) NOT NULL,
        period INT NOT NULL,
        status BOOLEAN DEFAULT TRUE,
        auth_type VARCHAR(10)
    );


CREATE TABLE Key_url( 
        metric_id INT AUTO_INCREMENT PRIMARY KEY NOT NULL,
        secret_key VARCHAR(255) NOT NULL,
        parent_id INT NOT NULL,
        
        FOREIGN KEY (parent_id) REFERENCES Basic_url(metric_id) ON DELETE CASCADE
    );

CREATE TABLE Token_url( 
        metric_id INT AUTO_INCREMENT PRIMARY KEY NOT NULL,
        parent_id INT NOT NULL,
        token_url VARCHAR(500) NOT NULL,
        secret_key VARCHAR(300) NOT NULL,
        secret VARCHAR(300) NOT NULL,
        content_type VARCHAR(50) NOT NULL,
        auth_type VARCHAR(50) NOT NULL,

        FOREIGN KEY (parent_id) REFERENCES Basic_url(metric_id) ON DELETE CASCADE
    );

CREATE TABLE Value( 
        url_id INT NOT NULL,
        timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        tag VARCHAR(100) PRIMARY KEY,
        value FLOAT,
        FOREIGN KEY (url_id) REFERENCES Basic_url(metric_id) ON DELETE CASCADE
    );