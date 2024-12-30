import sqlite3 # SQL DB to store information rather than a dictionary
import os # needed to understand the DB location
import boto3 # used to get a secret from AWS and interact with our AWS servers
from botocore.exceptions import ClientError
import re # used for partial matching of the title if not fully typed out or atleast closely typed
import http.client # used for connecting to Rapid API
from cryptography.fernet import Fernet # used to encrypt information on the device for usage

# Future goal is to add a new SQL service rather than use sqlite3

credential_storage = dict()
db_directory = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.abspath(os.path.join(db_directory, "credential_database.db"))
db_connection = sqlite3.Connection(db_path)
cur = db_connection.cursor()

def get_secret():

    secret_name = "BreachDirectory"
    region_name = "us-east-1"

    # Create a Secrets Manager client
    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name=region_name
    )

    try:
        get_secret_value_response = client.get_secret_value(
            SecretId=secret_name
        )
    except ClientError as e:
        raise e

    secret = get_secret_value_response['SecretString']

    

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
                title TEXT NOT NULL UNIQUE,
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
        title = input("Please input the title of your credential:\n")
        while title is None and title != "exit":
            title = input("Please input a valid credential, otherwise, input exit")
            if title == "exit":
                return
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
            INSERT INTO credential (title, username, password) VALUES (?, ?, ?)
            """, (title, username, password))
        # Include encrypt option here
        db_connection.commit()
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
    finally:
        return 

def delete_credential():
    new_con = sqlite3.connect(db_path)
    new_cur = new_con.cursor()
    new_cur.execute("SELECT title FROM credential") # This is how we will view the certain row we want
    print("These are the listed credentials:")
    rows = new_cur.fetchall()
    if not rows:
        print("The database is currently empty.")
        return
    else:
        for row in rows:
            print(row[0])
    try:
        remove_title = input("What credential would you like to remove?\n")
        while remove_title is None and remove_title != "exit":
            remove_title = input("Please input a valid credential, otherwise, input exit\n")
            if remove_title == "exit":
                return
        cur.execute("""
            DELETE FROM credential WHERE title = ?;
            """, (remove_title,))
        print("The credential " + remove_title + " has been deleted\n")
        db_connection.commit()
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
    finally:
        return

def view_credential():
    new_con = sqlite3.connect(db_path)
    new_cur = new_con.cursor()
    new_cur.execute("SELECT title FROM credential") # This is how we will view the certain row we want
    print("These are the listed credentials:")
    rows = new_cur.fetchall()
    if not rows:
        print("The database is currently empty.")
        return
    else:
        for row in rows:
            print(row[0])
    try:
        view_value = input("What credential would you like to view?\n")
        while view_value is None and view_value != "exit":
            view_value = input("Please input a valid credential, otherwise, input exit\n")
            if view_value == "exit":
                return
        cur.execute("""
            SELECT title, username, password FROM credential WHERE title = ?;
        """, (view_value,))
        row = cur.fetchone()
        if row:
            print(f"Username: {row[1]}, Password: {row[2]}")
        else:
            print(f"No credentials found for title '{view_value}'.")
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
        return None
    finally:
        return

def edit_credential():
    new_con = sqlite3.connect(db_path)
    new_cur = new_con.cursor()
    new_cur.execute("SELECT title FROM credential") # This is how we will view the certain row we want
    print("These are the listed credentials:")
    rows = new_cur.fetchall()
    if not rows:
        print("The database is currently empty.")
        return
    else:
        for row in rows:
            print(row[0])
    edit_value = input("What credential would you like to edit?\n")
    while edit_value is None and edit_value != "exit":
        edit_value = input("Please input a valid credential, otherwise, input exit\n")
        if edit_value == "exit":
            return
    #
    new_cur.execute("""
            SELECT title, username, password 
            FROM credential 
            WHERE title = ?;
        """, (edit_value,))
    # Fetch and display the results
    result = new_cur.fetchall()
    if not result:
        print(f"No credentials found for title: {edit_value}")
    else:
        for row in result:
            print(f"Title: {row[0]}, Username: {row[1]}, Password: {row[2]}")
    new_username = input("What is the new username? If nothing, please insert 'next'\n")
    if new_username.lower() == "next":
        new_password = input("What is the new password? If nothing, please insert 'next'\n")
        if new_password.lower() == "next":
            return
    else:
        new_password = input("What is the new password? If nothing, please insert 'next'\n")
        if new_password.lower() == "next":
            return

    new_cur.execute("""
        UPDATE credential
        SET username = ?, password = ?
        WHERE title = ?;
    """, (new_username, new_password, edit_value))

    print("Credentials updated successfully!")
    return

def check_breach():
    new_con = sqlite3.connect(db_path)
    new_cur = new_con.cursor()
    new_cur.execute("SELECT title FROM credential") # This is how we will view the certain row we want
    print("These are the listed credentials:")
    rows = new_cur.fetchall()
    if not rows:
        print("The database is currently empty.")
        return
    else:
        for row in rows:
            print(row[0])
    try:
        view_value = input("What credential would you like to view if it has been breached?\n")
        while view_value is None and view_value != "exit":
            view_value = input("Please input a valid credential, otherwise, input exit\n")
            if view_value == "exit":
                return
        cur.execute("""
            SELECT title, username, password FROM credential WHERE title = ?;
        """, (view_value,))
        row = cur.fetchone()
        if row:
            print(f"Password: {row[2]}")
        else:
            print(f"No credentials found for title '{view_value}'.")
        
    # except sqlite3.Error as e:
    #     print(f"An error occurred: {e}")
    #     return None
    # Is there a better way to do this?

    finally:
        return

def main():
    while True:
        choice = input("What would you like to do?\n 1.) Create Credentials \n 2.) Delete Credentials \n 3.) View Credentials \n 4.) Edit Credentials\n 5.) Check for Breach \n 6.) Exit\n")
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
            case("5"):
                check_breach()
            case("6"):
                print("Thank you!")
                return
            case("exit"):
                print("Thank you!")
                return
            case _:
                print("Please input a option or type 'exit' to leave.\n")

    return

if __name__ == "__main__":
    main()


# Look into why the Database becomes locked and broken