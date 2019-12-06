#!/bin/sh
if [ "$#" -ne 1 ]; then
    python ./20171062_1.py $1 $2
else 
    python ./20171062_2.py $1
fi
