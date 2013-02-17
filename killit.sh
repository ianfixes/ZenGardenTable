#!/bin/sh
ps -ef |grep "[p]ython table.py" 
ps -ef |grep "[p]ython table.py" |awk '{print "kill -9 " $2}' |sh
