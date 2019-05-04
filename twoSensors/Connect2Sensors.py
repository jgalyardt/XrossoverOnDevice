# Search for BLE UART devices and list all that are found.
# Author: Tony DiCola
import atexit
import time
import Adafruit_BluefruitLE
import time
import json
import atexit
from Adafruit_BluefruitLE.services import UART
import threading
# Get the BLE provider for the current platform.
ble = Adafruit_BluefruitLE.get_provider()


# Main function implements the program logic so it can run in a background
# thread.  Most platforms require the main thread to handle GUI events and other
# asyncronous events like BLE actions.  All of the threading logic is taken care
# of automatically though and you just need to provide a main function that uses
# the BLE provider.
def main():
    # Clear any cached data because both bluez and CoreBluetooth have issues with
    # caching data and it going stale.
    ble.clear_cached_data()

    # Get the first available BLE network adapter and make sure it's powered on.
    adapter = ble.get_default_adapter()
    adapter.power_on()
    print('Using adapter: {0}'.format(adapter.name))
    
    print('Disconnecting any connected UART devices...')
    UART.disconnect_devices()
    
    # Start scanning with the bluetooth adapter.
    adapter.start_scan()
    # Use atexit.register to call the adapter stop_scan function before quiting.
    # This is good practice for calling cleanup code in this main function as
    # a try/finally block might not be called since this is a background thread.
    atexit.register(adapter.stop_scan)
    print('Searching for UART devices...')
    print('Press Ctrl-C to quit (will take ~30 seconds on OSX).')
    # Enter a loop and print out whenever a new UART device is found.
    known_uarts = set()
    new = []
    while len(known_uarts) < 2:
        found = set(UART.find_devices())
        # Check for new devices that haven't been seen yet and print out
        # their name and ID (MAC address on Linux, GUID on OSX).
        new = found - known_uarts
        for device in new:
            print('Found UART: {0} [{1}]'.format(device.name, device.id))
        known_uarts.update(new)
        # Sleep for a second and see if new devices have appeared.
        time.sleep(1.0)
    
    count = 0
    
    dThreads = [0, 0]

    for device in known_uarts:
        print("Connecting")
        device.connect()
        print('Discovering')
        UART.discover(device)
        time.sleep(5)
        dThreads[count] = threading.Thread(target=readData, args=(device,count,))
        dThreads[count].start()
        time.sleep(10)
        count += 1

def readData(device, threadNum):
    uart = UART(device)
    print('Thread ' + str(threadNum) + ' has been started')
    # Write a string to the TX characteristic.
    uart.write(b'Hello world!\r\n')
    print("Sent 'Hello world!' to the device.")
    # Now wait up to one minute to receive data from the device.
    print('Waiting up to 60 seconds to receive data from the device...')
    
    with open('data' + str(threadNum) + '.txt', 'w') as outfile:
        print('Reading from device...')
        while True:
            received = uart.read(timeout_sec=60)
            if received is not None:
                # Received data, print it out.
                #print('Received: {0}'.format(received))
                outfile.write(str(received))
            else:
                # Timeout waiting for data, None is returned.
                print('Received no data!')


# Initialize the BLE system.  MUST be called before other BLE calls!
ble.initialize()

# Start the mainloop to process BLE events, and run the provided function in
# a background thread.  When the provided main function stops running, returns
# an integer status code, or throws an error the program will exit.
ble.run_mainloop_with(main)

