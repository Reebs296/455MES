import time
from enum import Enum
from CPLab_PLC_Communication import PLC_comm
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
    def __str__(self):
            start_time_str = (
                datetime.fromtimestamp(self.startTime).strftime('%Y-%m-%d %H:%M:%S')
                if self.startTime else "Not Started"
            )
            finish_time_str = (
                datetime.fromtimestamp(self.finishTime).strftime('%Y-%m-%d %H:%M:%S')
                if self.finishTime else "Not Completed"
            )
            
            # Calculate the duration in seconds if both start and finish times are available
            duration_str = (
                f"{(self.finishTime - self.startTime):.2f} seconds"
                if self.startTime and self.finishTime else "N/A"
            )

            return (
                f"--------"
                f"Order ID: {self.orderID}"
                f"--------\n"

                f"\tTask Code: {self.taskCode}\n"
                f"\tOrder Type: {self.ordertype.name}\n"
                f"\tStatus: {self.status.name}\n"
                f"\tStart Time: {start_time_str}\n"
                f"\tFinish Time: {finish_time_str}\n"
                f"\tDuration: {duration_str}"
            )
    def initiateOrder(self, plc_comm, carrier_tag, rfid_write_data_tag, rfid_write_tag, rfid_write_done_tag):
        print("Order Init.")
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


    def sendOrderInformation(self, plc_comm, task_code_tag):
        print("Sending Machine Parameters")
        plc_comm.write_tag(task_code_tag, self.taskCode)
        print(f"Task code {self.taskCode} written to PLC.")


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

    comms = PLC_comm(SERVER_ADDR)
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
