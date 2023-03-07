import sqlite3

class DataBaseCustomers:
    def __init__(self):
        self.connect = sqlite3.connect('DodoBase.db')

    def connect_db(self):
        cursor = self.connect.cursor()
        cursor.execute("""CREATE TABLE IF NOT EXISTS customers (
        first_name VARCHAR(255),
        last_name VARCHAR(255),
        username VARCHAR(255),
        user_id INTEGER,
        phone_number INTEGER DEFAULT 0
        );""")

        cursor.execute("""CREATE TABLE IF NOT EXISTS address (
        id_user INTEGER,
        address_longtitude INTEGER,
        address_latitude INTEGER
        );""")

        cursor.execute("""CREATE TABLE IF NOT EXISTS orders (
        user_id INTEGER,
        title VARCHAR(255),
        address_destination INTEGER(255),
        date_time_order VARCHAR(120)
        );""")

        self.connect.commit()