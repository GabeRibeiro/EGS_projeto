import mysql.connector
from config import *
#Set mysql access credentials
db = mysql.connector.connect(
  host=Config.host,
  user=Config.user,
  password = Config.password,
  database = Config.database
)
#Cursor to access mysql
cursor = db.cursor()

#Create bills database
cursor.execute("CREATE DATABASE IF NOT EXISTS url_db")
cursor.execute("USE url_db")


cursor.execute("DROP TABLE IF EXISTS Key_url;")
cursor.execute("DROP TABLE IF EXISTS Http_url;")
cursor.execute("DROP TABLE IF EXISTS Token_url;")
cursor.execute("DROP TABLE IF EXISTS Value;")
cursor.execute("DROP TABLE IF EXISTS Basic_url;")

cursor.execute("""
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
    """)


cursor.execute("""
    CREATE TABLE Key_url( 
        metric_id INT AUTO_INCREMENT PRIMARY KEY NOT NULL,
        secret_key VARCHAR(255) NOT NULL,
        parent_id INT NOT NULL,
        
        FOREIGN KEY (parent_id) REFERENCES Basic_url(metric_id) ON DELETE CASCADE
    );
    """)


cursor.execute("""
    CREATE TABLE Http_url( 
        metric_id INT AUTO_INCREMENT PRIMARY KEY NOT NULL,
        parent_id INT NOT NULL,
        secret_key VARCHAR(300) NOT NULL,
        username VARCHAR(300) NOT NULL,
        FOREIGN KEY (parent_id) REFERENCES Basic_url(metric_id) ON DELETE CASCADE
    );
    """)


cursor.execute("""
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
    """)

cursor.execute("""
    CREATE TABLE Value( 
        url_id INT NOT NULL,
        timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        tag VARCHAR(100) PRIMARY KEY,
        value FLOAT,
        FOREIGN KEY (url_id) REFERENCES Basic_url(metric_id) ON DELETE CASCADE
    );
    """)

print("Database and Tables created successfully")