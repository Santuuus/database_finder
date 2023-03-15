import os
import sqlite3
import binascii
import sys

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
        # Try to connect to the file as a SQLite database
        try:
            with open(os.path.join(root, file), 'rb') as f:
                header = f.read(16)
                if header.startswith(b'SQLite format'):
                    conn = sqlite3.connect(os.path.join(root, file))
                    cursor = conn.cursor()
                    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
                    # If we got here without an exception, the file is a SQLite database
                    database_files.append(os.path.join(root, file))
                    cursor.close()
                    conn.close()
        except (sqlite3.DatabaseError, IOError, binascii.Error):
            # If we got here, the file is not a SQLite database
            pass

# Print the database file paths
if database_files:
    print("The following files are SQLite databases:")
    for file in database_files:
        print(file)
else:
    print("No SQLite databases found in the directory.")
