# Student-Management-System-Final

## Instructions

#------- Run the Program -------
To run the program, follow these steps:

1. Run the Login-Page.py file to open the login page.
2. Enter the username and password to log in.
    username: admin
    password: password
3. After logging in, you will be directed to the main page where you can manage students, courses, and grades.

#------- Connect to Database -------
1. Click "Connect to Database" button on the main page.
2. Enter the database connection details:
    Host: localhost
    Username: root
    Password: (your MySQL root password)
3. Click "Connect" to establish a connection to the MySQL database.

#------- Run MySQL -------
run program:
& "C:\Program Files\MySQL\MySQL Server 9.6\bin\mysql.exe" -u root -p

to see database:
show databases;
use student_management;
select * from students;

to see students:
show databases;
use student_management;
show tables;
select * from students;

to see student dashboard:
*students
