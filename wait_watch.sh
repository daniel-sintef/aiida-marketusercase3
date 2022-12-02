#!/bin/bash

JOB_UUID=$(cat JOB_UUID)
WORKDIR=/home/aiidawork/${JOB_UUID}
mkdir -p $WORKDIR

INPUT_FILE=./inputs.json
cp $INPUT_FILE $WORKDIR/

OUTPUT_FILE=${WORKDIR}/results.json
while true
do
    if [ -e "$OUTPUT_FILE" ]; then
       echo "$OUTPUT_FILE found, done!"
       cp $OUTPUT_FILE ./
       break
    fi
    #sleep 2
done
