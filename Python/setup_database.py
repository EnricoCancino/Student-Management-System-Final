import mysql.connector
from mysql.connector import Error

def setup_database():
    try:
        # Connect to MySQL server with the provided password
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="cancino2006"  # Your MySQL root password
        )
        
        cursor = connection.cursor()
        
        # Create database
        cursor.execute("CREATE DATABASE IF NOT EXISTS student_management")
        print("✓ Database created successfully")
        
        # Connect to the database
        cursor.execute("USE student_management")
        
        # Create students table
        create_table_query = """
        CREATE TABLE IF NOT EXISTS students (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            mobile VARCHAR(15) NOT NULL,
            email VARCHAR(100) NOT NULL,
            birthday VARCHAR(20) NULL,
            address VARCHAR(255) NULL,
            gender VARCHAR(10) NULL
        )
        """
        cursor.execute(create_table_query)
        print("✓ Students table created successfully")
        
        connection.commit()
        cursor.close()
        connection.close()
        
        print("\n✓ Database setup completed!")
        print("\nYou can now run StudentManagementSystem.py")
        
    except Error as err:
        print(f"Error: {err}")
        print("\nTroubleshooting:")
        print("1. Make sure MySQL is running")
        print("2. Verify your root password is correct")

if __name__ == "__main__":
    setup_database()
