#!/bin/bash

for file in *.py
do
    echo "$file"
    pep8 "$file"
    res=$?
    if [ $res -ne 0 ]; then
        echo "Pep8 Failed on $file"
        exit 1
    fi
done
