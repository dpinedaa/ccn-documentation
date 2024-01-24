#!/bin/bash 

pid=$(lsof -t -i:4004)

if [ -n "$pid" ]; then
	sudo kill -9 $pid
fi

pid=$(sudo lsof -t -i:2004)

if [ -n "$pid" ]; then
	sudo kill -9 $pid
fi

#Start vue project 
cd ../documentation/Diana2-Test4
sudo PORT=2004 npm run serve &

#Start flask 
python3 app.py & 
