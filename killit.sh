#!/bin/sh
ps -ef |grep "[p]ython table_main.py" 
ps -ef |grep "[p]ython table_main.py" |awk '{print "kill -9 " $2}' |sh
