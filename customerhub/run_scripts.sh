#!/bin/bash

# Check if an argument is provided
if [ $# -eq 0 ]; then
    echo "Error: Please provide the script name as an argument."
    exit 1
fi

# Get the script name from the argument
script_name=$1

# Check if the script exists
if [ -f "scripts/$script_name" ]; then
    # Execute the provided script
    bash "scripts/$script_name"
else
    echo "Error: Script '$script_name' not found."
    exit 1
fi
