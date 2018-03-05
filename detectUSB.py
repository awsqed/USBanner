import re, sys, os, datetime
import subprocess
import pyudev
import usb.core, usb.util


def event_handle():
	context = pyudev.Context()
	monitor = pyudev.Monitor.from_netlink(context)
	monitor.filter_by(subsystem='usb')
	for device in iter(monitor.poll, None):
		if device.action == 'add':
			# idVendor and idProduct will be hex
			if None != device.get('ID_VENDOR_ID'):
				dev = usb.core.find(idVendor=int(device.get('ID_VENDOR_ID'),16), idProduct=int(device.get('ID_MODEL_ID'),16))
				for cfg in dev:
					for i in cfg:
						if i.bInterfaceClass == 8: # Get interface class , Mass storage will equal to 8
							with open("test/logs/add.log","a+") as f:
								f.write('{0}| INFO | VendorID: {1} , ModelID: {2} connected, Is Mass storage: Yes.\n'.format(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),device.get('ID_VENDOR_ID'), device.get('ID_MODEL_ID')))
								f.close()
						else:
							with open("test/logs/add.log","a+") as f:
								f.write('{0}| INFO | VendorID: {1} , ModelID: {2} connected, Is Mass storage: No.\n'.format(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),device.get('ID_VENDOR_ID'), device.get('ID_MODEL_ID')))
								f.close()
		if device.action == 'remove':
			with open("test/logs/remove.log","a+") as f:
				if None != device.get('ID_VENDOR_ID'):
					f.write('{0}| INFO | VendorID: {1} , ModelID: {2} disconnected.\n'.format(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),device.get('ID_VENDOR_ID'), device.get('ID_MODEL_ID')))
					f.close()
		
event_handle()


