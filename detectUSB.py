import re, sys, os, datetime, time, getpass
import subprocess
import pyudev
import usb.core, usb.util

LOG_FOLDER='/home/quanghuynh/USBanner/test/logs/{}'.format(time.strftime("%Y-%m-%d"))
LOG_FORMAT='[0] [{0}] [{1}]: {2}'

# Credit goes to MrVallentin, Dont know why after run setup.py I cannot use this lib
# https://github.com/MrVallentin/mount.py
def list_media_devices():
	# If the major number is 8, that indicates it to be a disk device.
	#
	# The minor number is the partitions on the same device:
	# - 0 means the entire disk
	# - 1 is the primary
	# - 2 is extended
	# - 5 is logical partitions
	# The maximum number of partitions is 15.
	#
	# Use `$ sudo fdisk -l` and `$ sudo sfdisk -l /dev/sda` for more information.
	with open("/proc/partitions", "r") as f:
		devices = []
		
		for line in f.readlines()[2:]: # skip header lines
			words = [ word.strip() for word in line.split() ]
			minor_number = int(words[1])
			device_name = words[3]
			
			if (minor_number % 16) == 0:
				path = "/sys/class/block/" + device_name
				
				if os.path.islink(path):
					if os.path.realpath(path).find("/usb") > 0:
						devices.append("/dev/" + device_name)
		
		return devices

def get_device_name(device):
	return os.path.basename(device)

def get_device_block_path(device):
	return "/sys/block/%s" % get_device_name(device)

def get_media_path(device):
	directory = "/media/"+getpass.getuser()+"/"
	return directory+next(os.walk(directory))[1][0]

def get_partition(device):
	os.system("fdisk -l %s > output" % device)
	with open("output", "r") as f:
		data = f.read()
		return data.split("\n")[-2].split()[0].strip()

def is_mounted(device):
	return os.path.ismount(get_media_path(device))

def unmount_partition(name="usb"):
	path = get_media_path(name)
	if is_mounted(path):
		os.system("umount " + path)
		#os.system("rm -rf " + path)

def mount(device, name=None):
	if not name:
		name = get_device_name(device)
	mount_partition(get_partition(device), name)

def unmount(device, name=None):
	if not name:
		name = get_device_name(device)
	unmount_partition(name)

def detect_connection():
	logs_folder_creator()
	context = pyudev.Context()
	monitor = pyudev.Monitor.from_netlink(context)
	monitor.filter_by(subsystem='usb')
	class8_list=[]
	for device in iter(monitor.poll, None):
		ids=str(device.get('ID_VENDOR_ID'))+':'+str(device.get('ID_MODEL_ID'))
		if device.action == 'add':
			# idVendor and idProduct will be hex
			if None != device.get('ID_VENDOR_ID'):
				dev = usb.core.find(idVendor=int(device.get('ID_VENDOR_ID'),16), idProduct=int(device.get('ID_MODEL_ID'),16))
				for cfg in dev:
					for i in cfg:
						if i.bInterfaceClass == 8: # Get interface class , Mass storage will equal to 8	
							if ids not in class8_list:
								class8_list.append(ids) # append to list for remove action
							with open(LOG_FOLDER+"/add.log","a+") as f:
								temp = LOG_FORMAT.format(datetime.datetime.now().strftime("%H:%M:%S"),'INFO',ids) +" is plugged in.\n"
								f.write(temp)
								f.close()
		if device.action == 'remove':
			if None != device.get('ID_VENDOR_ID'):
				if ids not in class8_list:
					pass
				else:
					class8_list.remove(ids)
				with open(LOG_FOLDER+"/remove.log","a+") as f:
					temp = LOG_FORMAT.format(datetime.datetime.now().strftime("%H:%M:%S"),'INFO',ids) +" is unplugged.\n"
					f.write(temp)
					f.close()

def logs_folder_creator():
	if os.path.exists("/home/quanghuynh/USBanner/test/logs/{}".format(time.strftime("%Y-%m-%d"))) == False:
		os.makedirs("/home/quanghuynh/USBanner/test/logs/{}".format(time.strftime("%Y-%m-%d")))

def cls():
	os.system("cls" if os.name == "nt" else "clear")

def main():
	for i in list_media_devices():
		if is_mounted(i):
			unmount(i)
		else:
			pass


if __name__=="__main__":
	main()

