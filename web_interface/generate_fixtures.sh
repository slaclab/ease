#!/usr/bin/env bash

# use this script to generate the fixtures required for tests from .py
# allows the .json to be automatically generated, adapt to model changes

DB="fixture"
DBNAME="fixture.sqlite3"
MG="./manage.py"

for f in fixtures/*.py; do 
    #python "$f";
    $MG migrate --database=$DB
    $MG shell < "$f"
    NAME=$(echo $f| cut -f 1 -d '.')
    $MG dumpdata --database=$DB -o $NAME.json
    rm $DBNAME
done
