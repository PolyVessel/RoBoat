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
# Adafruit-BBIO is pretty cool. Let's install it.
###
sudo apt-get update
sudo apt-get install build-essential python3-dev python3-pip -y
sudo pip3 install Adafruit_BBIO
