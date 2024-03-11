#!/usr/bin/env bash

workspace=$(cd `dirname $0`/..; pwd)
cd $workspace

git submodule update --init

python3 -m venv .venv
source .venv/bin/activate
pip install -i https://pypi.tuna.tsinghua.edu.cn/simple -r requirements.txt

# install git hook
pre-commit install
