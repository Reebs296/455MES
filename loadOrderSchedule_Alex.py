from DatabaseController import DatabaseController  # Import the DatabaseController class
from PyQt5 import QtWidgets as qtw  # Ensure you import QtWidgets correctly
from datetime import datetime, timedelta

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
        """
        Fetch order schedule data from the database.
        :return: A list of orders with associated customer information.
        """
        query = """
        SELECT 
            o.product_number, 
            c.name, 
            o.product_type, 
            o.upper_color,
            o.order_date, 
            o.order_time, 
            o.end_time,
            CASE 
                WHEN o.order_time IS NULL THEN 'In Queue'
                WHEN o.end_time IS NULL THEN 'In Progress'
                ELSE 'Complete'
            END AS status
        FROM Orders o
        JOIN Customers c ON c.customer_id = o.customer_id
        WHERE o.product_type = 'Phone Case'
        """
        return self.db.execute(query)

    def populateTableRow(self, row_idx, order):
        """
        Populate a single row in the tableWidget with the given order data.
        :param row_idx: Index of the row to populate.
        :param order: Tuple containing the order data.
        """
        # Extract the order data from the tuple
        product_number, customer_name, product_type, upper_color, order_date, order_time, end_time, status = order

        # Calculate due date (from end_time)
        due_date = end_time if end_time else "Not Set"
        
        # Calculate processing time (end_time - order_time)
        if order_time and end_time:
            order_time_obj = datetime.strptime(order_time, "%Y-%m-%d %H:%M:%S")
            end_time_obj = datetime.strptime(end_time, "%Y-%m-%d %H:%M:%S")
            processing_time = str(end_time_obj - order_time_obj)
        else:
            processing_time = "Not Set"

        # Set the values for each column in the row
        self.ui_orderSched.tableWidget.setItem(row_idx, 0, qtw.QTableWidgetItem(str(product_number)))  # Order ID
        self.ui_orderSched.tableWidget.setItem(row_idx, 1, qtw.QTableWidgetItem(str(customer_name)))  # Customer Name
        self.ui_orderSched.tableWidget.setItem(row_idx, 2, qtw.QTableWidgetItem(str(product_type)))  # Product
        self.ui_orderSched.tableWidget.setItem(row_idx, 3, qtw.QTableWidgetItem(str(upper_color)))  # Colour (use upper)
        self.ui_orderSched.tableWidget.setItem(row_idx, 4, qtw.QTableWidgetItem(str(due_date)))  # Due Date
        self.ui_orderSched.tableWidget.setItem(row_idx, 5, qtw.QTableWidgetItem(str(processing_time)))  # Processing Time
        self.ui_orderSched.tableWidget.setItem(row_idx, 6, qtw.QTableWidgetItem(str(order_time)))  # Start Time
        self.ui_orderSched.tableWidget.setItem(row_idx, 7, qtw.QTableWidgetItem(str(end_time) if end_time else "Not Set"))  # End Time
        self.ui_orderSched.tableWidget.setItem(row_idx, 8, qtw.QTableWidgetItem(str(status)))  # Status


    def calculateProcessingTime(self, start_time, end_time):
        """
        Calculate the processing time based on the start time and end time.
        :param start_time: The start time.
        :param end_time: The end time.
        :return: The calculated processing time.
        """
        # Assuming start_time and end_time are in a format that allows subtraction (e.g., datetime objects or timestamps)
        # If they are strings or in another format, convert them to datetime objects first
        try:
            start_time_obj = datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S")  # Adjust format as needed
            end_time_obj = datetime.strptime(end_time, "%Y-%m-%d %H:%M:%S")    # Adjust format as needed
            processing_time = end_time_obj - start_time_obj
            return str(processing_time)  # Return as a string (e.g., timedelta format)
        except Exception as e:
            print(f"Error calculating processing time: {e}")
            return "Not Set"