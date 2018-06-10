#!/usr/bin/env bash

export ROOTDIR=/movit/
export CONFDIR=${ROOTDIR}movit/

echo ">>> Updating system <<<"

apt-get update
apt-get upgrade -y

echo ">>> Installing required packages <<<"
apt-get -qq install python3 build-essential python-software-properties python3 python3-dev python3-pip libjpeg-dev zlib1g-dev gcc

echo ">>> Installing Python requirements <<<"
pip3 install -qUr ${ROOTDIR}requirements.txt

echo ">>> Configuring DEV environnement <<<"
if [ ! -f ${CONFDIR}settings_local.py ]; then
    cp ${CONFDIR}settings_local.py.tpl ${CONFDIR}settings_local.py
fi

echo ">>> Creating Database <<<"
cd ${ROOTDIR}
python3 manage.py makemigrations
python3 manage.py migrate
