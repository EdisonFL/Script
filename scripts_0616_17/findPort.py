import json
import re
import serial
import subprocess

ioreg_output = subprocess.check_output(['ioreg', '-Src', 'IOUSBDevice']).decode('utf-8')
usb_devices = re.split(' }', ioreg_output)

for device in usb_devices:
    location_id_match = re.search(r'"locationID" = (\w+)', device)
    sn_match = re.search(r'"USB Serial Number" = "(\w+)"', device)
    if location_id_match:
        print(location_id_match.group(1))
    if sn_match:
        print(sn_match.group(1))

