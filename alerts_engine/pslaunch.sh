#!/usr/bin/env bash
TNETPORT=9001
procServ $(which python3) launch_engine.py
echo "starting procServ on localhost" $TNETPORT
