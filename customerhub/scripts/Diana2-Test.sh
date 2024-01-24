#!/bin/bash 

pid=$(lsof -t -i:4003)

if [ -n "$pid" ]; then
	sudo kill -9 $pid
fi

pid=$(sudo lsof -t -i:2003)

if [ -n "$pid" ]; then
	sudo kill -9 $pid
fi

#Start vue project 
cd ../documentation/Diana2-Test
sudo PORT=2003 npm run serve &

#Start flask 
python3 app.py & 
