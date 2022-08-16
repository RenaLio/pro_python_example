#!/usr/bin/env bash

pip3 install -r requirements.txt
systemctl stop propy
rm -rf /var/log/journal/*
chmod 755 propy.service
cp -f warpplus.service /etc/systemd/system/propy.service
systemctl daemon-reload
systemctl start propy
systemctl enable propy