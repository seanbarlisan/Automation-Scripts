import sqlite3 # SQL DB to store information rather than a dictionary
import json # will use in future to store all information as JSON files for the SQL DB
from cryptography.fernet import Fernet # used to encrypt information on the device for usage

class Credential:
    def __init__(self, username, password):
        self.username = username
        self.password = password

credential_storage = dict()

def create_credential():
    new_credential = Credential()
    username = input("Please input your username.")
    while username is None and username != "exit":
        username = input("Please input a valid credential, otherwise, input exit")
        if username == "exit":
            return
    password = input("Please input your password.")
    while password is None and password != "exit":
        password = input("Please input a valid credential, otherwise, input exit")
        if password == "exit":
            return
    # store the object into the dictionary
    new_credential = Credential(username, password) # create the new object
    credential_storage[username] = Credential(username, password) # store into the dictionary
    return 

def delete_credential():
    remove_username = input("What credential would you like to remove?")
    while remove_username is None and remove_username != "exit":
        remove_username = input("Please input a valid credential, otherwise, input exit")
        if remove_username == "exit":
            return
    del credential_storage(remove_username) # Deletes the credential from the database
    return

def view_credential():
    view_value = input("What credential would you like to view?")
    while view_value is None and view_value != "exit":
        view_value = input("Please input a valid credential, otherwise, input exit")
        if view_value == "exit":
            return
    print(credential_storage[view_value].values()) # Prints out the credential KEY and credential VALUE
    return

def edit_credential():
    edit_value - input("What credential would you like to edit?")
    while edit_value is None and edit_value != "exit":
        edit_value = input("Please input a valid credential, otherwise, input exit")
        if edit_value == "exit":
            return
    credential_storage[edit_value] = input("What would you like your new password to be?")
    return

def encrypt_credential(password):
    key = Fernet.generate_key()
    fernet = Fernet(key)
    encPassword = fernet.encrypt(password.encode())
    return encPassword

def decrypt_credential(password): # how will we decrypt this password from function?
    decPassword = fernet.decrypt(password.decode())
    return

def main():
    choice = input("What would you like to do?")
    match choice:
        case("1"):
            create_credential()
        case("2"):
            delete_credential()
        case("3"):
            view_credential()
        case("4"):
            edit_credential()
    return