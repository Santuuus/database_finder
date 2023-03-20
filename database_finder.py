import os
import sqlite3
import csv
import sys
import binascii

# Get the directory path from the command-line argument
if len(sys.argv) != 2:
    print("Usage: python database_finder.py /path/to/directory")
    sys.exit(1)
directory = sys.argv[1]

# A list to store the database file paths
database_files = []

# Walk through the directory and its subdirectories
for root, dirs, files in os.walk(directory):
    for file in files:
        # Check if the file is an SQLite database
        with open(os.path.join(root, file), 'rb') as f:
            header = f.read(100)
            if b'SQLite format 3' in header:
                database_files.append(os.path.join(root, file))

# A list to store the table information
table_info = []

# Process each database file
for database_file in database_files:
    # Connect to the database
    conn = sqlite3.connect(database_file)
    cursor = conn.cursor()

    # Get the table names and row counts
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = [row[0] for row in cursor.fetchall()]

    for table in tables:
        cursor.execute("SELECT COUNT(*) FROM " + table + ";")
        row_count = cursor.fetchone()[0]
        table_info.append((database_file, table, row_count))

    # Close the database connection
    conn.close()

# Write the table information to a CSV file
with open("database_finder.csv", "w", newline="") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["Database File", "Table Name", "Row Count"])
    for info in table_info:
        writer.writerow(info)

# Print the table information
for info in table_info:
    print("Database file: {}, Table name: {}, Row count: {}".format(info[0], info[1], info[2]))
