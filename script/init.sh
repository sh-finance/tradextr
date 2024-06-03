#!/usr/bin/env bash

workspace=$(cd `dirname $0`/..; pwd)
cd $workspace

python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# install git hook
pre-commit install
