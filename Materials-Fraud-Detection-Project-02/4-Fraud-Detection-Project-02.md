# Fraud-Detection Project

Start Docker and our docker compose files including services like, postgres, mysql, kafka, connect, kafka-ui and ... .

➡ `docker copmose -p fraud-detection  up -d`

🛑 `-p` is for project name

After our databases engines are ready, we should go for creating two tables in them as follows:   

### 🛑 Create your PostgreSQL table

```bash
docker exec -it postgres bash

psql -U postgres
```

```sql
CREATE TABLE customer (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255),
    age INT,
    email VARCHAR(255),
    purchase INT,
    timestamp TIMESTAMP,
    store VARCHAR(2),
    clerk VARCHAR(35)
);
```

### 🛑 Create your MySQL table

```bash
mysql -u root -p

password is "debezium"
```

```sql
CREATE DATABASE mariadb;

USE mariadb;

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

SHOW DATABASES;
 
SHOW TABLES;
```

### 🛑 Run the python script and check if it works

```
python generateItems.py
```

Now check the tables in your databases. 

### 🛑 Set up some DNS configs

Go to `C:\Windows\System32\drivers\etc` and open `hosts` file. Then add these DNS:

```reStructuredText
127.0.0.1 postgres
127.0.0.1 kafka
127.0.0.1 connect
127.0.0.1 zookeeper
127.0.0.1 mariadb
127.0.0.1 mysql
```

### 🛑 Write a simple bash script

```bash
./5-start.sh
```

the content of `5-start.sh` file is as follows:

```bash
#!/bin/bash

# Start Docker Compose
docker-compose -p fraud-detection -f ./1-docker-compose.yaml up -d

# Wait for cluster to start
sleep 60
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
python3 ./3-generateItems.py
```

