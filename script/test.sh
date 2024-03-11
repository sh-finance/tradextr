#!/usr/bin/env bash

workspace=$(cd `dirname $0`/..; pwd)
cd $workspace

source .venv/bin/activate

OUTPUT_ENV=False python3 ./src/test.py
