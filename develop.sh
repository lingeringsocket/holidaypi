#!/bin/bash

source ./config.py

pushd ${VIDEO_PATH}

opts=""

for f in *.h264
do
    opts+="-cat ${f} "
done

MP4Box -fps ${VIDEO_FRAMERATE} ${opts} film.mp4

rm *.h264

popd
