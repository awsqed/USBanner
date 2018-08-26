import os, time
import pyudev
import usb.core, usb.util

LOG_FORMAT = "[0][{0}][{1}]: {2}\n"
CONNECTED_USB = []
WHITELIST = []

def init_whitelist():
    filename = "whitelist"
    try:
        with open(filename, "r") as f:
            global WHITELIST
            WHITELIST = f.readline().split("|")
    except IOError:
        print "Whitelist file does not exist, creating one..."
        with open(filename, "w") as f:
            f.close()
        os.system("chmod 0600 " + filename)

def create_log_folder(name):
    path = "logs/" + name
    if os.path.exists(path) == False:
        print "Log folder does not exist, creating one..."
        os.makedirs(path)

def log(log_type, log_level, message):
    path = "logs/{0}/{1}.log".format(log_type, time.strftime("%Y-%m-%d"))
    with open(path, "a+") as f:
        entry = LOG_FORMAT.format(time.strftime("%H:%M:%S"), log_level, message)
        f.write(entry)
        f.close()

def is_usb(device):
    if device.bDeviceClass == 8:
        return True
    for cfg in device:
        if usb.util.find_descriptor(cfg, bInterfaceClass = 8) != None:
            return True

def usb_monitor():
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
                    if uid not in CONNECTED_USB:
                        CONNECTED_USB.append(uid)
                        log("connection", "INFO", uid + " is plugged in.")
                        if uid not in WHITELIST:
                            os.system("echo 0 > " + device.sys_path + "/authorized")
                            log("connection", "WARN", uid + " is not in the whitelist. Disconnected.")
                        else:
                            log("connection", "WARN", uid + " is allowed to connect.")
        if device.action == "remove":
            if uid in CONNECTED_USB:
                CONNECTED_USB.remove(uid)
                log("connection", "INFO", uid + " is unplugged.")

if __name__ == "__main__":
    init_whitelist()
    create_log_folder("connection")
    try:
        usb_monitor()
    except KeyboardInterrupt:
        print "Program exited"