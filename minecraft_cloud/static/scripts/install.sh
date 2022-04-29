#!/bin/sh
set -e

apt update
apt upgrade -y
apt install -y default-jre
apt install -y htop screen
screen -AmdS minecraft sh start.sh

exit 0
