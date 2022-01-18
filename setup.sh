#!/bin/bash

echo Creating virtual environment.
if   [ -x "$(command -v python3)" ]; then
	python3 -m venv venv
elif   [ -x "$(command -v python)" ]; then
	python -m venv venv
fi

source venv/bin/activate || exit 1

echo Installing python libraries.
pip install -r requirements.txt

echo Installing emulator \(root access may be required\).
if   [ -x "$(command -v apt)" ];    then sudo apt install xserver-xephyr
elif [ -x "$(command -v dnf)" ];    then sudo dnf install xorg-x11-server-Xephyr
elif [ -x "$(command -v yum)" ];    then sudo yum install xorg-x11-server-Xephyr
elif [ -x "$(command -v apk)" ];    then sudo apk add --no-cache Xorg-server-xephyr
elif [ -x "$(command -v zypper)" ]; then sudo zypper install xorg-x11-server-extra 
elif [ -x "$(command -v pacman)" ]; then sudo pacman -S xorg-server-xephyr
else echo "You need to install: Xephyr emulator manually." >&2
fi
