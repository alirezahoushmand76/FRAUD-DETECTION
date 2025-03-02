#!/bin/bash

# Start Docker Compose
docker-compose up -d

# Wait for cluster to start
sleep 30
echo "Wait a little for our services to be run ..." 

# Run MariaDB initialization
# Variables
MYSQL_CONTAINER_NAME="mysql"  # Replace with your MySQL container name
MYSQL_ROOT_PASSWORD="debezium"          # Replace with your MySQL root password
DATABASE_NAME="mariadb"                 # Replace with your desired database name
TABLE_NAME="customer"                       # Replace with your desired table name

# Create database and table
docker exec -i $MYSQL_CONTAINER_NAME mysql -u root -p$MYSQL_ROOT_PASSWORD <<EOF
CREATE DATABASE IF NOT EXISTS $DATABASE_NAME;

USE $DATABASE_NAME;

CREATE TABLE customer (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255),
    age INT,
    email VARCHAR(255),
    purchase INT,
    timestamp DATETIME,
    store VARCHAR(2),
    clerk VARCHAR(35)		
);
EOF

echo "Database and table created successfully."

# Run PostgreSQL initialization


# Variables
POSTGRES_CONTAINER_NAME="postgres"  # Replace with your PostgreSQL container name
POSTGRES_USER="postgres"              # PostgreSQL user
POSTGRES_DB="postgres"                 # Desired database name
TABLE_NAME="customer"                  # Desired table name

# Create database and table
docker exec -i $POSTGRES_CONTAINER_NAME psql -U $POSTGRES_USER -d $POSTGRES_DB <<EOF
CREATE TABLE IF NOT EXISTS $TABLE_NAME (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255),
    age INT,
    email VARCHAR(255),
    purchase INT,
    timestamp TIMESTAMP,
    store VARCHAR(2),
    clerk VARCHAR(35)	
);
EOF

echo "PostgreSQL Database and table created successfully."

# Run the Python script to generate and insert data
python3 ./generateItems.py

