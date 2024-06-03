#!/usr/bin/env bash

workspace=$(cd `dirname $0`/..; pwd)
cd $workspace

git pull origin main
docker compose up --build -d
