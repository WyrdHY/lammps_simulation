#!/bin/bash

# Loop from 1 to 100
for i in {1..100}
do
  # Define the directory and file names
  DIR="/root/Desktop/host/100_direct_cool/simulation_data/run_$i"
  FILE="cool_$i.in"

  # Check if the directory exists
  if [ -d "$DIR" ]; then
    # Change to the directory
    cd "$DIR" || exit

    # Check if the file exists
    if [ -f "$FILE" ]; then
      # Execute the command in the background
      lmp_mpi -in "$FILE" &
    else
      echo "File $FILE not found in $DIR"
    fi
  else
    echo "Directory $DIR not found"
  fi
done

# Wait for all background processes to complete
wait
