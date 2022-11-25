#!/bin/bash
RED='\033[0;31m'
NC='\033[0m'
if [[ "$UID" != 0 ]] ; then
	echo -e "${RED}[ERRORE]${NC} Questo script ha bisogno dei privilegi di root per essere eseguito"
	exit
fi
apt update
apt upgrade -y
apt install python3 -y
apt install python3-pip -y
pip install opencv-python 
pip install tensorflow 
pip install paho-mqtt
pip install pillow
pip install scipi
