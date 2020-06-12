#importing the required packages
import pandas as pd
import sqlite3
from sqlite3 import Error
from datetime import datetime

# function which creates master and transaction tables
# Returns Transaction Failed if name does not exist in Employees List else returns Transaction Successful
def do_log_employee(name, conn):
    df = pd.read_excel("C:\\Users\PRUDHVIG\Desktop\SAMPLEDATA.xlsx")
    df1 = pd.read_excel("C:\\Users\PRUDHVIG\Desktop\SAMPLEDATA.xlsx")
    if name not in df.values:
        return "Transaction Failed"
    else:
        emp_id = int(df.loc[df['Name'] == name].values[0][0])
        emp_name = df.loc[df['Name'] == name].values[0][1]
        emp_location = df1.loc[df1['Emp ID'] == emp_id].values[0][1]
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        task1 = (emp_id, emp_name)
        task2 = (emp_id, emp_location, current_time)
        create_master(conn, task1)
        create_transaction(conn, task2)
        return "Transaction Successful"
#function which creates connection to the database
def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)
    return conn
#function which creates the table in the database
def create_table(conn, create_table_sql):
    """ create a table from the create_table_sql statement
    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :return:
    """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)
#function which inserts data into master table
def create_master(conn,task):
    """
    Create a new project into the master table
    :param conn:
    :param master_table:
    :return: project id
    """
    sql = ''' INSERT OR IGNORE INTO emp(emp_id,name)
              VALUES(?,?) '''
    c = conn.cursor()
    c.execute(sql,task)
    conn.commit()
#function which inserts data into transaction table
def create_transaction(conn,task):
    """
    Create a new task
    :param conn:
    :param transaction_table:
    :return:
    """
    sql = ''' INSERT OR IGNORE INTO emp1(emp_id,location,login_time)
              VALUES(?,?,?) '''
    c = conn.cursor()
    c.execute(sql,task)
    conn.commit()
#main method
def main():
    database = r"C:\Users\PRUDHVIG\.spyder-py3\fr_recognition.db"
    employee_master_table = """ CREATE TABLE IF NOT EXISTS emp (
                                                emp_id integer PRIMARY KEY NOT NULL,
                                                name text NOT NULL
                                            ); """
    employee_transaction_table = """CREATE TABLE IF NOT EXISTS emp1 (
                                    emp_id integer PRIMARY KEY NOT NULL,
                                    location text NOT NULL,
                                    login_time datetime NOT NULL,
                                    FOREIGN KEY (emp_id) REFERENCES emp (emp_id)
                                );"""
    # create a database connection
    conn = create_connection(database)
    # create tables
    if conn is not None:
        #creating master table
        create_table(conn, employee_master_table)
        #creating transaction table
        create_table(conn,employee_transaction_table)
        employee_name_id = ['Ravi Kumar','Anil Kumar AMARA','Divya Sa CHINTALACHERUVU MARY','Prudhvi Kumar']
        for i in employee_name_id:
            status = do_log_employee(i,conn)
            print(status)
    else:
        print("Error! cannot create the database connection.")
if __name__ == '__main__':
    main()
