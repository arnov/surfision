#!/bin/sh
set -eu

alias ffmpeg="/usr/bin/ffmpeg"
alias python="/home/arnoveenstra/.pyenv/shims/python"

cd /home/arnoveenstra/surfision
export PYTHONPATH="$(pwd)"

python predict/predict_live.py --cam wijk
python predict/predict_live.py --cam scheveningen
