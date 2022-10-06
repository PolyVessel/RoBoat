#!/usr/bin/env bash

if [ "$EUID" -ne 0 ]
  then echo "Please run as root"
  exit
fi


# Moves working directory to this file's directory
cd "$(dirname "$0")"

#################
# Let's install some prereqs for our BeagleBone.
# Are you ready?
################

###
# Install Updates
###
apt-get update -y && sudo apt-get upgrade -y

###
# Install Python
###
apt-get update
apt-get install build-essential python3-dev python3-pip -y

###
# Lets install all of our Python Libraries
# --no-cache-dir because this can fail from MemoryErrors without it
###
pip3 --no-cache-dir install -r requirements.txt
