# Password Manager
### Purpose
This script's function is to act as a(n insecure) password manager for any sites/services that you may have a login for. The script can add, delete, update, and retrieve entries in the SQL database as well as generate new passwords for new or existing entries.

### Usage
**Add an Entry:** `python password_manager.py add <service> <username/email> <password>`  
**Delete an Entry:** `python password_manager.py delete <entry id>`  
**Update a Username:** `python password_manager.py update_username <entry id> <new username>`  
**Update a Password:** `python password_manager.py update_password <entry id> <new password>`  
**Retrieve an Entry:** `python password_manager.py get <entry id>`  
**Retrieve all Entries:** `python password_manager.py get_all`  
**Generate a Password:** `python password_manager.py generate [-l, --length] <length> [-u, --update] <entry id>`
