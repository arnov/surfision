#!/bin/sh
mkdir -p dependencies
cd dependencies

git clone https://github.com/matterport/Mask_RCNN.git
git clone https://github.com/experiencor/kangaroo.git

cd dependencies/Mask_RCNN
python setup.py install
