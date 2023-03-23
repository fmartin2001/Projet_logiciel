#!/bin/bash

VAR=$(realpath $0)
CHEMIN=$(echo "${VAR%/*}")

cd $CHEMIN
source ./env_robot/bin/activate

#lancer le programme
python3 ./IG.py
