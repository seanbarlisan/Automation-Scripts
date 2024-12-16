import sqlite3 # SQL DB to store information rather than a dictionary
import os # needed to understand the DB location
from cryptography.fernet import Fernet # used to encrypt information on the device for usage

# Change the code ot implement a title alongside the username and password so we don't lose the infomration and mix up usernames and passwords

credential_storage = dict()
db_directory = "./password_manager/"
db_path = os.path.abspath(os.path.join(db_directory, "credential_database.db"))
db_connection = sqlite3.Connection(db_path)
cur = db_connection.cursor()

if os.path.isfile(db_path):
    print("Database has been created already.")
    print(f"Database path: {db_path}")

    cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='credential';")
    table_exists = cur.fetchone()

    if not table_exists:
        # Table doesn't exist, create it
        cur.execute("""
            CREATE TABLE IF NOT EXISTS credential (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL UNIQUE,
                password TEXT NOT NULL
            );
        """)
        print("Table 'credential' created.")
    else:
        print("Table 'credential' already exists.")
else:
    print(f"Database doesn't exist at {db_path}, creating new database.")
    # Table creation will be handled later

def create_credential():
    try:
        username = input("Please input your username:\n")
        while username is None and username != "exit":
            username = input("Please input a valid credential, otherwise, input exit")
            if username == "exit":
                return
        password = input("Please input your password:\n")
        while password is None and password != "exit":
            password = input("Please input a valid credential, otherwise, input exit")
            if password == "exit":
                return
        cur.execute("""
            INSERT INTO credential (username, password) VALUES (?, ?)
            """, (username, password))
        # Include encrypt option here
        db_connection.commit()
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
    finally:
        db_connection.close()
    return 

def delete_credential():
    try:
        remove_username = input("What credential would you like to remove?\n")
        while remove_username is None and remove_username != "exit":
            remove_username = input("Please input a valid credential, otherwise, input exit\n")
            if remove_username == "exit":
                return
        cur.execute("""
            DELETE FROM credential WHERE username = ?;
            """, (remove_username,))
        db_connection.commit()
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
    finally:
        db_connection.close()

def view_credential():
    try:
        view_value = input("What credential would you like to view?\n")
        while view_value is None and view_value != "exit":
            view_value = input("Please input a valid credential, otherwise, input exit\n")
            if view_value == "exit":
                return
        cur.execute("""
            SELECT username, password FROM credentials WHERE username = ?;
        """, (view_value,))
        row = cur.fetchone()
        if row:
            print(f"Username: {row[0]}, Password: {row[1]}")
        else:
            print(f"No credentials found for username '{view_value}'.")
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
        return None
    finally:
        # Close the connection
        db_connection.close()

def edit_credential():
    edit_value - input("What credential would you like to edit?\n")
    while edit_value is None and edit_value != "exit":
        edit_value = input("Please input a valid credential, otherwise, input exit\n")
        if edit_value == "exit":
            return
    credential_storage[edit_value] = input("What would you like your new password to be?\n")
    return

# Implement a function to encrypt and decrypt the password values we create, should use the fermet library

def main():
    while True:
        choice = input("What would you like to do?\n 1.) Create Credentials \n 2.) Delete Credentials \n 3.) View Credentials \n 4.) Edit Credentials")
        choice = choice.lower()
        match choice:
            case("1"):
                create_credential()
            case("2"):
                delete_credential()
            case("3"):
                view_credential()
            case("4"):
                edit_credential()
            case("exit"):
                return
            case _:
                print("Please input a option or type 'exit' to leave.\n")

    return

if __name__ == "__main__":
    main()