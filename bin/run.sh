#!/bin/ash
set -x
/usr/sbin/crond -b -L /dev/stdout
/usr/bin/python3 -u /app/watcher.py