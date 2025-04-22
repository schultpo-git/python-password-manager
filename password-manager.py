import argparse
import sqlite3
import re
import random
import string
import pandas as pd

db = 'secrets.db'

# Initialize database
def init_db():
    conn = sqlite3.connect(db)
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
def add_password(service, username, password):
    if not validate_password(password):
        print('Error: Password must be at least 8 characters and include at least one uppercase letter, lowercase letter, number, and special character')
        return
    conn = sqlite3.connect(db)
    cursor = conn.cursor()
    cursor.execute('INSERT INTO passwords (service, username, password) VALUES (?, ?, ?)', (service, username, password))
    conn.commit()
    print(f'Added credentials for {service} under username {username}')
    conn.close()

# Retrieve a password
def get_password(service):
    conn = sqlite3.connect(db)
    cursor = conn.cursor()
    cursor.execute('SELECT id, service, username, password FROM passwords WHERE service=?', (service,))
    results = cursor.fetchall()
    conn.close()
    if results:
        df = pd.DataFrame(results, columns=['ID', 'Service', 'Username', 'Password'])
        print(df)
    else:
        print(f'No credentials found for {service}')

def get_all_passwords():
    conn = sqlite3.connect(db)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM passwords')
    results = cursor.fetchall()
    conn.close()
    if results:
        df = pd.DataFrame(results, columns=['ID', 'Service', 'Username', 'Password'])
        print(df)
    else:
        print('No entries found')

def delete_password(password_id):
    conn = sqlite3.connect(db)
    cursor = conn.cursor()
    cursor.execute('DELETE FROM passwords WHERE id=?', (password_id,))
    if cursor.rowcount == 0:
        print('No entry found under ID:', {password_id})
    else:
        conn.commit()
        print('Deleted entry with ID:', {password_id})

def main():
    parser = argparse.ArgumentParser(description='Password Manager')
    subparsers = parser.add_subparsers(dest='command')

    # Add
    add = subparsers.add_parser('add', help = 'Add a new password/credential')
    add.add_argument('service', help = 'Name of the service (iCloud, Netflix, etc.)')
    add.add_argument('username', help = 'Username/Email')
    add.add_argument('password', help = 'Password')

    # Get
    get = subparsers.add_parser('get', help = 'Retrieve login credentials for a service')
    get.add_argument('service', help = 'Name of the service (iCloud, Netflix, etc.)')

    # Get All
    get_all = subparsers.add_parser('get_all', help = 'Retreive all login credentials stored')

    # Delete
    delete = subparsers.add_parser('delete', help = 'Delete a password via ID')
    delete.add_argument('id', type=int, help = 'ID of entry to delete (use get or get_all to find entry you wish to delete)')

    args = parser.parse_args()
    init_db()

    if args.command == 'add':
        add_password(args.service, args.username, args.password)
    elif args.command == 'get':
        get_password(args.service)
    elif args.command == 'get_all':
        get_all_passwords()
    elif args.command == 'delete':
        delete_password(args.id)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
