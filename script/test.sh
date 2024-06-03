#!/usr/bin/env bash

workspace=$(cd `dirname $0`/..; pwd)
cd $workspace

source .venv/bin/activate

# 备份并清空日志
echo -e "\n\n\n\n\n" >> .app.old.log
cat .app.log >> .app.old.log
echo "$(date +'%Y-%m-%d %H:%M:%S.%3N')  Application Started." > .app.log
code -a -g .app.log:1
# 跳转到日志最后一行
# code -a -g .app.log:2147483647

python3 ./src/test.py
