import sqlite3

class DatabaseController:

    def __init__(self):

        # Connect to a single database file
        self.conn = sqlite3.connect("MES.db")
        self.c = self.conn.cursor()

        # Enable foreign key constraints
        self.c.execute("PRAGMA foreign_keys = ON;")

    def buildTables(self):
        
        # Create Customers table
        self.c.execute("""
        CREATE TABLE IF NOT EXISTS Customers (
            customer_id TEXT PRIMARY KEY,          -- Changed to TEXT and matches product_number
            name TEXT NOT NULL,
            phone_number TEXT,
            email TEXT,
            shipping_address TEXT,
            billing_address TEXT
        );
        """)

        # Create Orders table
        self.c.execute("""
            CREATE TABLE IF NOT EXISTS Orders (
            product_number TEXT PRIMARY KEY,       -- Primary Key and matches customer_id
            product_type TEXT NOT NULL,
            upper_color TEXT,
            lower_color TEXT,
            upper_limit TEXT,
            lower_limit TEXT,
            order_date TEXT NOT NULL,
            order_time TEXT NOT NULL,
            customer_id TEXT NOT NULL,
            FOREIGN KEY (customer_id) REFERENCES Customers (customer_id)
        );
        """)


        # Create Employees table
        self.c.execute("""
        CREATE TABLE IF NOT EXISTS Employees (
            employee_id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            role TEXT NOT NULL,
            required_hours INTEGER NOT NULL DEFAULT 40  -- Default to 40 hours per week
        );
        """)

        # Create Inventory table
        self.c.execute("""
        CREATE TABLE IF NOT EXISTS Inventory (
            product_id INTEGER PRIMARY KEY,
            product_name TEXT NOT NULL,
            quantity INTEGER NOT NULL
        );
        """)

        # Create ShiftSchedules table
        self.c.execute("""
        CREATE TABLE IF NOT EXISTS ShiftSchedules (
            shift_id INTEGER PRIMARY KEY,
            employee_id INTEGER NOT NULL,
            start_time DATETIME NOT NULL,
            end_time DATETIME NOT NULL,
            shift_type TEXT NOT NULL,  -- Morning, Afternoon, Night
            status TEXT NOT NULL,
            FOREIGN KEY (employee_id) REFERENCES Employees (employee_id)
        );
        """)

        # Create WorkOrders table
        self.c.execute("""
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
        self.c.execute("""
        CREATE TABLE IF NOT EXISTS ProductionMetrics (
            metric_id INTEGER PRIMARY KEY,
            timestamp DATETIME NOT NULL,
            OEE FLOAT,
            downtime INTEGER,
            errors INTEGER
        );
        """)

        # Create Products table
        self.c.execute("""
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
        self.c.execute("""
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

        # Commit changes and verify
        self.conn.commit()

    def populateCustomers(self, product_number, customer_name, phone_number, email, shipping_address, billing_address):
        # Insert into Customers table
        self.c.execute("""
        INSERT INTO Customers (customer_id, name, phone_number, email, shipping_address, billing_address)
        VALUES (?, ?, ?, ?, ?, ?)
        """, (product_number, customer_name, phone_number, email, shipping_address, billing_address))


    def populateOrders(self, product_number, product_type, upper_color, lower_color, upper_limit, lower_limit, order_date, order_time):

        # Insert into Orders table
        self.c.execute("""
        INSERT INTO Orders (product_number, product_type, upper_color, lower_color, upper_limit, lower_limit, order_date, order_time, customer_id)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (product_number, product_type, upper_color, lower_color, upper_limit, lower_limit, order_date, order_time, product_number))

    def populateShifts(self, firstName, lastName, employeeNumber, maxHours, minHours, start_date, end_date):
        # If the employee number matches with dates on the current sched, then the new info replaces that
        self.c.execute("""
        INSERT INTO ShiftSchedule (firstName, lastName, employeeNumber, maxHours, minHours, start_date, end_date)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (firstName, lastName, employeeNumber, maxHours, minHours, start_date, end_date))
    
    """def populateTables(self):
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
        c.executemany("INSERT INTO ShiftSchedules (shift_id, employee_id, start_time, end_time, shift_type, status) VALUES (?, ?, ?, ?, ?, ?)", ShiftScheduleData)"""
