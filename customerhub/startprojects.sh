#!/bin/bash

SCRIPT_DIR="./scripts"

#Do a while loop
while true; do
    # Check if the scripts directory exists
    if [ -d "$SCRIPT_DIR" ]; then
        # Loop through each script in the directory
        for script in "$SCRIPT_DIR"/*.sh; do
            echo "$script"
            
            # Get the script name
            script_name=$(basename "$script" .sh)
            echo "$script_name"

            # Use pgrep to check if the script is running
            processes=$(pgrep -f "$script_name")

            # Count the number of processes
            num_processes=$(echo "$processes" | wc -w)

            if [ "$num_processes" -eq 1 ]; then
                echo "Rerunning the script..."
                "$script"
            elif [ "$num_processes" -gt 1 ]; then
                echo "Multiple instances of the script are running. Not rerunning."
            else
                echo "Script is not running."
                bash "$script"
            fi
        done
    else
        echo "Directory $SCRIPT_DIR does not exist."
    fi
    sleep 5
done

