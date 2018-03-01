import re
import subprocess

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
	return devices

def get_info(devices):
	usb_location=[]
	mass_storage=[]
	for device in devices:
		usb_location.append(device.get("device"))
	for item in usb_location:
		temp = subprocess.Popen(["lsusb","-D", item],stdout=subprocess.PIPE).communicate()[0]
		communicateRes = temp.communicate()
		stdOutValue, stdErrValue = communicateRes
		my_output_list = stdOutValue.split(" ")

# after the split we have a list of string in my_output_list 
		for word in my_output_list :
			if word == "myword":
			print "something something"

get_info(get_usb())