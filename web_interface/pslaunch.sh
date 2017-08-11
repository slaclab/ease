#!/usr/bin/env bash
TNETPORT=9000
procServ $TNETPORT $(which gunicorn) -w 17 -b 0.0.0.0:8000 web_interface.wsgi
echo "starting procServ on localhost" $TNETPORT
