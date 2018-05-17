#!/bin/bash

cd /vagrant/web_interface

source activate ease-env

python manage.py runserver 127.0.0.1:8000
