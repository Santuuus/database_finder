import os
import sqlite3
import csv
import argparse
from gooey import Gooey, GooeyParser

@Gooey
def main():
    # Get the directory to analyze from the command line
    parser = GooeyParser(description='Analyze SQLite databases')
    parser.add_argument('directory', widget='DirChooser')
    args = parser.parse_args()

    # A list to store the database file paths
    database_files = []
    # The directory to analyze
    directory = args.directory

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
            # get the data on the table
            cursor.execute("SELECT * FROM " + table + ";")
            row_info = cursor.fetchmany(3)
            # Execute the PRAGMA statement to get the desired pragma
            cursor.execute("PRAGMA user_version;")
            pragma=cursor.fetchone()
            # Add the table information to the list
            table_info.append((database_file, table, pragma, row_count, row_info))

        # Close the database connection
        cursor.close
        conn.close()

    # Write the table information to a CSV file
    with open("database_finder.csv", "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(
            ["Database File", "Table Name","Database Version", "Row Count", "Content"])
        for info in table_info:
            writer.writerow(info)

    # Print the table information
    for info in table_info:
        print("Database file: {}, Table name: {}, Database Version: {}, Row count: {}, Content: {}".format(info[0], info[1], info[2], info[3], info[4]))

main()