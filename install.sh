#!/usr/bin/env bash

#################
# Let's install some prereqs for our BeagleBone.
# Are you ready?
################

###
# Set up a locale which supports UTF-8 encoding
###

sudo apt-get update && sudo apt-get upgrade

###
# Install Python
###
sudo apt-get update
sudo apt-get install build-essential python3-dev python3-pip -y

###
# Lets install all of our Python Libraries
###
sudo pip3 install -r requirements.txt
