#!/bin/sh
ps -ef |grep "[p]ython" |grep "[t]able_main.py$" 
ps -ef |grep "[p]ython" |grep "[t]able_main.py$" |awk '{print "kill -9 " $2}' |sh
