#!/bin/sh
mkdir -p dependencies
cd dependencies

git clone https://github.com/matterport/Mask_RCNN.git
pip install Mask_RCNN/
