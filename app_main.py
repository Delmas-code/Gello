import sqlite3
from sqlite3 import Date, Error
import os
import threading

dirname = os.path.dirname(__file__)
database = f"{dirname}/Database/gelloData.db"

# function Creates a connection with the database fr access to data


def create_connection(db_file):
    conn = None
    try:
        # Creates a connection
        conn = sqlite3.connect(db_file, check_same_thread=False)
        # print("Connection successs")

    except Error as e:
        # print(e)
        pass

    return conn

# creates a cursor to be used to open up the databaasse for manipulations


def open_db():
    global conn, cur
    # Create a connection with the database

    try:
        # Creates a connection
        conn = sqlite3.connect(database, check_same_thread=False)
        # print("Connection successs")

    except Error as e:
        # print(e)
        pass

    # setup a cursor to manipulate the database

    cur = conn.cursor()


# gets the products name from database
def company_info(com):
    open_db()
    for row in cur.execute(f'SELECT company_name, company_image, email FROM Company WHERE company_name ="{com}";'):

        return row

    conn.close()
    

def com_login(usr):
    open_db()
    try:
        curs = conn.cursor()
        for row1, row2 in curs.execute(f'SELECT company_name, password FROM Company WHERE company_name ="{usr}";'):

            return row1, row2
    except:
        return False, False

    conn.close()
    
# this sis a test fuction to view users and thier password

def view():
    l1 = []
    l2 = []
    open_db()
    for row1 in cur.execute(f'SELECT company_name FROM Company;'):
        l1.append(row1)

    conn.close()

    return l1
lock = threading.Lock()
def get_view():
    open_db()
    row1 = []
    clearx= []
    curs = conn.cursor()
    for row in curs.execute(f'SELECT company_name FROM Company;'):
        row1.append(row)
        clearx.append(row)
        
    conn.close()
    return row1

# Function to update the OTP code in the database
def update_company_info(conn, companyName, email, phone, con_pass):
    sql = f'''
            UPDATE Company
            SET email = "{email}", phone = "{phone}", password = "{con_pass}"
            WHERE company_name = "{companyName}";
            '''

    cur = conn.cursor()
    cur.execute(sql)
    conn.commit()
