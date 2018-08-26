#!/bin/bash
if [ "$EUID" -ne 0 ]
then
	echo "Current user doesn't have sudo privilege."
	echo "Sudo privilege is required to monitor USB ports."
	exit 3
else
	nohup python usbanner.py >& /dev/null &
fi
exit
