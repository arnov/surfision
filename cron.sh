#!/bin/sh
set -eu

alias ffmpeg="/usr/bin/ffmpeg"
alias python="/usr/local/bin/python"

cd /usr/src/app
python get_data.py
