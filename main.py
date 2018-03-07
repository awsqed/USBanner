import re, sys, os, datetime, time, getpass
import subprocess
import pyudev
import usb.core, usb.util

LOG_FORMAT = "[0][{0}][{1}]: {2}\n"
USB_LIST = []

def create_log_folder(name):
    path = "logs/" + name
    if os.path.exists(path) == False:
        os.makedirs(path)

def log(log_type, log_level, message):
    path = "logs/{0}/{1}.log".format(log_type, time.strftime("%Y-%m-%d"))
    with open(path, "a+") as f:
        entry = LOG_FORMAT.format(datetime.datetime.now().strftime("%H:%M:%S"), log_level, message)
        f.write(entry)
        f.close()

def init_handler():
    context = pyudev.Context()
    monitor = pyudev.Monitor.from_netlink(context)
    monitor.filter_by(subsystem = "usb")
    for device in iter(monitor.poll, None):
        uid = str(device.get("ID_VENDOR_ID")) + ':' + str(device.get("ID_MODEL_ID"))
        if device.action == "add":
            if device.get("ID_VENDOR_ID") != None:
                dev = usb.core.find(idVendor = int(device.get("ID_VENDOR_ID"), 16), idProduct = int(device.get("ID_MODEL_ID"), 16))
                for cfg in dev:
                    for i in cfg:
                        if i.bInterfaceClass == 8:
                            if uid not in USB_LIST:
                                USB_LIST.append(uid)
                                print USB_LIST
                            log("connection", "INFO", uid + " is plugged in")
        if device.action == "remove":
            if device.get("ID_VENDOR_ID") != None:
                if uid in USB_LIST:
                    USB_LIST.remove(uid)
                    print USB_LIST
                log("connection", "INFO", uid + " is unplugged")

create_log_folder("connection")
init_handler()
