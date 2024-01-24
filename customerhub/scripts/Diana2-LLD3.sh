#!/bin/bash 

pid=$(lsof -t -i:4002)

if [ -n "$pid" ]; then
	sudo kill -9 $pid
fi

pid=$(sudo lsof -t -i:2002)

if [ -n "$pid" ]; then
	sudo kill -9 $pid
fi

#Start vue project 
cd ../documentation/Diana2-LLD3
sudo PORT=2002 npm run serve &

#Start flask 
python3 app.py & 
