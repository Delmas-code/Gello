import sqlite3
from sqlite3 import Date, Error
import os
from werkzeug.security import generate_password_hash


dirname = os.path.dirname(__file__)
database = f"{dirname}/gelloData.db"


dirname = os.path.dirname(__file__)
root = os.path.abspath(os.path.join(dirname, os.pardir))
com_path = os.path.join(root, "static/images/company_img")

# function Creates a connection with the database fr access to data


def create_connection(db_file):
    conn = None
    try:
        # Creates a connection
        conn = sqlite3.connect(db_file)
        # print("Connection successs")

    except Error as e:
        # print(e)
        pass

    return conn

#Func to create ouur tables


def create_table(conn, create_table_sql):
    try:
        cur = conn.cursor()
        cur.execute(create_table_sql)
        # print("table created")
    except Error as e:
        # print(e)
        pass


#Funct to insrt data into a user table

def create_Product(conn, product):
    sql = '''
            INSERT INTO Products(product_name, price, status, product_image, feature_image, product_description, companyId)
            VALUES(?, ?, ?, ?, ?, ?, ?)
            '''

    cur = conn.cursor()
    cur.execute(sql, product)
    conn.commit()


#Funct to insrt data into a user table

def create_Company(conn, company):
    sql = '''
            INSERT INTO Company(company_name, company_image, email, password, phone)
            VALUES(?, ?, ?, ?, ?)
            '''

    cur = conn.cursor()
    cur.execute(sql, company)
    conn.commit()


#The main func that performs all the task tgether
def main():

    database = f"{dirname}/gelloData.db"

    #attributes input to the Product table
    sql_create_Product_table = """ CREATE TABLE IF NOT EXISTS Products (
                                    productId integer PRIMARY KEY,
                                    product_name text NOT NULL,
                                    price text NOT NULL,
                                    status text NOT NULL,
                                    product_image text NOT NULL,
                                    feature_image text,
                                    product_description text NOT NULL,
                                    companyId text NOT NULL,
                                    FOREIGN KEY(companyId) REFERENCES Company(companyId)
                                ); """
                                
    #attributes input to the Company table
    sql_create_Company_table = """ CREATE TABLE IF NOT EXISTS Company (
                                    companyId integer PRIMARY KEY,
                                    company_name text UNIQUE NOT NULL,
                                    company_image text NOT NULL,
                                    email text NOT NULL,
                                    password text NOT NULL,
                                    phone text NOT NULL
                                ); """

    #connect to our database
    conn = create_connection(database)

    #create the table
    if conn is not None:

        #create the sample table with the attributes passed to the req func
        create_table(conn, sql_create_Company_table)
        create_table(conn, sql_create_Product_table)

    else:
        pass

    with conn:
        

        #Data About Various Products

        
        #Data for each gas companyy
        company_1_pass = "AfriGaz"
        company_1_pass_hash = generate_password_hash(company_1_pass)
        company_1 = ("AfriGaz", com_path + "/AfriGaz_9.jpg", "afrigaz@gmail.com", company_1_pass_hash, "678320110")
        
        company_2_pass = "Bocom"
        company_2_pass_hash = generate_password_hash(company_2_pass)
        company_2 = ("Bocom", com_path + "/Bocom_2.jpg", "bocom@gmail.com", company_2_pass_hash, "672530110")
        
        company_3_pass = "Gaz"
        company_3_pass_hash = generate_password_hash(company_2_pass)
        company_3 = ("Gaz", com_path + "/Bocom_2.jpg", "gaz@gmail.com", company_3_pass_hash, "672530110")

        create_Company(conn, company_1)
        create_Company(conn, company_2)
        create_Company(conn, company_3)


#Call the main() funct
if __name__ == '__main__':
    main()
