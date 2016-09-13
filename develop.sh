#!/bin/bash

set -e

source ./config.py

pushd ${VIDEO_PATH}

opts=""

for f in *.h264
do
    opts+="-cat ${f} "
done

MP4Box -fps ${VIDEO_FRAMERATE} ${opts} film.mp4

# for a more old-timey effect, use
# ffmpeg -i film.mp4 -vf "curves=preset=vintage" vintage.mp4
# or something like https://github.com/mazurkin/mkfilm_old

popd
