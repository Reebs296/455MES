import time
from CPLab_PLC_Communication import PLC_comm
from CPLabOrders import Order, Status, Ordertype
from DatabaseController import DatabaseController

# Define MES server address and client configuration
SERVER_ADDR = 'opc.tcp://172.21.10.1:4840'
RFID_READ_DONE_TAG = 'ns=3;s="abstractMachine"."read_complete"'
CARRIER_ID_TAG = 'ns=3;s="identData"."readData"[0]'
ORDER_ID_TAG = 'ns=3;s="identData"."readData"[1]'
RFID_WRITE_TAG = 'ns=3;s="RFID_control"."write"'
RFID_WRITE_DONE_TAG = 'ns=3;s="RFID_control"."write_done"'
RFID_WRITE_DATA_TAG = 'ns=3;s="identData"."writeData"'
TASK_CODE_TAG = 'ns=3;s="abstractMachine"."task code"'
EXEC_ORDER_TAG = 'ns=3;s="abstractMachine"."exec_order"'
ORDER_COMPLETE_TAG = 'ns=3;s="abstractMachine"."order_complete"'

# Initialize global variable for RFID read completion presence
global presence
pending_orders = []

def rfid_read_done_cb(tag_name, value):
    global presence
    if value:
        presence = True
    print(f"Tag '{tag_name}' changed to : {value}")

def load_orders(cursor, conn):

    cursor.execute(""" SELECT product_number, upper_color FROM Orders""")
    temp_list = cursor.fetchall()
    pending_orders = []

    for order in temp_list:

        if order[1] == 'Red' or 'Black': taskCode = 1
        elif order[1] == 'Blue' or 'Grey': taskCode = 2
        else: taskCode == -1

        temp_order = Order(int(order[0]), taskCode, None)

        pending_orders.append(temp_order)

    return pending_orders

def process_orders(pending_orders):

    global presence
    presence = False

    pending_order_ids = [int(order.orderID) for order in pending_orders]
    print(f"Pending orders ids: {pending_order_ids}")
    completed_orders = []
    comms = PLC_comm(SERVER_ADDR)
    
    comms.connect()
    comms.subscribe_tag(RFID_READ_DONE_TAG, rfid_read_done_cb)

    try:
        while pending_orders:  # Continue until the orders list is empty

            if presence:
                presence = False
                print('Pallet detected at the RFID reader.')

                current_order_id = int(comms.read_tag(ORDER_ID_TAG))
                print(f"Current OrderID:{current_order_id}")
                print(f"Pending orders ids: {pending_order_ids}")
                if current_order_id  in pending_order_ids:
                    print(f" Current orderID : {current_order_id} is in pending orders")
                    # current_order = pending_orders.pop(0)
                    current_order = next(order for order in pending_orders if order.orderID == current_order_id)
                    pending_orders.remove(current_order)
                    pending_order_ids.remove(current_order_id)
                    print(f"Pending orders ids after popping: {pending_order_ids}")

                    while current_order.status is not Status.COMPLETED:
                        # Pop the first order from the list
                        current_order.initiateOrder(comms, CARRIER_ID_TAG, RFID_WRITE_DATA_TAG, RFID_WRITE_TAG, RFID_WRITE_DONE_TAG)
                        if current_order.ordertype is Ordertype.PROD or Ordertype.CSTM:
                            current_order.sendOrderInformation(comms, TASK_CODE_TAG)
                            while comms.read_tag(TASK_CODE_TAG) != current_order.taskCode:
                                time.sleep(1)
                            print(f"Task code {current_order.taskCode} confirmed by PLC.")
                            comms.write_tag(EXEC_ORDER_TAG,True)
                            current_order.startTime = time.time()

                            while comms.read_tag(ORDER_COMPLETE_TAG) != True:
                                time.sleep(0.5)

                            current_order.status = Status.COMPLETED
                            completed_orders.append(current_order)
                            current_order.finishTime = time.time()

                else:
                        print(f" Current orderID : {current_order_id} is NOT in pending orders")
                        comms.write_tag(TASK_CODE_TAG, -1)
                        while comms.read_tag(TASK_CODE_TAG) != -1:
                            time.sleep(1)
                        print(f"Task code {-1} confirmed by PLC.")
                        comms.write_tag(EXEC_ORDER_TAG,True)
            time.sleep(1)
        print("All orders Completed")
        [print(completed_order)for completed_order in completed_orders]

    except KeyboardInterrupt:
        print("Shutting down OPC-UA client...")
    
    finally:
        comms.disconnect()

if __name__ == '__main__':

    pending_orders = None

    db = DatabaseController()
    db.buildTables()

    while True:

        pending_orders = load_orders(db.c, db.conn)

        if len(pending_orders) != 0: 

            process_orders(pending_orders)

    