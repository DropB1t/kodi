#!/bin/bash
RED='\033[0;31m'
NC='\033[0m'
if [[ "$UID" != 0 ]] ; then
	echo -e "${RED}[ERRORE]${NC} Questo script ha bisogno dei privilegi di root per essere eseguito"
	exit
fi
apt update
apt upgrade -y
apt install ca-certificates curl gnupg lsb-release -y
mkdir -p /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/debian/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/debian \
  $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
apt update
sudo apt-get install docker-ce docker-ce-cli containerd.io docker-compose-plugin -y
mkdir mosquitto/
mkdir mosquitto/data/
mkdir mosquitto/log/
mkdir mosquitto/config/
printf "persistence true\npersistence_location /mosquitto/data/\nlog_dest file /mosquitto/log/mosquitto.log\nlistener 1883\nallow_anonymous true" > mosquitto/config/mosquitto.conf
#TODO togliere anonymous
chown -R 1883:1883 mosquitto/
docker compose up -d
# chmod u+x test.sh
# sudo vi /etc/sudoers copia incolla camibando username
