import re, sys, os
import subprocess
import pyudev


def event_handle():
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
	
	for device in devices:
		temp = device.get("device")
		print temp
		command = ['lsusb', '-D', '{}'.format(temp), "|", "grep", "-Ei", "'(idVendor|Mass Storage)'"]
		print subprocess.check_output(command,shell=True) 

get_usb()


