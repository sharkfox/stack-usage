#!/bin/bash -ex

SCRIPT_DIR=$(dirname "$0")
BUILD_DIR=$1

if [ -z $BUILD_DIR ];
then
	echo "BUILD_DIR required"
fi

find  $BUILD_DIR -name '*.cgraph' | grep -v stack-usage-log | xargs cat > stack-usage-log.cgraph
find  $BUILD_DIR -name '*.su'     | grep -v stack-usage-log | xargs cat > stack-usage-log.su
python3 ${SCRIPT_DIR}/stack-usage.py
