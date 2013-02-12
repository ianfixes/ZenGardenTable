#!/bin/sh
ps -ef |grep "python table.py" 
ps -ef |grep "python table.py" |awk '{print "kill -9 " $2}' |sh
