#!/usr/bin/python3

import subprocess
from shutil import which
import sys


class BTdevice():
    def __init__(self, name, mac):
        self.name = name
        self.mac = mac

    def getProperties(self):
        return self.name, self.mac


# Helper function to handle sending command and handle the result
def msghandler(args):
    (message, _) = subprocess.Popen(args,stdout=subprocess.PIPE).communicate()
    return message.decode('utf-8')

# List of devices, earlier device will be check first.
# So for performance reason place more common devices first,
# allowing the execution to terminated earlier.

bt_devices = [BTdevice(name='XM3', mac='CC:98:8B:4A:07:31')]

def main(argv):
    if len(argv) == 0:
        # Print connected device
        if which("bluetoothctl") is not None:
            bt_connected = "no"
            for dev in bt_devices:
                name, mac = dev.getProperties()
                cmd_bt_connected = 'bluetoothctl info ' + mac + ' | grep -i connected | awk \'{print $2}\''
                t = subprocess.Popen([cmd_bt_connected], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
                bt_connected = t.stdout.read().decode('utf-8').strip('\n')
                if bt_connected == "yes":
                    print(name)
                    break
            if bt_connected == "no":
                print("None")
        else:
            print("bluetoothctl missing")

    else:
        # Click detected, handle input

        # If connected, we want to disconnect and if successful we might
        # as well turn off the bluetooth controller since we won't use it.
        message = msghandler(['bluetoothctl', 'disconnect'])
        if "Successful disconnected" in message:
            msghandler(['bluetoothctl', 'power', 'off'])
            exit()

        # If disconnected, we want to make sure the controller is turned on
        # and then try to connect the device.
        # This is a bit slow but it does the job.
        msghandler(['bluetoothctl', 'power', 'on'])
        for dev in bt_devices:
            (_, mac) = dev.getProperties()
            message = msghandler(['bluetoothctl', 'connect', mac])
            if "Connection successful" in message:
                exit()


if __name__ == "__main__":
    main(sys.argv[1:])
