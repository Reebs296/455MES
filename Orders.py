import time
from enum import Enum
from PLCCommunications import PLCCommunicator
from datetime import datetime

class Status(Enum):
    QUEUED = "Queued"
    IN_PROGRESS = "In Progress"
    COMPLETED = "Completed"
    FAILED = "Failed"

class Ordertype(Enum):
    PROD = 'production'
    CSTM = 'customer'

class Order:
    def __init__(self, orderID, taskCode, ordertype,startTime=None):
        self.orderID = orderID
        self.taskCode = taskCode
        self.startTime = startTime
        self.finishTime = None
        self.status = Status.QUEUED
        self.ordertype = ordertype

    def initiateOrder(self, plc_comm, carrier_tag, rfid_write_data_tag, rfid_write_tag, rfid_write_done_tag):
            # Build data packet: [CarrierID, OrderID] + [0]*30
            dataPacket = [0] * 32
            carrier_id = plc_comm.read_tag(carrier_tag)
            dataPacket[0] = carrier_id
            dataPacket[1] = self.orderID

            # Write data packet to RFID
            plc_comm.write_tag(rfid_write_data_tag, dataPacket)
            plc_comm.write_tag(rfid_write_tag, True)

            # Wait for write to complete
            while not plc_comm.read_tag(rfid_write_done_tag):
                print("Waiting for RFID writing to complete.")
                time.sleep(1)
            plc_comm.write_tag(rfid_write_tag, False)
            print("RFID writing to complete.")
            print(f"Initiated order with Carrier ID {carrier_id} and Order ID {self.orderID}")
            self.status = Status.IN_PROGRESS

    def save_to_database(self, cursor):
        cursor.execute("""
        INSERT INTO Orders (order_id, product_details, priority, status, customer_id)
        VALUES (?, ?, ?, ?, ?)
        """, (self.orderID, "Task Code: " + str(self.taskCode), 1, self.status.value, None))


    def sendOrderInformation(self, plc_comm, task_code_tag):
        plc_comm.write_tag(task_code_tag, self.taskCode)

def rfid_read_done_cb(tag_name, value):
    global presence
    presence = True
    print(f"Tag '{tag_name}' changed to : {value}(DEC) - > {str(hex(value))}(HEX)")

if __name__ == "__main__":
    order = Order(101, 1)
    # Define MES server address and client configuration
    SERVER_ADDR = 'opc.tcp://172.21.10.1:4840'
    RFID_READ_DONE_TAG = 'ns=3;s="RFID_control"."read_done"'
    CARRIER_ID_TAG = 'ns=3;s="identData"."readData"[0]'
    RFID_WRITE_TAG = 'ns=3;s="RFID_control"."write"'
    RFID_WRITE_DONE_TAG = 'ns=3;s="RFID_control"."write_done"'
    RFID_WRITE_DATA_TAG = 'ns=3;s="identData"."writeData"'
    TASK_CODE_TAG = 'ns=3;s="abstractMachine"."task code"'

    presence = False

    comms = PLCCommunicator(SERVER_ADDR)
    comms.connect()

    comms.subscribe_tag(RFID_READ_DONE_TAG, rfid_read_done_cb)

    try:
        while True:
            if presence:
                order.initiateOrder(comms, CARRIER_ID_TAG, RFID_WRITE_DATA_TAG, RFID_WRITE_TAG, RFID_WRITE_DONE_TAG)
                order.sendOrderInformation(comms, TASK_CODE_TAG)
                presence = False
            time.sleep(1)
    except KeyboardInterrupt:
        print("Shutting down OPC-UA client...")
    finally:
        comms.disconnect()