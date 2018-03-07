import re, sys, os, datetime, time, getpass, threading
import subprocess
import pyudev
import usb.core, usb.util

LOG_FORMAT = "[0][{0}][{1}]: {2}\n"
USB_LIST = []

def create_log_folder(name):
    path = "logs/" + name
    if os.path.exists(path) == False:
        print "Log folder doesn't exist, creating one..."
        os.makedirs(path)

def log(log_type, log_level, message):
    path = "logs/{0}/{1}.log".format(log_type, time.strftime("%Y-%m-%d"))
    with open(path, "a+") as f:
        entry = LOG_FORMAT.format(datetime.datetime.now().strftime("%H:%M:%S"), log_level, message)
        f.write(entry)
        f.close()

def is_usb(device):
    if device.bDeviceClass == 8:
        return True
    for cfg in device:
        if usb.util.find_descriptor(cfg, bInterfaceClass = 8) != None:
            return True

def monitoring():
    print "Monitoring..."
    monitor = pyudev.Monitor.from_netlink(pyudev.Context())
    monitor.filter_by(subsystem = "usb")
    for device in iter(monitor.poll, None):
        vendor_id = str(device.get("ID_VENDOR_ID"))
        model_id = str(device.get("ID_MODEL_ID"))
        uid = vendor_id + ':' + model_id
        if device.action == "add":
            if device.get("ID_VENDOR_ID") != None:
                dev = usb.core.find(find_all = False, idVendor = int(vendor_id, 16), idProduct = int(model_id, 16), custom_match = is_usb)
                if dev != None:
                    if uid not in USB_LIST:
                        USB_LIST.append(uid)
                        log("connection", "INFO", uid + " is plugged in")
                        print uid + " is plugged in."
        if device.action == "remove":
            if uid in USB_LIST:
                USB_LIST.remove(uid)
                log("connection", "INFO", uid + " is unplugged")
                print uid + " is unplugged."

if __name__ == "__main__":
    create_log_folder("connection")
    threading.Thread(target = monitoring).start()