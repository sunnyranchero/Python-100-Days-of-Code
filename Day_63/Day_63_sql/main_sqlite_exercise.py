import sqlite3
import os

os.chdir(os.path.dirname(__file__))

# This will create a database if it does not exist
# Otherwise it establishes a connection to it.
db = sqlite3.connect("book-collection.db")

# Create a cursor to control actions on the database.
# AKA "mouse" or "pointer"
cursor = db.cursor()

# next add a table to the database
creation_query = """
CREATE TABLE books (
    id INTEGER PRIMARY KEY,
    title VARCHAR(250) NOT NULL UNIQUE,
    author VARCHAR(250) NOT NULL,
    rating FLOAT NOT NULL)
"""
## Added a check for if the table already exists so I can keep running
## the same script over and over without any issues.

check_for_table_query = """
    SELECT name 
    FROM sqlite_master 
    WHERE type='table' AND name='books'
"""
cursor.execute(check_for_table_query)
table_exists = cursor.fetchone() is not None

if not table_exists:
    cursor.execute(creation_query)
    db.commit()
else:
    print("Table already exists.")

# Then download the gui browser to test to see what happened there
# https://sqlitebrowser.org/dl/

insert_items = (1, 'Harry Potter','J.K. Rowling',9.3)
check_title = insert_items[1]

insert_query = "INSERT INTO books (id, title, author, rating) VALUES (?, ?, ?, ?)"

check_entry_query = "SELECT title FROM books WHERE title = ?"

cursor.execute(check_entry_query, (check_title,))
book_exists = cursor.fetchone() is not None

if not book_exists:
    cursor.execute(insert_query, insert_items)
    db.commit()
    print("Entry added.")
else:
    print("The book was already added.")

# SQLAlchemy can be used to simplify these entries. Moving on

