import sqlite3

class DatabaseController:

    def __init__(self):

        # Connect to a single database file
        conn = sqlite3.connect("MES.db")
        c = conn.cursor()

        # Enable foreign key constraints
        c.execute("PRAGMA foreign_keys = ON;")

        return conn, c

    def buildTables(c, conn):

        # Create Customers table
        c.execute("""
        CREATE TABLE IF NOT EXISTS Customers (
            customer_id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            contact_info TEXT
        );
        """)

        # Create Orders table
        c.execute("""
        CREATE TABLE IF NOT EXISTS Orders (
            order_id INTEGER PRIMARY KEY,
            product_details TEXT NOT NULL,
            priority INTEGER NOT NULL,
            status TEXT NOT NULL,
            customer_id INTEGER,
            FOREIGN KEY (customer_id) REFERENCES Customers (customer_id)
        );
        """)

        # Create Employees table
        c.execute("""
        CREATE TABLE IF NOT EXISTS Employees (
            employee_id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            role TEXT NOT NULL,
            required_hours INTEGER NOT NULL DEFAULT 40  -- Default to 40 hours per week
        );
        """)

        # Create Inventory table
        c.execute("""
        CREATE TABLE IF NOT EXISTS Inventory (
            product_id INTEGER PRIMARY KEY,
            product_name TEXT NOT NULL,
            quantity INTEGER NOT NULL
        );
        """)

        # Create ShiftSchedules table
        c.execute("""
        CRdEATE TABLE IF NOT EXISTS ShiftSchedules (
            shift_id INTEGER PRIMARY KEY,
            employee_id INTEGER NOT NULL,
            start_time DATETIME NOT NULL,
            end_time DATETIME NOT NULL,
            shift_type TEXT NOT NULL,  -- Morning, Afternoon, Night
            hours INTEGER NOT NULL,   -- Hours worked (0-8)
            date DATE NOT NULL,       -- Specific day of the shift
            FOREIGN KEY (employee_id) REFERENCES Employees (employee_id)
        );
        """)

        # Create WorkOrders table
        c.execute("""
        CREATE TABLE IF NOT EXISTS WorkOrders (
            work_order_id INTEGER PRIMARY KEY,
            order_id INTEGER,
            task_description TEXT NOT NULL,
            assigned_to INTEGER,
            status TEXT NOT NULL,
            FOREIGN KEY (order_id) REFERENCES Orders (order_id),
            FOREIGN KEY (assigned_to) REFERENCES Employees (employee_id)
        );
        """)

        # Create ProductionMetrics table
        c.execute("""
        CREATE TABLE IF NOT EXISTS ProductionMetrics (
            metric_id INTEGER PRIMARY KEY,
            timestamp DATETIME NOT NULL,
            OEE FLOAT,
            downtime INTEGER,
            errors INTEGER
        );
        """)

        # Create Products table
        c.execute("""
        CREATE TABLE IF NOT EXISTS Products (
            product_id INTEGER PRIMARY KEY,
            product_name TEXT NOT NULL,
            specifications TEXT,
            sorting_rule TEXT,
            inventory_id INTEGER,
            FOREIGN KEY (inventory_id) REFERENCES Inventory (product_id)
        );
        """)

        # Create QualityControl table
        c.execute("""
        CREATE TABLE IF NOT EXISTS QualityControl (
            qc_id INTEGER PRIMARY KEY,
            order_id INTEGER,
            checked_by INTEGER,
            status TEXT NOT NULL,
            notes TEXT,
            FOREIGN KEY (order_id) REFERENCES Orders (order_id),
            FOREIGN KEY (checked_by) REFERENCES Employees (employee_id)
        );
        """)

        # Populate Customers table
        CustomerData = [
            (1, "John Doe", "john.doe@example.com"),
            (2, "Jane Smith", "jane.smith@example.com")
        ]
        c.executemany("INSERT INTO Customers (customer_id, name, contact_info) VALUES (?, ?, ?)", CustomerData)

        # Populate Orders table
        OrderData = [
            (1, "Phone Model A", 1, "Pending", 1),
            (2, "Phone Model B", 2, "In Progress", 2)
        ]
        c.executemany("INSERT INTO Orders (order_id, product_details, priority, status, customer_id) VALUES (?, ?, ?, ?, ?)", OrderData)

        # Populate Employees table
        EmployeeData = [
            (1, "Alice Johnson", "Technician", 40),
            (2, "Bob Brown", "Manager", 35),
            (3, "Charlie Smith", "Operator", 30)
        ]
        c.executemany("INSERT INTO Employees (employee_id, name, role, required_hours) VALUES (?, ?, ?, ?)", EmployeeData)

        # Populate Inventory table
        InventoryData = [
            (1, "Phone Model A", 50),
            (2, "Phone Model B", 30)
        ]
        c.executemany("INSERT INTO Inventory (product_id, product_name, quantity) VALUES (?, ?, ?)", InventoryData)

        # Populate ShiftSchedules table
        ShiftScheduleData = [
            (1, 1, "2024-11-01 06:00:00", "2024-11-01 14:00:00", "Morning", "Confirmed"),
            (2, 2, "2024-11-01 14:00:00", "2024-11-01 22:00:00", "Afternoon", "Confirmed")
        ]
        c.executemany("INSERT INTO ShiftSchedules (shift_id, employee_id, start_time, end_time, shift_type, status) VALUES (?, ?, ?, ?, ?, ?)", ShiftScheduleData)

        # Commit changes and verify
        conn.commit()

if __name__ == "__main__":

    test = DatabaseController

    # Test query
    query = """
    SELECT o.order_id, o.product_details, o.status, c.name, e.name AS employee
    FROM Orders o
    JOIN Customers c ON o.customer_id = c.customer_id
    LEFT JOIN WorkOrders w ON o.order_id = w.order_id
    LEFT JOIN Employees e ON w.assigned_to = e.employee_id
    """
    test.c.execute(query)
    print(test.c.fetchall())

    # Close the connection
    test.conn.close()
