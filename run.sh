#!/bin/bash

APP_NAME="usbanner"

if [ "$EUID" -ne 0 ]
then
	echo "Current user doesn't have sudo privilege."
	echo "Sudo privilege is required to monitor USB ports."
	exit 3
fi

while [ "$#" -ne 1 ]; do
	echo "Usage:  sudo ${0} OPTIONS"
	echo "OPTIONS:"
	echo "        sudo ${0} start				start monitoring."
	echo "        sudo ${0} stop				stop monitoring."
	exit 1
done

case "${1}" in
start)
	nohup python "${APP_NAME}.py" >& /dev/null &
	# Get pid for stop
	echo $! > "${APP_NAME}.pid"
	;;
stop)
	# Get pid from file and send kill command
	pkill -F "${APP_NAME}.pid"
	# Remove pid file
	rm "${APP_NAME}.pid"
	;;
esac