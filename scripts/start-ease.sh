#!/bin/bash

cd /vagrant/web_interface

source activate ease-env

python manage.py runserver 0.0.0.0:8000
