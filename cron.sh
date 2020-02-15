#!/bin/sh
set -eu

alias ffmpeg="/usr/bin/ffmpeg"
alias python="/usr/local/bin/python"

cd /usr/src/app
python predict_live.py --cam wijk
python predict_live.py --cam scheveningen
