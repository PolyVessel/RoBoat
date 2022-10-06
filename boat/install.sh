#!/usr/bin/env bash

if [ "$EUID" -ne 0 ]
  then echo "Please run as root"
  exit
fi

#################
# Let's install some prereqs for our BeagleBone.
# Are you ready?
################

###
# Set up a locale which supports UTF-8 encoding
###

apt-get update && sudo apt-get upgrade

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
