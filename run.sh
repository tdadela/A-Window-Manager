#!/bin/bash

size="1200x800"

if [[ $# -eq 1 ]]; then
	size=$1
fi

source venv/bin/activate
Xephyr -screen $size -br :1 &
emu_pid=$!
DISPLAY=:1 python wm.py

kill $emu_pid
