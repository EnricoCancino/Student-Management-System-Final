@echo off
echo MySQL Root Password Reset Script
echo ==================================

echo Stopping MySQL service...
net stop MySQL96

echo Starting MySQL in safe mode...
start /B "C:\Program Files\MySQL\MySQL Server 9.6\bin\mysqld.exe" --skip-grant-tables --skip-networking

echo Waiting for MySQL to start...
timeout /t 5 /nobreak > nul

echo Connecting to MySQL and resetting root password...
"C:\Program Files\MySQL\MySQL Server 9.6\bin\mysql.exe" -u root -e "FLUSH PRIVILEGES; ALTER USER 'root'@'localhost' IDENTIFIED BY '';"

echo Stopping MySQL...
taskkill /F /IM mysqld.exe > nul 2>&1

echo Starting MySQL service normally...
net start MySQL96

echo.
echo Password reset complete! Root password is now blank.
echo You can now run: python setup_database.py
echo.
pause