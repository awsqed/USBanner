import re, sys
import subprocess
import pyudev
import usb.core


def log_event():
	context = pyudev.Context()
	monitor = pyudev.Monitor.from_netlink(context)
	monitor.filter_by(subsystem='usb')
	for device in iter(monitor.poll, None):
		if device.action == 'add':
			with open("test/logs/add.log","a+") as f:
				f.write('{} connected\n'.format(device))
		if device.action == 'remove':
			with open("test/logs/remove.log","a+") as f:
				f.write('{} disconnected\n'.format(device))

def get_usb():
	device_re = re.compile("Bus\s+(?P<bus>\d+)\s+Device\s+(?P<device>\d+).+ID\s(?P<id>\w+:\w+)\s(?P<tag>.+)$", re.I)
	df = subprocess.check_output("lsusb")
	devices = []
	for i in df.split('\n'):
		if i:
			info = device_re.match(i)
			if info:
				dinfo = info.groupdict()
				dinfo['device'] = '/dev/bus/usb/%s/%s' % (dinfo.pop('bus'), dinfo.pop('device'))
				devices.append(dinfo)
	dev = usb.core.find(find_all=True, bDeviceClass=8)
	sys.stdout.write('There are ' + len(dev) + ' in the system\n.')
	#for device in devices:
	#	#idVendor="0x"+device.get("id").split(":")[0],idProduct="0x"+device.get("id").split(":")[1]
	#	dev = usb.core.find(find_all=True, bDeviceClass=8)
	


log_event()
#for device in get_usb():
#	print device

