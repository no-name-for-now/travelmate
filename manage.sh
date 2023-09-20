#!/bin/bash

# Function to run Flask-Migrate upgrade
function upgrade {
  flask db migrate
  flask db upgrade 
}

# Function to run Flask-Migrate downgrade
function downgrade {
  flask db downgrade 
}

# Check the command-line argument
if [ $# -lt 1 ]; then
  echo "Usage: $0 <command>"
  exit 1
fi

# Get the command from the first argument
command="$1"

# Perform actions based on the command
case "$command" in
  "upgrade")
    upgrade
    ;;
  "downgrade")
    downgrade
    ;;
  *)
    echo "Unknown command: $command"
    exit 1
    ;;
esac
