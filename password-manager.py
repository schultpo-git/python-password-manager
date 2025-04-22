import argparse
import sqlite3
import re
import random
import string
import pandas as pd

db_name = 'secrets.db'

# Initialize database
def init_db():
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS passwords 
                    (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                    service TEXT, 
                    username TEXT, 
                    password TEXT)''')
    conn.commit()
    conn.close()

# Validate password with regex
def validate_password(password):
    pattern = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[^a-zA-Z0-9\\s]).{8,}$'
    return re.match(pattern, password)

# Add a new password
def add(service, username, password):
    if not validate_password(password):
        print("Error: Password must be at least 8 characters and include at least one uppercase letter, lowercase letter, number, and special character.")
        return
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute('INSERT INTO passwords (service, username, password) VALUES (?, ?, ?)', (service, username, password))
    conn.commit()
    print(f"Added credentials for {service} under username {username}.")
    conn.close()

def main():
    parser = argparse.ArgumentParser(description='Password Manager')
    subparsers = parser.add_subparsers(dest='command')

    # Add
    add = subparsers.add_parser('add', help = 'Add a new password/credential')
    add.add_argument('service', help = 'Name of the service (iCloud, Netflix, etc.)')
    add.add_argument('username', help = 'Username/Email')
    add.add_argument('password', help = 'Password')

    args = parser.parse_args()
    init_db()

    if args.command == 'add':
        add_password(args.service, args.username, args.password)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
