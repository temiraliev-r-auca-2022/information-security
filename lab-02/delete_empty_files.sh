#!/bin/bash

directory=$1

find "$directory" -type f -empty | while read file
do
    echo "Deleting: $file"
    rm "$file"
done
