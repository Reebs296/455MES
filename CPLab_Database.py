import sqlite3
import os

if __name__ == '__main__':
    try:
        os.remove("Orders.db")
        os.remove("Customers.db")
        os.remove("Employees.db")
        os.remove("Inventory.db")
    except:
        pass

# create (if needed) and connect to a database
conn_orders = sqlite3.connect("Orders.db")
conn_customers = sqlite3.connect("Customers.db")
conn_employees = sqlite3.connect("Employees.db")
conn_inventory = sqlite3.connect("Inventory.db")

# cursor used to stage SQL commands
c_orders = conn_orders.cursor()
c_customers = conn_customers.cursor()
c_employees = conn_employees.cursor()
c_inventory = conn_inventory.cursor()

# stage a new table creation
sql = "CREATE TABLE Orders ()"
c_orders.execute(sql)
conn_orders.commit()

sql = "CREATE TABLE Customers ()"
c_customers.execute(sql)
conn_customers.commit()

sql = "CREATE TABLE Employees ()"
c_employees.execute(sql)
conn_employees.commit()

sql = "CREATE TABLE Inventory ()"
c_inventory.execute(sql)
conn_inventory.commit()

# add hospital records
OrderData = [
(),
(),
()
]

c_orders.executemany("INSERT INTO CPLab (Team_Name, Wins, Losses) VALUES(?,?,?)", OrderData)
conn_orders.commit()

conn_orders.close()
conn_customers.close()
conn_employees.close()
conn_inventory.close()