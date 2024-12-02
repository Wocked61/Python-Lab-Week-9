import sqlite3
import os

class Contacts:
    def __init__(self):
        self.database_name = ""

    def set_database_name(self, database_name):
        self.database_name = database_name

        if not os.path.exists(database_name):
            connector = sqlite3.connect(database_name)
            cursor = connector.cursor()
            cursor.execute('''
                CREATE TABLE contacts (
                    contact_id INTEGER PRIMARY KEY,
                    first_name TEXT,
                    last_name TEXT
                )
            ''')
#phone table
            cursor.execute('''
                CREATE TABLE phones (
                    phone_id INTEGER PRIMARY KEY,
                    contact_id INTEGER,
                    phone_type TEXT,
                    phone_number TEXT,
                    FOREIGN KEY (contact_id) REFERENCES contacts (contact_id)
                )
            ''')
            
            connector.commit()
            connector.close()

    def get_database_name(self):
        return self.database_name

    def add_contact(self,first_name,last_name):
        connector = sqlite3.connect(self.database_name)
        cursor = connector.cursor()
        cursor.execute('''
            INSERT INTO contacts (first_name, last_name)
            VALUES (?, ?)
        ''', (first_name, last_name))
        connector.commit()
        connector.close()
    
    def modify_contact(self, contact_id, first_name, last_name):
        connector = sqlite3.connect(self.database_name)
        cursor = connector.cursor()
        cursor.execute('''
            UPDATE contacts
            SET first_name = ?, last_name = ?
            WHERE contact_id = ?
        ''', (first_name, last_name, int(contact_id)))
        connector.commit()
        connector.close()
    
    def add_phone(self,contact_id,phone_type,phone_number):
        connector = sqlite3.connect(self.database_name)
        cursor = connector.cursor()
        cursor.execute('''
            INSERT INTO phones (contact_id, phone_type, phone_number)
            VALUES (?, ?, ?)
        ''', (int(contact_id), phone_type, phone_number))
        connector.commit()
        connector.close()

    def modify_phone(self,phone_id,phone_type, phone_number):
        connector = sqlite3.connect(self.database_name)
        cursor = connector.cursor()
        cursor.execute('''
            UPDATE phones
            SET phone_type = ?, phone_number = ?
            WHERE phone_id = ?''', (phone_type, phone_number, int(phone_id)))
        connector.commit()
        connector.close()       

    def get_contact_phone_list(self ):
        connector = sqlite3.connect(self.database_name)
        cursor = connector.cursor()
        cursor.execute('''SELECT contacts.*, phones.* FROM contacts LEFT JOIN phones ON contacts.contact_id=phones.contact_id''')
        results = cursor.fetchall()
        connector.close()
        return results