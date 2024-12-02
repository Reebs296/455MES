# command to install QtDesigner: pip install PyQt5Designer
# command to create Python UI library: pyuic5 -o <UiLibraryName> <UiFileName>

from loginWindow import Ui_MainWindow
from overviewWindow import Ui_MainWindow as Ui_Overview
from oeeWindow import Ui_MainWindow as Ui_Oee
from newOrdersWindow import Ui_MainWindow as Ui_NewOrders
from existingOrdersWindow import Ui_MainWindow as Ui_ExistingOrders
from orderScheduleWindow import Ui_MainWindow as Ui_OrderSchedule
from shiftScheduleWindow import Ui_MainWindow as Ui_ShiftSchedule

from PyQt5 import QtWidgets as qtw
from PyQt5 import QtCore as qtc

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

        # launch login page
        self.ui.setupUi(self)

        # Connect the Enter button to the checkCredentials method
        self.ui.Enter.clicked.connect(self.checkCredentials)

    def checkCredentials(self):
        # Define valid credentials
        credentials = {
            "Worker": "1234",
            "MaintenanceStaff": "1234",
            "QualityControl": "1234",
            "Management": "1234",
        }

        # Get entered username and password
        username = self.ui.username.text()
        password = self.ui.password.text()

        # Check if the entered credentials match any valid user type
        if username in credentials and credentials[username] == password:
            # Assign login type and show success message
            login_type = username  # The username corresponds to the login type
            qtw.QMessageBox.information(self, "Login Status", f"Login Successful\nUser Type: {login_type}")

            # launch overview page
            self.showOverviewPage()

        else:
            # Show denied message for invalid credentials
            qtw.QMessageBox.warning(self, "Login Status", "Denied!")

    def showOverviewPage(self):
        self.ui_overview.setupUi(self)

        # button on overview page to change to oee page
        self.ui_overview.pushButton_7.clicked.connect(self.showOeePage)
        
        # button on overview page to change to orders page
        self.ui_overview.pushButton_14.clicked.connect(self.showNewOrdersPage)

        # button on overview page to change to order scheduling page
        self.ui_overview.pushButton_10.clicked.connect(self.showOrderSchedulePage)

        # button on overview page to change to shift scheduling page
        self.ui_overview.pushButton_13.clicked.connect(self.showShiftSchedulePage)


    def showOeePage(self):
        self.ui_oee.setupUi(self)

        # button on overview page to change to overview page
        self.ui_oee.pushButton_5.clicked.connect(self.showOverviewPage)
        
        # button on overview page to change to orders page
        self.ui_oee.pushButton_14.clicked.connect(self.showNewOrdersPage)

        # button on overview page to change to order scheduling page
        self.ui_oee.pushButton_10.clicked.connect(self.showOrderSchedulePage)

        # button on overview page to change to shift scheduling page
        self.ui_oee.pushButton_13.clicked.connect(self.showShiftSchedulePage)



    def showNewOrdersPage(self):
        self.ui_newOrders.setupUi(self)

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

    def showExistingOrdersPage(self):
        self.ui_existingOrders.setupUi(self)

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
    
    #def showInventoryPage(self):

    #def showTrackingPage(self):

    def showOrderSchedulePage(self):
        self.ui_orderSched.setupUi(self)

        # button on overview page to change to overview page
        self.ui_orderSched.pushButton_5.clicked.connect(self.showOverviewPage)

        # button on overview page to change to oee page
        self.ui_orderSched.pushButton_7.clicked.connect(self.showOeePage)
        
        # button on overview page to change to orders page
        self.ui_orderSched.pushButton_14.clicked.connect(self.showNewOrdersPage)

        # button on overview page to change to shift scheduling page
        self.ui_orderSched.pushButton_13.clicked.connect(self.showShiftSchedulePage)

    def showShiftSchedulePage(self):
        self.ui_shiftSched.setupUi(self)

        # button on overview page to change to overview page
        self.ui_shiftSched.pushButton_5.clicked.connect(self.showOverviewPage)

        # button on overview page to change to oee page
        self.ui_shiftSched.pushButton_7.clicked.connect(self.showOeePage)
        
        # button on overview page to change to orders page
        self.ui_shiftSched.pushButton_14.clicked.connect(self.showNewOrdersPage)

        # button on overview page to change to order scheduling page
        self.ui_shiftSched.pushButton_10.clicked.connect(self.showOrderSchedulePage)

    #def showReportsPage(self):

if __name__ == '__main__':
    app = qtw.QApplication([])

    widget = MANF455_Widget()
    widget.show()

    app.exec_()
