#!/usr/bin/env bash

workspace=$(cd `dirname $0`/..; pwd)
cd $workspace

source .venv/bin/activate

python3 ./src/main.py
