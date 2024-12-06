from DatabaseController_Alex import DatabaseController  # Import the DatabaseController class
from PyQt5 import QtWidgets as qtw  # Ensure you import QtWidgets correctly
from datetime import datetime, timedelta
import sqlite3

class OrderScheduleLoader:
    def __init__(self, ui_orderSched):
        self.ui_orderSched = ui_orderSched
        self.db = DatabaseController()  # Reuse a central database controller for queries

    def loadOrderSchedule(self):
        """
        Load the order schedule into the tableWidget on the UI.
        """
        try:
            # Step 1: Clear any existing content in the tableWidget before adding new rows
            self.ui_orderSched.tableWidget.clearContents()

            # Step 2: Fetch order schedule data from the database
            orders = self.fetchOrderData()

            # Step 3: Check if there are any orders to display
            if orders:
                # Step 4: Set the number of rows in the table based on the data fetched
                self.ui_orderSched.tableWidget.setRowCount(len(orders))

                # Step 5: Populate the table with order data
                for row_idx, order in enumerate(orders):
                    self.populateTableRow(row_idx, order)

            else:
                print("No orders found to load.")

        except Exception as e:
            print(f"Error loading order schedule: {e}")

    def fetchOrderData(self):
        query = """
        SELECT 
            o.product_number, 
            c.name, 
            o.product_type, 
            o.upper_color,
            o.order_date, 
            o.order_time, 
            o.end_time,
            o.upper_limit,  -- Upper limit (float)
            o.lower_limit,  -- Lower limit (float)
            CASE 
                WHEN o.order_time IS NULL THEN 'In Queue'
                WHEN o.end_time IS NULL THEN 'In Progress'
                ELSE 'Complete'
            END AS status
        FROM Orders o
        JOIN Customers c ON c.customer_id = o.customer_id
        WHERE o.product_type = 'Phone Case'
        """
        try:
            print("Executing query to fetch orders...")
            self.db.c.execute(query)  # Execute the query
            result = self.db.c.fetchall()  # Fetch all results

            # Format the rows to ensure floats are correctly formatted as strings
            formatted_result = []
            for row in result:
                # Adjust for the correct number of columns (9 columns including 'status')
                formatted_row = list(row)

                # Format the upper_limit and lower_limit as strings with two decimal places
                formatted_row[7] = f"{formatted_row[7]:.2f}" if isinstance(formatted_row[7], float) else formatted_row[7]
                formatted_row[8] = f"{formatted_row[8]:.2f}" if isinstance(formatted_row[8], float) else formatted_row[8]

                formatted_result.append(tuple(formatted_row))

            print(f"Orders fetched: {formatted_result}")  # Debugging: Log the fetched data
            return formatted_result
        except sqlite3.Error as e:
            print(f"Error fetching orders: {e}")
            return []

    def populateTableRow(self, row_idx, order):
        """
        Populate a single row in the tableWidget with the given order data.
        :param row_idx: Index of the row to populate.
        :param order: Tuple containing the order data.
        """
        # Unpack the order data (9 values)
        product_number, customer_name, product_type, upper_color, order_date, order_time, end_time, upper_limit, lower_limit, status = order

        # Calculate Due Date: If end_time exists, use it, otherwise set it as "Not Set"
        due_date = end_time if end_time else "Not Set"

        # Calculate Processing Time: (end_time - order_time), or "Not Set" if either time is missing
        if order_time and end_time:
            try:
                order_time_obj = datetime.strptime(order_time, "%Y-%m-%d %H:%M:%S")
                end_time_obj = datetime.strptime(end_time, "%Y-%m-%d %H:%M:%S")
                processing_time = str(end_time_obj - order_time_obj)
            except Exception as e:
                processing_time = "Not Set"
                print(f"Error calculating processing time: {e}")
        else:
            processing_time = "Not Set"

        # Determine the Status:
        if not order_time:
            status = "In Queue"
        elif not end_time:
            status = "In Progress"
        else:
            status = "Complete"

        # Set the values for each column in the row
        self.ui_orderSched.tableWidget.setItem(row_idx, 0, qtw.QTableWidgetItem(str(product_number)))  # Order ID
        self.ui_orderSched.tableWidget.setItem(row_idx, 1, qtw.QTableWidgetItem(str(customer_name)))  # Customer Name
        self.ui_orderSched.tableWidget.setItem(row_idx, 2, qtw.QTableWidgetItem(str(product_type)))  # Product
        self.ui_orderSched.tableWidget.setItem(row_idx, 3, qtw.QTableWidgetItem(str(upper_color)))  # Colour (upper)
        self.ui_orderSched.tableWidget.setItem(row_idx, 4, qtw.QTableWidgetItem(str(due_date)))  # Due Date
        self.ui_orderSched.tableWidget.setItem(row_idx, 5, qtw.QTableWidgetItem(str(processing_time)))  # Processing Time
        self.ui_orderSched.tableWidget.setItem(row_idx, 6, qtw.QTableWidgetItem(str(order_time)))  # Start Time
        self.ui_orderSched.tableWidget.setItem(row_idx, 7, qtw.QTableWidgetItem(str(end_time) if end_time else "Not Set"))  # End Time
        self.ui_orderSched.tableWidget.setItem(row_idx, 8, qtw.QTableWidgetItem(str(status)))  # Status
