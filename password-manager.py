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

# Retrieve all passwords
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

# Delete an entry
def delete_password(entry_id):
    conn = sqlite3.connect(db)
    cursor = conn.cursor()
    cursor.execute('DELETE FROM passwords WHERE id=?', (entry_id,))
    if cursor.rowcount == 0:
        print('No entry found under ID:', {entry_id})
    else:
        conn.commit()
        print('Deleted entry with ID:', {entry_id})

# Update a username
def update_username(entry_id, new_username):
    conn = sqlite3.connect(db)
    cursor = conn.cursor()
    cursor.execute('UPDATE passwords SET username=? WHERE id=?', (new_username, entry_id))
    if cursor.rowcount == 0:
        print('No entry found under ID:', {entry_id})
    else:
        conn.commit()
        print(f'Updated username to {new_username} of entry with ID:{entry_id}')
    conn.close()

# Update a password
def update_password(entry_id, new_password):
    if not validate_password(new_password):
        print('Error: Password must be at least 8 characters and include at least one uppercase letter, lowercase letter, number, and special character')
        return
    conn = sqlite3.connect(db)
    cursor = conn.cursor()
    cursor.execute('UPDATE passwords SET password=? WHERE id=?', (new_password, entry_id))
    if cursor.rowcount == 0:
        print('No entry found under ID:', {entry_id})
    else:
        conn.commit()
        print('Updated entry with ID:', {entry_id})
    conn.close()

# Generate a password
def generate_password(length, entry_id=None):
    if length < 8:
        print("Error: Password length must be at least 8 characters")
        return
    characters = string.ascii_letters + string.digits + string.punctuation
    while True:
        password = ''.join(random.choice(characters) for _ in range(length))
        if validate_password(password):
            break

    if entry_id is not None:
        conn = sqlite3.connect(db)
        cursor = conn.cursor()
        cursor.execute('UPDATE passwords SET password=? WHERE id=?', (password, entry_id))
        conn.commit()
        if cursor.rowcount == 0:
            print('No entry found under ID:', {entry_id})
        else:
            print(f'Updated password to {password} of entry with ID:{entry_id}')
        conn.close()
    else:
        print(f"Generated Password: {password}")

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

    # Update Username
    update_user = subparsers.add_parser('update_username', help = 'Update a username via ID')
    update_user.add_argument('id', type=int, help = 'ID of entry to update (use get or get_all to find entry you wish to update)')
    update_user.add_argument('new_username', help = 'New username to be stored')

    # Update Password
    update_pass = subparsers.add_parser('update_password', help = 'Update a password via ID')
    update_pass.add_argument('id', type=int, help = 'ID of entry to update (use get or get_all to find entry you wish to update)')
    update_pass.add_argument('new_password', help = 'New password to be stored')

    # Generate Password
    generate = subparsers.add_parser('generate', help = 'Generate a password for a new or existing ID')
    generate.add_argument('-l', '--length', type=int, default=12, help='Length of the password (default of 12)')
    generate.add_argument('-u', '--update', type=int, help='Entry ID to update with generated password (optional)')

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
    elif args.command == 'update_username':
        update_username(args.id, args.new_username)
    elif args.command == 'update_password':
        update_password(args.id, args.new_password)
    elif args.command == 'generate':
        generate_password(args.length, args.update)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
