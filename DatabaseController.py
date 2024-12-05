import sqlite3
from datetime import datetime, timedelta

class DatabaseController:

    def __init__(self):
        try:
            self.conn = sqlite3.connect("database.db")  # Ensure the database path is correct
            self.c = self.conn.cursor()
            print("Database connection established.")
            
            # Create tables before checking for columns
            self.buildTables()
            
            # Check and add any necessary columns
            self.check_and_add_end_time_column()
        except sqlite3.Error as e:
            print(f"Error initializing database: {e}")

    def check_and_add_end_time_column(self):
        """Ensure the 'end_time' column exists in the Orders table."""
        self.c.execute("PRAGMA table_info(Orders);")
        columns = [column[1] for column in self.c.fetchall()]
        if "end_time" not in columns:
            self.c.execute("""
                ALTER TABLE Orders ADD COLUMN end_time TEXT;
            """)
            self.conn.commit()

    def execute(self, query, params=None):
        try:
            if params is None:
                self.c.execute(query)
            else:
                self.c.execute(query, params)
            return self.c.fetchall()  # Fetch and return all results
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            return []

    def buildTables(self):
        try:
            print("Creating tables if they don't exist...")

            # Create Customers table
            self.c.execute("""
            CREATE TABLE IF NOT EXISTS Customers (
                customer_id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                phone_number TEXT,
                email TEXT,
                shipping_address TEXT,
                billing_address TEXT
            );
            """)
            print("'Customers' table created successfully.")

            # Create Orders table
            self.c.execute("""
            CREATE TABLE IF NOT EXISTS Orders (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                customer_id INTEGER,  -- Foreign key to link to Customers
                product_number TEXT NOT NULL,
                product_type TEXT,
                upper_color TEXT,
                lower_color TEXT,
                upper_limit REAL,
                lower_limit REAL,
                order_date TEXT,
                order_time TEXT,
                end_time TEXT,
                FOREIGN KEY(customer_id) REFERENCES Customers(customer_id) ON DELETE CASCADE
            );
            """)
            print("'Orders' table created successfully.")

            self.conn.commit()
        except sqlite3.Error as e:
            print(f"Error creating tables: {e}")

    def populateCustomers(self, product_number, customer_name, phone_number, email, shipping_address, billing_address):
        try:
            self.c.execute("""
                INSERT INTO Customers (customer_id, name, phone_number, email, shipping_address, billing_address)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (product_number, customer_name, phone_number, email, shipping_address, billing_address))
            self.conn.commit()  # Commit after insertion
        except sqlite3.Error as e:
            print(f"Error inserting customer: {e}")

    def populateOrders(self, product_number, product_type, upper_color, lower_color, upper_limit, lower_limit, order_date, order_time):
        try:
            # Convert the 'order_date' and 'order_time' into the correct format
            try:
                # Convert 'DD/MM/YYYY' to 'YYYY-MM-DD' for the date
                order_date_obj = datetime.strptime(order_date, "%d/%m/%Y")
                order_date_formatted = order_date_obj.strftime("%Y-%m-%d")
            except ValueError as e:
                print(f"Error parsing date {order_date}: {e}")
                order_date_formatted = "Not Set"  # Default value if parsing fails

            try:
                # Convert 'hh:mm:ss' to 'HH:mm:ss' for the time
                order_time_obj = datetime.strptime(order_time, "%H:%M:%S")
                order_time_formatted = order_time_obj.strftime("%H:%M:%S")
            except ValueError as e:
                print(f"Error parsing time {order_time}: {e}")
                order_time_formatted = "Not Set"  # Default value if parsing fails

            # Combine date and time into one datetime object
            if order_date_formatted != "Not Set" and order_time_formatted != "Not Set":
                order_datetime = datetime.strptime(order_date_formatted + " " + order_time_formatted, "%Y-%m-%d %H:%M:%S")
            else:
                order_datetime = None  # Handle case where either date or time is not set

            # Simulating a 5-minute 'end_time' for testing
            if order_datetime:
                end_time = order_datetime + timedelta(minutes=5)
                end_time_str = end_time.strftime("%Y-%m-%d %H:%M:%S")
            else:
                end_time_str = None

            # Insert order with simulated end_time
            self.c.execute("""
                INSERT INTO Orders (product_number, product_type, upper_color, lower_color, upper_limit, lower_limit, order_date, order_time, end_time, customer_id)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (product_number, product_type, upper_color, lower_color, upper_limit, lower_limit, order_date_formatted, order_time_formatted, end_time_str, product_number))

            self.conn.commit()
        except sqlite3.Error as e:
            print(f"Error inserting order: {e}")

    def updateCustomerAndOrder(self, product_number, customer_name, phone_number, email, shipping_address, billing_address,
                               product_type, upper_color, lower_color, upper_limit, lower_limit, order_date, order_time):
        try:
            # Update customer data
            self.c.execute("""
                UPDATE Customers
                SET name = ?, phone_number = ?, email = ?, shipping_address = ?, billing_address = ?
                WHERE customer_id = ?
            """, (customer_name, phone_number, email, shipping_address, billing_address, product_number))

            # Update order data
            self.c.execute("""
                UPDATE Orders
                SET product_type = ?, upper_color = ?, lower_color = ?, upper_limit = ?, lower_limit = ?, order_date = ?, order_time = ?
                WHERE product_number = ?
            """, (product_type, upper_color, lower_color, upper_limit, lower_limit, order_date, order_time, product_number))

            self.conn.commit()  # Commit after updates
        except sqlite3.Error as e:
            print(f"Error updating customer or order: {e}")

    def close(self):
        """Close the database connection when done."""
        self.conn.close()

    def populateTestData(self):
        """
        Insert test data into Customers and Orders tables for testing purposes.
        """
        try:
            print("Populating test data...")

            # Insert test customers
            self.c.execute("""
            INSERT OR IGNORE INTO Customers (customer_id, name, phone_number, email, shipping_address, billing_address)
            VALUES 
                (1, 'John Doe', '1234567890', 'john.doe@example.com', '123 Test St', '456 Billing St'),
                (2, 'Jane Smith', '9876543210', 'jane.smith@example.com', '789 Another St', '101 Main St');
            """)

            # Insert test orders with a valid customer_id
            self.c.execute("""
            INSERT OR IGNORE INTO Orders (customer_id, product_number, product_type, upper_color, lower_color, upper_limit, lower_limit, order_date, order_time, end_time)
            VALUES 
                (1, 'P001', 'Phone Case', 'Red', 'White', 10.0, 5.0, '2024-12-01', '08:00:00', '2024-12-01 08:05:00'),
                (2, 'P002', 'Phone Case', 'Blue', 'Black', 8.0, 4.0, '2024-12-02', '09:00:00', NULL);
            """)

            self.conn.commit()
            print("Test data inserted successfully.")
        except sqlite3.Error as e:
            print(f"Error inserting test data: {e}")

