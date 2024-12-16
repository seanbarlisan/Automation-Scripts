import sqlite3 # SQL DB to store information rather than a dictionary
import json # will use in future to store all information as JSON files for the SQL DB
from cryptography.fernet import Fernet # used to encrypt information on the device for usage

credential_storage = dict()
db_connection = sqlite3.Connection("credential_database.db")
cur = db_connection.cursor()
cur.execute("CREATE TABLE credential(username, password)")

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
            INSERT INTO credential VALUES
                    (username, password) VALUES (?, ?)
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
        choice = input("What would you like to do?\n")
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