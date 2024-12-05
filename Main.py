import sqlite3
from loginWindow import Ui_MainWindow
from overviewWindow import Ui_MainWindow as Ui_Overview
from oeeWindow import Ui_MainWindow as Ui_Oee
from newOrdersWindow import Ui_MainWindow as Ui_NewOrders
from existingOrdersWindow import Ui_MainWindow as Ui_ExistingOrders
from orderScheduleWindow import Ui_MainWindow as Ui_OrderSchedule
from shiftScheduleWindow import Ui_MainWindow as Ui_ShiftSchedule
from dateTime import DateTimeUpdater
from oeePlotter import OEEPlotter
from partRejectionPlotter import RejectionPlotter
from oeeCalculator import OEECaculator
from DatabaseController import DatabaseController
#import CPLabCommunication
from PyQt5 import QtWidgets as qtw
from PyQt5 import QtCore as qtc
from datetime import datetime
import pytz
import random
from CPLabOrders import Order
import logging
from PyQt5.QtCore import QDate
from PyQt5.QtWidgets import QGraphicsRectItem, QPushButton, QDateTimeEdit, QMessageBox
class MANF455_Widget(qtw.QMainWindow):
    def __init__(self):
        super().__init__()
        # create all page objects
        self.ui = Ui_MainWindow()
        self.ui_overview = Ui_Overview()
        self.ui_oee = Ui_Oee()
        self.ui_newOrders = Ui_NewOrders()
        self.ui_existingOrders = Ui_ExistingOrders()
        self.ui_orderSched = Ui_OrderSchedule()
        self.ui_shiftSched = Ui_ShiftSchedule()
        # Set up a QTimer to update the date and time every second
        self.timer = qtc.QTimer(self)
        self.timer.timeout.connect(self.updateDateTime)
        self.timer.start(1000)  # Timeout interval in milliseconds (1000ms = 1 second)
        self.date_range = []  # Initialize date_range as an empty list
        # launch login page
        self.ui.setupUi(self)
        # Connect the Enter button to the checkCredentials method
        self.ui.Enter.clicked.connect(self.checkCredentials)
    def updateDateTime(self):
        # Update the date and time for the current page (or add specific logic if you want different behavior)
        if hasattr(self, 'current_ui'):
            dt_updater = DateTimeUpdater(self.current_ui)
            dt_updater.update()
    def checkCredentials(self):
        # Define valid credentials
        credentials = {
            "Worker": "1234",
            "MaintenanceStaff": "1234",
            "QualityControl": "1234",
            "Management": "1234",
        }
        # Define first and last names based on user type
        user_info = {
        "Worker": {"first_name": "John", "last_name": "Doe"},
        "MaintenanceStaff": {"first_name": "Seth", "last_name": "Loewen"},
        "QualityControl": {"first_name": "Lucas", "last_name": "Fabian"},
        "Management": {"first_name": "Alex", "last_name": "Rybka"},
        }
        # Define user roles
        user_roles = {
            "Worker": "Worker",
            "MaintenanceStaff": "Maintenance Staff",
            "QualityControl": "Quality Control",
            "Management": "Management",
        }
        # Get entered username and password
        username = self.ui.username.text()
        password = self.ui.password.text()
        # Check if the entered credentials match any valid user type
        if username in credentials and credentials[username] == password:
            # Assign login type and show success message
            login_type = username  # The username corresponds to the login type
            qtw.QMessageBox.information(self, "Login Status", f"Login Successful\nUser Type: {login_type}")
            # Retrieve the first and last name from the user_info dictionary
            first_name = user_info[login_type]["first_name"]
            last_name = user_info[login_type]["last_name"]
            # Retrieve the role from the user_roles dictionary
            user_role = user_roles[login_type]
            # Store the full name for later use
            self.userFullName = f"{last_name}, {first_name}"
            self.userRole = user_role
            # launch overview page
            self.showOverviewPage()
        else:
            # Show denied message for invalid credentials
            qtw.QMessageBox.warning(self, "Login Status", "Denied!")    
#This is the function to handle buttons on the Overview Page
    def showOverviewPage(self):
        self.ui_overview.setupUi(self)
        # Set current_ui to the current page
        self.current_ui = self.ui_overview
        # Create DateTimeUpdater instance and update date/time
        dt_updater = DateTimeUpdater(self.ui_overview)
        dt_updater.update()
        # button on overview page to change to oee page
        self.ui_overview.pushButton_7.clicked.connect(self.showOeePage)
        
        # button on overview page to change to orders page
        self.ui_overview.pushButton_14.clicked.connect(self.showNewOrdersPage)
        # button on overview page to change to order scheduling page
        self.ui_overview.pushButton_10.clicked.connect(self.showOrderSchedulePage)
        # button on overview page to change to shift scheduling page
        self.ui_overview.pushButton_13.clicked.connect(self.showShiftSchedulePage)
        # button on overview page for the calendar 
        self.ui_overview.calendarWidget.clicked.connect(self.onDateSelected)
        # Display the full name and role in the QTextBrowser widgets on the overview page
        self.displayUserFullName()
        self.displayUserRole()
#This is the function to handle buttons on the OEE Page
    def showOeePage(self):
        self.ui_oee.setupUi(self)
        # Set current_ui to the current page
        self.current_ui = self.ui_oee
        # Create DateTimeUpdater instance and update date/time
        dt_updater = DateTimeUpdater(self.ui_oee)
        dt_updater.update()
        # button on overview page to change to overview page
        self.ui_oee.pushButton_5.clicked.connect(self.showOverviewPage)
        
        # button on overview page to change to orders page
        self.ui_oee.pushButton_14.clicked.connect(self.showNewOrdersPage)
        # button on overview page to change to order scheduling page
        self.ui_oee.pushButton_10.clicked.connect(self.showOrderSchedulePage)
        # button on overview page to change to shift scheduling page
        self.ui_oee.pushButton_13.clicked.connect(self.showShiftSchedulePage)
        # button on overview page to generate OEE calculation
        self.ui_oee.commandLinkButton.clicked.connect(self.calculateOEE)
        # button on overview page to generate availability calculation
        self.ui_oee.commandLinkButton_2.clicked.connect(self.calculateAvailability)
        # button on overview page to generate performance calculation
        self.ui_oee.commandLinkButton_3.clicked.connect(self.calculatePerformance)
        # button on overview page to generate quality calculation
        self.ui_oee.commandLinkButton_4.clicked.connect(self.calculateQuality)
        
        # button on overview page to generate quality calculation
        self.ui_oee.pushButton.clicked.connect(self.submitButton)
#This is the function to handle buttons on the New Orders Page
    def showNewOrdersPage(self):
        self.ui_newOrders.setupUi(self)
        # Set current_ui to the current page
        self.current_ui = self.ui_newOrders
        # Create DateTimeUpdater instance and update date/time
        dt_updater = DateTimeUpdater(self.ui_newOrders)
        dt_updater.update()
        # button on overview page to change to overview page
        self.ui_newOrders.pushButton_5.clicked.connect(self.showOverviewPage)
        # button on overview page to change to oee page
        self.ui_newOrders.pushButton_7.clicked.connect(self.showOeePage)
        
        # button on overview page to change to existing orders page
        self.ui_newOrders.commandLinkButton_2.clicked.connect(self.showExistingOrdersPage)
        # button on overview page to change to order scheduling page
        self.ui_newOrders.pushButton_10.clicked.connect(self.showOrderSchedulePage)
        # button on overview page to change to shift scheduling page
        self.ui_newOrders.pushButton_13.clicked.connect(self.showShiftSchedulePage)
        # Connect buttonBox signals to the appropriate functions
        self.ui_newOrders.buttonBox.accepted.connect(self.onOkClicked)
        self.ui_newOrders.buttonBox.rejected.connect(self.onCancelClicked)
#This is the function to handle buttons on the Existing Orders Page
    def showExistingOrdersPage(self):
        self.ui_existingOrders.setupUi(self)
        # Set current_ui to the current page
        self.current_ui = self.ui_existingOrders
        # Create DateTimeUpdater instance and update date/time
        dt_updater = DateTimeUpdater(self.ui_existingOrders)
        dt_updater.update()
        # button on overview page to change to overview page
        self.ui_existingOrders.pushButton_5.clicked.connect(self.showOverviewPage)
        # button on overview page to change to oee page
        self.ui_existingOrders.pushButton_7.clicked.connect(self.showOeePage)
        
        # button on overview page to change to new orders page
        self.ui_existingOrders.commandLinkButton.clicked.connect(self.showNewOrdersPage)
        # button on overview page to change to order scheduling page
        self.ui_existingOrders.pushButton_10.clicked.connect(self.showOrderSchedulePage)
        # button on overview page to change to shift scheduling page
        self.ui_existingOrders.pushButton_13.clicked.connect(self.showShiftSchedulePage)
        # Connect buttonBox signals to the appropriate functions
        self.ui_existingOrders.buttonBox.accepted.connect(self.onOkClicked2)
        self.ui_existingOrders.buttonBox.rejected.connect(self.onCancelClicked2) 
    
    #def showInventoryPage(self):
    #def showTrackingPage(self):
#This is the function to handle buttons on the Order Schedule Page
    def showOrderSchedulePage(self):
        self.ui_orderSched.setupUi(self)
        # Set current_ui to the current page
        self.current_ui = self.ui_orderSched
        # Create DateTimeUpdater instance and update date/time
        dt_updater = DateTimeUpdater(self.ui_orderSched)
        dt_updater.update()
        # button on overview page to change to overview page
        self.ui_orderSched.pushButton_5.clicked.connect(self.showOverviewPage)
        # button on overview page to change to oee page
        self.ui_orderSched.pushButton_7.clicked.connect(self.showOeePage)
        
        # button on overview page to change to orders page
        self.ui_orderSched.pushButton_14.clicked.connect(self.showNewOrdersPage)
        # button on overview page to change to shift scheduling page
        self.ui_orderSched.pushButton_13.clicked.connect(self.showShiftSchedulePage)
#This is the function to handle buttons on the Shift Schedule Page
    def showShiftSchedulePage(self):
        self.ui_shiftSched.setupUi(self)
        # Set current_ui to the current page
        self.current_ui = self.ui_shiftSched
        # Create DateTimeUpdater instance and update date/time
        dt_updater = DateTimeUpdater(self.ui_shiftSched)
        dt_updater.update()
        # button on overview page to change to overview page
        self.ui_shiftSched.pushButton_5.clicked.connect(self.showOverviewPage)
        # button on overview page to change to oee page
        self.ui_shiftSched.pushButton_7.clicked.connect(self.showOeePage)
        
        # button on overview page to change to orders page
        self.ui_shiftSched.pushButton_14.clicked.connect(self.showNewOrdersPage)
        # button on overview page to change to order scheduling page
        self.ui_shiftSched.pushButton_10.clicked.connect(self.showOrderSchedulePage)
    #def showReportsPage(self):
############################################################################################
# Below is a set of Functions to be Performed based on the GUI Page Listed.
# Overview Page Functions:
    def onDateSelected(self):
        # Get the currently selected date
        selected_date = self.ui_overview.calendarWidget.selectedDate()
        #print(f"Selected Date: {selected_date.toString()}")
        # Write code to access data for the graphical output based on the date clicked*****
    # Function to display the user's full name in the QTextBrowser
    def displayUserFullName(self):
        # Ensure the QTextBrowser exists and is accessible
        if hasattr(self.ui_overview, 'textBrowser'):
            # Set the formatted full name into the textBrowser widget
            self.ui_overview.textBrowser.setPlainText(self.userFullName)
    
    # Function to display the user's role in the QTextBrowser_2
    def displayUserRole(self):
        # Ensure the QTextBrowser_2 exists and is accessible
        if hasattr(self.ui_overview, 'textBrowser_2'):
            # Set the role into the textBrowser_2 widget
            self.ui_overview.textBrowser_2.setPlainText(self.userRole)
# OEE Page Functions:
    def calculateOEE(self):
        # Create an instance of OEECaculator
        self.oee_calculator = OEECaculator()
        # Calculate OEE
        oee = self.oee_calculator.calculateOEE()
        # Use the generate_date_range function
        dates = self.submitButton()
    
        # Debugging: Ensure dates are generated properly
        if not dates:
            print("Error: No dates generated.")
            QMessageBox.warning(self, "Error", "Date range is empty. Please set a valid date range.")
            return
    # ************************ NEEDS TO BE UPDATED WITH DATABASE INFO **************************************
        # Ensure the length of the date list is consistent with the length of the generated arrays
        num_dates = len(dates)
        # Generate values for OEE, Availability, Performance, and Quality between 0 and 100
        oee_values = [random.randint(0, 100) for _ in range(num_dates)]
        availability_values = [random.randint(0, 100) for _ in range(num_dates)]
        performance_values = [random.randint(0, 100) for _ in range(num_dates)]
        quality_values = [random.randint(0, 100) for _ in range(num_dates)]
        # Create an instance of OEEPlotter and plot the data
        oee_plotter = OEEPlotter(self.ui_oee.graphicsView_3)  # Pass graphicsView_3 widget to the plotter
        oee_plotter.plot_oee_data(dates, oee_values, availability_values, performance_values, quality_values)
        # Create an instance of the RejectionPlotter
        rejected_plotter = RejectionPlotter(self.ui_oee.graphicsView_4)
        # Generate values for number of parts rejected
        hourly = [random.randint(0, 20) for _ in range(num_dates)]
        daily = [random.randint(0, 100) for _ in range(num_dates)]
        weekly = [random.randint(0, 500) for _ in range(num_dates)]
        monthly = [random.randint(0, 1000) for _ in range(num_dates)]
        annually = [random.randint(0, 10000) for _ in range(num_dates)]
        # Plot data
        time_intervals = ["Hourly", "Daily", "Weekly", "Monthly", "Annually"]
        rejected_parts = [hourly, daily, weekly, monthly, annually]  # Example data
        rejected_plotter.plot_rejected_parts(time_intervals, rejected_parts)
    # *******************************************************************************************************
    def calculateAvailability(self):
        # Create an instance of OEECaculator
        self.oee_calculator = OEECaculator()
        # Calculate OEE
        oee = self.oee_calculator.calculateAvailability()
    def calculatePerformance(self):
        # Create an instance of OEECaculator
        self.oee_calculator = OEECaculator()
        # Calculate OEE
        oee = self.oee_calculator.calculatePerformance()
    def calculateQuality(self):
        # Create an instance of OEECaculator
        self.oee_calculator = OEECaculator()
        # Calculate OEE
        oee = self.oee_calculator.calculateQuality()
    def submitButton(self):
        # Retrieve the start date from the first QDateTimeEdit widget
        start_date = self.ui_oee.dateTimeEdit.date()
        # Retrieve the end date from the second QDateTimeEdit widget
        end_date = self.ui_oee.dateTimeEdit_2.date()
        # Print out the dates for debugging
        print(f"Start Date (before conversion): {start_date.toString('yyyy-MM-dd')}")
        print(f"End Date (before conversion): {end_date.toString('yyyy-MM-dd')}")
        # Check if the start date is the same as the end date
        if start_date == end_date:
            # If they are the same, show a warning message
            QMessageBox.warning(self, "Invalid Date Range", "Start date cannot be the same as the end date!")
            return  # Exit the function if dates are the same
        # Check if the start date is after the end date
        if start_date > end_date:
            # If the start date is after the end date, show an error message
            QMessageBox.warning(self, "Invalid Date Range", "Start date must be before the end date!")
            return  # Exit the function if the start date is after the end date
        # Initialize an empty list to hold the date range
        date_list = []
        # Generate the list of dates between start_date and end_date
        current_date = start_date
        while current_date < end_date:  # Ensure we only include dates before the end date
            date_list.append(current_date)  # Append QDate object (already in QDate format)
            current_date = current_date.addDays(1)  # Move to the next day
        # Store the dates in the date_range list if valid
        self.date_range = [start_date, end_date]  # Store as QDate objects
        # Show success message
        QMessageBox.information(self, "Success", f"Date range set: {start_date.toString('yyyy-MM-dd')} to {end_date.toString('yyyy-MM-dd')}")
        # Debugging: Ensure date_range is populated correctly
        if self.date_range:
            print(f"Start Date: {self.date_range[0].toString('yyyy-MM-dd')}, End Date: {self.date_range[1].toString('yyyy-MM-dd')}")
        else:
            print("Date range is empty. There was an issue with storing the dates.")
        # Debugging: Print the generated date range (list of QDate objects)
        print("Generated date range (QDate objects):", [date.toString('yyyy-MM-dd') for date in date_list])
        # Return the generated list of QDate objects (between start_date and end_date)
        return date_list
# New Orders Page Functions: (LUCAS)
    def validateNewOrderInputs(self):
        #Validate inputs for creating a new order
        required_fields = [
            self.ui_newOrders.textEdit_11.toPlainText(),  # Order Date
            self.ui_newOrders.textEdit_12.toPlainText(),  # Order Time
            self.ui_newOrders.lineEdit.text(),            # Customer Name
            self.ui_newOrders.lineEdit_9.text()           # Product Number
        ]
    
        if not all(required_fields):
            qtw.QMessageBox.warning(self, "Validation Error", "Please fill out all required fields!")
            return False
        
        # Check if product number is already in use
        product_number = self.ui_newOrders.lineEdit_9.text()
        if self.isProductNumberInUse(product_number):
            qtw.QMessageBox.warning(self, "Validation Error", f"Product Number '{product_number}' is already in use!")
            return False
        
        return True
    
    def isProductNumberInUse(self, product_number):
        # Query database to check if product number is already in use
        try:
            db = DatabaseController()
            db.c.execute("SELECT COUNT(*) FROM Orders WHERE product_number = ?", (product_number,))
            result = db.c.fetchone()
            return result[0] > 0  # Return True if product number exists
        except sqlite3.Error as e:
            print(f"Database error while checking product number: {e}")
            return False
    
    def onOkClicked(self):
        # Validate inputs
        if not self.validateNewOrderInputs():
            return
        # Extract data from GUI
        customer_name = self.ui_newOrders.lineEdit.text()       # Customer Name
        phone_number = self.ui_newOrders.lineEdit_2.text()      # Phone Number
        email = self.ui_newOrders.lineEdit_3.text()             # Email
        shipping_address = self.ui_newOrders.lineEdit_4.text()  # Shipping Address
        billing_address = self.ui_newOrders.lineEdit_5.text()   # Billing Address
        product_number = self.ui_newOrders.lineEdit_9.text()    # Product Number
        product_type = self.ui_newOrders.comboBox.currentText() # Product Type
        upper_color = self.ui_newOrders.comboBox_2.currentText()# Upper Color
        lower_color = self.ui_newOrders.comboBox_3.currentText()# Lower Color
        upper_limit = self.ui_newOrders.lineEdit_8.text()       # Upper Limit
        lower_limit = self.ui_newOrders.lineEdit_10.text()      # Lower Limit
        order_date = self.ui_newOrders.textEdit_11.toPlainText()# Order Date
        order_time = self.ui_newOrders.textEdit_12.toPlainText()# Order Time
        self.insertData(customer_name, phone_number, email, shipping_address, billing_address,
                    product_number, product_type, upper_color, lower_color, upper_limit, lower_limit, order_date, order_time)
        # Database operations    
        
    def insertData(self, customer_name, phone_number, email, shipping_address, billing_address,
               product_number, product_type, upper_color, lower_color, upper_limit, lower_limit, order_date, order_time):
        try:
            db = DatabaseController()
            db.buildTables()
            db.populateCustomers(product_number, customer_name, phone_number, email, shipping_address, billing_address)
            db.conn.commit()
            db.populateOrders(product_number, product_type, upper_color, lower_color, upper_limit, lower_limit, order_date, order_time)
            db.conn.commit()
            print("Data successfully inserted into the database.")
            # Test print Orders/Customers tables
            print("\nCustomers Table:")
            db.c.execute("SELECT * FROM Customers")
            customers = db.c.fetchall()
            for row in customers:
                print(row)
            print("\nOrders Table:")
            db.c.execute("SELECT * FROM Orders")
            orders = db.c.fetchall()
            for row in orders:
                print(row)
            #CPLabCommunication.pending_orders = CPLabCommunication.load_orders(db.c, db.conn)
            #CPLabCommunication.process_orders(CPLabCommunication.pending_orders)
        except sqlite3.Error as e:
            print(f"An error occurred while inserting data: {e}")
            db.conn.rollback()
        
    def onCancelClicked(self):
        #Clear all input fields in the New Orders page
        self.ui_newOrders.textEdit_11.setPlainText("DD/MM/YYYY")  # Order Date
        self.ui_newOrders.textEdit_12.setPlainText("hh:mm:ss")  # Order Time
        self.ui_newOrders.lineEdit.clear()     # Customer Name
        self.ui_newOrders.lineEdit_2.clear()   # Phone Number
        self.ui_newOrders.lineEdit_3.clear()   # Email
        self.ui_newOrders.lineEdit_4.clear()   # Shipping Address
        self.ui_newOrders.lineEdit_5.clear()   # Billing Address
        self.ui_newOrders.lineEdit_9.clear()   # Product Number
        self.ui_newOrders.lineEdit_8.clear()   # Upper Limit
        self.ui_newOrders.lineEdit_10.clear()  # Lower Limit
        self.ui_newOrders.comboBox.setCurrentIndex(0)      # Product Type
        self.ui_newOrders.comboBox_2.setCurrentIndex(0)    # Upper Color
        self.ui_newOrders.comboBox_3.setCurrentIndex(0)    # Lower Color
        pass
# Existing Orders Page Functions: (LUCAS)
    def onOkClicked2(self):
        # Extract product number from the GUI
        product_number = self.ui_existingOrders.lineEdit_9.text()  # Product Number
        try:
            db = DatabaseController()
            if not hasattr(self, 'edit_mode') or not self.edit_mode:
                # First click: Check if the product exists
                query = """
                SELECT c.customer_id, c.name, c.phone_number, c.email, c.shipping_address, c.billing_address,
                    o.product_number, o.product_type, o.upper_color, o.lower_color, o.upper_limit, o.lower_limit,
                    o.order_date, o.order_time
                FROM Customers c
                JOIN Orders o ON c.customer_id = o.customer_id
                WHERE o.product_number = ?
                """
                db.c.execute(query, (product_number,))
                result = db.c.fetchone()
                if result:
                    print("Order found. Populating fields for editing...")
                    # Populate GUI fields with existing data
                    self.ui_existingOrders.lineEdit.setText(result[1])  # Name
                    self.ui_existingOrders.lineEdit_2.setText(result[2])  # Phone Number
                    self.ui_existingOrders.lineEdit_3.setText(result[3])  # Email
                    self.ui_existingOrders.lineEdit_4.setText(result[4])  # Shipping Address
                    self.ui_existingOrders.lineEdit_5.setText(result[5])  # Billing Address
                    self.ui_existingOrders.lineEdit_9.setText(result[6])  # Product Number
                    self.ui_existingOrders.comboBox.setCurrentText(result[7])  # Product Type
                    self.ui_existingOrders.comboBox_2.setCurrentText(result[8])  # Upper Color
                    self.ui_existingOrders.comboBox_3.setCurrentText(result[9])  # Lower Color
                    self.ui_existingOrders.lineEdit_8.setText(result[10])  # Upper Limit
                    self.ui_existingOrders.lineEdit_10.setText(result[11])  # Lower Limit
                    self.ui_existingOrders.textEdit_7.setPlainText(result[12])  # Order Date
                    self.ui_existingOrders.textEdit_10.setPlainText(result[13])  # Order Time
                    # Save customer_id for later updates
                    self.current_customer_id = result[0]
                    # Enable edit mode
                    self.edit_mode = True
                    print("Edit mode enabled. Modify fields and click OK again to save changes.")
                else:
                    qtw.QMessageBox.warning(self, "Validation Error", "Product number not found!")
                    print("Product number not found!")
            else:
                # Second click: Update database with new information
                print("Updating existing order and customer...")
                # Extract data from GUI
                customer_name = self.ui_existingOrders.lineEdit.text()  # Name
                phone_number = self.ui_existingOrders.lineEdit_2.text()  # Phone Number
                email = self.ui_existingOrders.lineEdit_3.text()  # Email
                shipping_address = self.ui_existingOrders.lineEdit_4.text()  # Shipping Address
                billing_address = self.ui_existingOrders.lineEdit_5.text()  # Billing Address
                product_type = self.ui_existingOrders.comboBox.currentText()  # Product Type
                upper_color = self.ui_existingOrders.comboBox_2.currentText()  # Upper Color
                lower_color = self.ui_existingOrders.comboBox_3.currentText()  # Lower Color
                upper_limit = self.ui_existingOrders.lineEdit_8.text()  # Upper Limit
                lower_limit = self.ui_existingOrders.lineEdit_10.text()  # Lower Limit
                order_date = self.ui_existingOrders.textEdit_7.toPlainText()  # Order Date
                order_time = self.ui_existingOrders.textEdit_10.toPlainText()  # Order Time
                # Update database with new info
                db.updateCustomerAndOrder(
                    product_number, customer_name, phone_number, email, shipping_address, billing_address,
                    product_type, upper_color, lower_color, upper_limit, lower_limit, order_date, order_time
                )
                db.conn.commit()
                print("Order successfully updated.")
                qtw.QMessageBox.information(self, "Update Successful", "Order and customer information updated.")
                # Test print Orders/Customers tables
                print("\nCustomers Table:")
                db.c.execute("SELECT * FROM Customers")
                customers = db.c.fetchall()
                for row in customers:
                    print(row)
                print("\nOrders Table:")
                db.c.execute("SELECT * FROM Orders")
                orders = db.c.fetchall()
                for row in orders:
                    print(row)
                # Reset edit mode
                self.edit_mode = False
        except sqlite3.Error as e:
            print(f"Database error: {e}")
    def onCancelClicked2(self):
        #Clear all input fields in the New Orders page
        self.ui_existingOrders.textEdit_7.setPlainText("DD/MM/YYYY")  # Order Date
        self.ui_existingOrders.textEdit_10.setPlainText("hh:mm:ss")  # Order Time
        self.ui_existingOrders.lineEdit.clear()     # Customer Name
        self.ui_existingOrders.lineEdit_2.clear()   # Phone Number
        self.ui_existingOrders.lineEdit_3.clear()   # Email
        self.ui_existingOrders.lineEdit_4.clear()   # Shipping Address
        self.ui_existingOrders.lineEdit_5.clear()   # Billing Address
        self.ui_existingOrders.lineEdit_9.clear()   # Product Number
        self.ui_existingOrders.lineEdit_8.clear()   # Upper Limit
        self.ui_existingOrders.lineEdit_10.clear()  # Lower Limit
        self.ui_existingOrders.comboBox.setCurrentIndex(0)      # Product Type
        self.ui_existingOrders.comboBox_2.setCurrentIndex(0)    # Upper Color
        self.ui_existingOrders.comboBox_3.setCurrentIndex(0)    # Lower Color
        self.edit_mode = False
        print("Update cancelled")
# Orders Schedule Page Functions:
# Shift Schedule Page Functions:
# Shift Schedule Page Functions:
    def submitShift(self):
        shifts = {"Morning": (6, 14), "Afternoon": (14, 22), "Night": (22, 6)}
        schedule = []
        firstName = self.ui_shiftSched.lineEdit.text()
        lastName = self.ui_shiftSched.lineEdit_2.text()
        employeeNumber = self.ui_shiftSched.lineEdit_3.text()
        maxHours = int(self.ui_shiftSched.lineEdit_4.text())
        minHours = int(self.ui_shiftSched.lineEdit_5.text())
        start_date = self.ui_shiftSched.dateTimeEdit.date()
        end_date = self.ui_shiftSched.dateTimeEdit_2.date()
        print("First Name: " + firstName)
        print("Last Name: " + lastName)
        print("Employee Number: " + employeeNumber)
        print("Max Hours: " + maxHours)
        print("Min Hours: " + minHours)
        # Convert dates to datetime objects
        start_date = datetime.strptime(start_date, "%Y-%m-%d")
        end_date = datetime.strptime(end_date, "%Y-%m-%d")
        try:
            db = DatabaseController()
            db.buildTables()
            db.populateShifts(firstName, lastName, employeeNumber, maxHours, minHours, start_date, end_date)
            db.conn.commit()
            print("Data successfully inserted into the database.")
            # Test print Orders/Customers tables
            print("\nShift Schedule Table:")
            db.c.execute("SELECT * FROM ShiftSchedule")
            customers = db.c.fetchall()
            for row in customers:
                print(row)
            
        except sqlite3.Error as e:
            print(f"An error occurred while inserting data: {e}")
            db.conn.rollback()
    def updateShifts(firstName, lastName, employeeNumber, maxHours, minHours, start_date, end_date):
        # Function will update the figure in the Shift Schedule window to display the shifts
        # Get data
        # Format data
        # Display data
        return
if __name__ == '__main__':
# MAIN COMMUNICATION LOOP ############################################################################################
    # Connect to the database
    db = DatabaseController()
    db.buildTables()
    '''db.populateCustomers(1, 'Seth', 1, "seth", 'shipping_address', 'billing_address')
    db.populateCustomers(2, 'Seth', 1, "seth", 'shipping_address', 'billing_address')
    db.populateCustomers(3, 'Seth', 1, "seth", 'shipping_address', 'billing_address')
    db.populateCustomers(4, 'Seth', 1, "seth", 'shipping_address', 'billing_address')
    db.populateCustomers(5, 'Seth', 1, "seth", 'shipping_address', 'billing_address')
    db.populateOrders(1, 'Phone', 'Red', 'Red', '2', '1', 'DDMMYYYY', 'DDMMYYYY')
    db.populateOrders(2, 'Phone', 'Blue', 'Red', '2', '1', 'DDMMYYYY', 'DDMMYYYY')
    db.populateOrders(3, 'Phone', 'Purple', 'Red', '2', '1', 'DDMMYYYY', 'DDMMYYYY')
    db.populateOrders(4, 'Phone', 'White', 'Red', '2', '1', 'DDMMYYYY', 'DDMMYYYY')
    db.populateOrders(5, 'Phone', 'Black', 'Red', '2', '1', 'DDMMYYYY', 'DDMMYYYY')'''
# MAIN COMMUNICATION LOOP END ########################################################################################
    app = qtw.QApplication([])
    widget = MANF455_Widget()
    widget.show()
    app.exec_()
