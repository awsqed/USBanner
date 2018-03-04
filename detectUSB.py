import re, sys, os
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
				print type(device.get('ID_VENDOR_ID'))
				dev = usb.core.find(idVendor=device.get('ID_VENDOR_ID'), idProduct=device.get('ID_MODEL_ID'))
				for cfg in dev:
					for i in cfg:
						print i.bInterfaceClass # Get interface class , Mass storage will equal to 8
				with open("test/logs/add.log","a+") as f:
					f.write('VendorID: {0} , ModelID: {1} connected\n'.format(device.get('ID_VENDOR_ID'), device.get('ID_MODEL_ID')))
		if device.action == 'remove':
			with open("test/logs/remove.log","a+") as f:
				if None != device.get('ID_VENDOR_ID'):
					f.write('VendorID: {0} , ModelID: {1} disconnected\n'.format(device.get('ID_VENDOR_ID'), device.get('ID_MODEL_ID')))
		
event_handle()


