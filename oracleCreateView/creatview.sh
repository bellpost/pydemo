#!/bin/sh

cd /opt/gjb
source /root/.bash_profile
echo $PATH 
echo `date`
/usr/bin/python ./oraclemouth_view.py

echo 'End' 
