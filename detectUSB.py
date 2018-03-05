import re, sys, os, datetime, time
import subprocess
import pyudev
import usb.core, usb.util

LOG_FOLDER='/home/quanghuynh/USBanner/test/logs/{}'.format(time.strftime("%Y-%m-%d"))
LOG_FORMAT='[0] [{0}] [{1}]: {2}'

def event_handle():
	logs_folder_creator()
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
							with open(LOG_FOLDER+"/add.log","a+") as f:
								temp = LOG_FORMAT.format(datetime.datetime.now().strftime("%H:%M:%S"),'INFO',device.get('ID_VENDOR_ID')+':'+device.get('ID_MODEL_ID')) +" is plugged in.\n"
								f.write(temp)
								f.close()
		if device.action == 'remove':
			with open(LOG_FOLDER+"/remove.log","a+") as f:
				if None != device.get('ID_VENDOR_ID'):
					temp = LOG_FORMAT.format(datetime.datetime.now().strftime("%H:%M:%S"),'INFO',device.get('ID_VENDOR_ID')+':'+device.get('ID_MODEL_ID')) +" is unplugged.\n"
					f.write(temp)
					f.close()

def logs_folder_creator():
	if os.path.exists("/home/quanghuynh/USBanner/test/logs/{}".format(time.strftime("%Y-%m-%d"))) == False:
		os.makedirs("/home/quanghuynh/USBanner/test/logs/{}".format(time.strftime("%Y-%m-%d")))


event_handle()


