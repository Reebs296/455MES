from opcua import Client, ua
import time
import os

class SubHandler(object):

    def __init__(self, callback, tag_name,triggered=False):
        self.callback = callback
        self.tag_name = tag_name
        self.triggered = triggered

    def datachange_notification(self, node, val, data):
        self.callback(self.tag_name, val) 
        self.triggered = True
        # print("Handler process ID:", os.getpid()) 

class PLC_comm:
    def __init__(self, server_addr):
        self.server_addr = server_addr
        self.client = None
        self.subscribed_tags = {}
        self.tag_callbacks = {}
        self.handlers = []
        self.handles = []
        self.subscriptions = []

    def connect(self):
        try:
            self.client = Client(self.server_addr)
            self.client.connect()
            print(" INFO : Connected to OPC-UA server at", self.server_addr)
        except Exception as e:
            print(" INFO : Failed to connect to OPC-UA server:", e)

    def subscribe_tag(self, tag_name, callback):
        try:
            node = self.client.get_node(tag_name)
            handler = SubHandler(callback, tag_name)
            subscription = self.client.create_subscription(500, handler)
            handle = subscription.subscribe_data_change(node)
            
            # Store tag, handler, and handle for management
            self.tag_callbacks[tag_name] = callback
            self.subscribed_tags[tag_name] = None  # Initialize the tag's value as None
            self.subscriptions.append(subscription)
            self.handlers.append(handler)
            self.handles.append(handle)
            print(f" INFO : Subscribed to tag '{tag_name}' with callback.")
        except Exception as e:
            print(f" INFO : Failed to subscribe to tag '{tag_name}':", e)

    def write_tag(self, tag_name, value):
        try:
            node = self.client.get_node(tag_name)
            node.set_value(ua.DataValue(ua.Variant(value, node.get_data_type_as_variant_type())))
            print(f" INFO : Written value '{value}' to tag '{tag_name}'.")
        except Exception as e:
            print(f" INFO : Failed to write to tag '{tag_name}':", e)

    def read_tag(self, tag_name):
        try:
            node = self.client.get_node(tag_name)
            value = node.get_value()
            self.subscribed_tags[tag_name] = value  # Update attribute dictionary with the latest value
            print(f" INFO : Read value '{value}' from tag '{tag_name}'.")
            return value
        except Exception as e:
            print(f" INFO : Failed to read tag '{tag_name}':", e)
            return None

    def disconnect(self):
        """Closes subscriptions and disconnects the OPC-UA client."""
        try:
            # Gracefully close all subscriptions before disconnecting
            for sub in self.subscriptions:
                try:
                    sub.unsubscribe(self.handles.pop())  # Unsubscribe handle from subscription
                    sub.delete()  # Explicitly delete each subscription
                    print(" INFO : Subscription deleted.")
                except Exception as e:
                    print(" INFO : Error deleting subscription:", e)

            # Disconnect from the client
            if self.client:
                self.client.disconnect()
                print(" INFO : Disconnected from OPC-UA server")
        except Exception as e:
            print(" INFO : Error during disconnect:", e)

if __name__ == "__main__":
    SERVER_ADDR = 'opc.tcp://172.21.10.1:4840'
    comms = PLC_comm(SERVER_ADDR)
    
    def example_callback(tag_name, value):
        print(f" INFO : Tag '{tag_name}' changed to {value}")
        # print("Callback process ID:", os.getpid())  

    comms.connect()
    comms.subscribe_tag('ns=3;s="conv_start"', example_callback)
    comms.subscribe_tag('ns=3;s="Data_block_1"."var1"', example_callback)
    toggle = True
    try:
        while True:
            time.sleep(2)
            toggle = not toggle
            print(toggle)
            comms.write_tag('ns=3;s="Data_block_1"."var1"', toggle)
    except KeyboardInterrupt:
        print("Shutting down OPC-UA client...")
    finally:
        comms.disconnect()

