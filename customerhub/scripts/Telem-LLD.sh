#!/bin/bash 

pid=$(lsof -t -i:4307)

if [ -n "$pid" ]; then
	sudo kill -9 $pid
fi

pid=$(sudo lsof -t -i:2445)

if [ -n "$pid" ]; then
	sudo kill -9 $pid
fi

#Start vue project 
cd ../documentation/Telem-LLD
sudo PORT=2445 npm run serve &

#Start flask 
python3 app.py & 
