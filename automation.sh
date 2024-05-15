#!/bin/bash

# MySQL root credentials
# MYSQL_ROOT_USER="root"
# MYSQL_ROOT_PASSWORD="your_root_password"

# Install necessary packages
pip install -r requirements.txt

# Commands to fully Uninstall MySQL.
# sudo apt-get remove --purge mysql-server mysql-client mysql-common -y
# sudo apt-get autoremove -y
# sudo apt-get autoclean
# sudo rm -rf /etc/mysql
# sudo rm -rf /var/lib/mysql
# sudo rm -rf /var/log/mysql



# Commands to Install MySQL.
# sudo apt-get update
# sudo apt-get install -y mysql-server

# Start MySQL
sudo systemctl start mysql

# New user details
NEW_USER="portfolio"
NEW_USER_PASSWORD="Password@123"

# MySQL command to create the new user if they do not exist
MYSQL_COMMAND="CREATE USER IF NOT EXISTS '${NEW_USER}'@'localhost' IDENTIFIED BY '${NEW_USER_PASSWORD}';"

# MySQL command to create the database if it does not exist
MYSQL_COMMAND+="CREATE DATABASE IF NOT EXISTS application_copilot;"

# MySQL command to grant all privileges to the portfolio user on the database
MYSQL_COMMAND+=" GRANT ALL PRIVILEGES ON application_copilot.* TO '${NEW_USER}'@'localhost';"
MYSQL_COMMAND+="FLUSH PRIVILEGES;"


# One command to rule them all
# CREATE USER IF NOT EXISTS 'portfolio'@'localhost' IDENTIFIED BY 'Password@123'; CREATE DATABASE IF NOT EXISTS application_copilot; GRANT ALL PRIVILEGES ON application_copilot.* TO 'portfolio'@'localhost'; FLUSH PRIVILEGES;

# Execute the MySQL commands
sudo mysql | "${MYSQL_COMMAND}"

# Appending the db creadencials to the ~/.bashrc file
echo "export SQLALCHEMY_DATABASE_URI=mysql+pymysql://portfolio: ..." >> ~/.bashrc

# Adding the secret key to the ~/.bashrc file
echo "export SECRET_KEY=..." >> ~/.bashrc

# adding openai's api key to the ~/.bashrc file
echo "export OPENAI_API_KEY=sk-proj-..." >> ~/.bashrc

# Command to make sure nginx does not start on boot
# sudo systemctl disable nginx
# command to stop nginx
# sudo systemctl stop nginx
# command to start nginx
# sudo systemctl start nginx

# Command to make sure gunicorn starts on boot
# sudo systemctl enable gunicorn
