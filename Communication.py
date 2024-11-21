import time
from datetime import datetime
from PLCCommunications import PLCCommunicator
from Orders import Order, Status

# Constants
SERVER_ADDR = 'opc.tcp://172.21.10.1:4840'
RFID_READ_DONE_TAG = 'ns=3;s="RFID_control"."read_done"'
CARRIER_ID_TAG = 'ns=3;s="identData"."readData"[0]'
RFID_WRITE_TAG = 'ns=3;s="RFID_control"."write"'
RFID_WRITE_DONE_TAG = 'ns=3;s="RFID_control"."write_done"'
RFID_WRITE_DATA_TAG = 'ns=3;s="identData"."writeData"'
TASK_CODE_TAG = 'ns=3;s="abstractMachine"."task code"'

# Global state for RFID tag presence
presence = False

# Callback for RFID tag read completion
def rfid_read_done_cb(value):
    global presence
    if value:
        print("RFID tag read complete.")
        presence = True

# Function to get active employees from ShiftSchedules table
def get_active_employees(cursor, current_time):
    """Retrieve employees scheduled to work at the current time."""
    cursor.execute("""
    SELECT employee_id, name FROM ShiftSchedules
    WHERE ? BETWEEN start_time AND end_time
    """, (current_time,))
    return cursor.fetchall()

# Main processing loop
def process_orders(cursor, conn, pending_orders):
    global presence

    # Initialize PLC communication
    comms = PLCCommunicator(SERVER_ADDR)
    comms.connect()
    comms.subscribe_tag(RFID_READ_DONE_TAG, rfid_read_done_cb)

    completed_orders = []

    try:
        while len(pending_orders) > 0:
            # Fetch the current time
            current_time = datetime.now()

            # Check for active employees
            active_employees = get_active_employees(cursor, current_time)
            if not active_employees:
                print("No active employees available for this shift. Waiting...")
                time.sleep(60)  # Wait for 1 minute and retry
                continue

            # Assign the order to an active employee
            assigned_employee = active_employees[0]  # Simple round-robin logic
            print(f"Assigning order to employee: {assigned_employee[1]} (ID: {assigned_employee[0]})")

            # Pop the next order from the queue
            current_order = pending_orders.pop(0)

            # Update the order in the database with assigned employee
            cursor.execute("""
            UPDATE Orders SET status = ?, assigned_to = ?
            WHERE order_id = ?
            """, (Status.IN_PROGRESS.value, assigned_employee[0], current_order.orderID))
            conn.commit()

            # Process the order with the PLC
            current_order.initiateOrder(
                comms,
                CARRIER_ID_TAG,
                RFID_WRITE_DATA_TAG,
                RFID_WRITE_TAG,
                RFID_WRITE_DONE_TAG,
                cursor
            )

            # Mark order as completed in the database
            cursor.execute("""
            UPDATE Orders SET status = ? WHERE order_id = ?
            """, (Status.COMPLETED.value, current_order.orderID))
            conn.commit()

            # Log completed order
            completed_orders.append(current_order)
            print(f"Order {current_order.orderID} completed and assigned to {assigned_employee[1]}")
            presence = False  # Reset presence after processing

    except KeyboardInterrupt:
        print("Shutting down order processing...")
    finally:
        comms.disconnect()

# Main execution
if __name__ == "__main__":
    import sqlite3

    # Connect to the database
    conn = sqlite3.connect("MES.db")
    cursor = conn.cursor()

    # Example: Define pending orders (these would typically be loaded from the database)
    pending_orders = [
        Order(101, 1, None),
        Order(102, 2, None),
        Order(103, 3, None)
    ]

    # Process orders
    process_orders(cursor, conn, pending_orders)

    # Close the database connection
    conn.close()
