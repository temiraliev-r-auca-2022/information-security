#!/bin/bash

file=$1
word=$2

count=$(grep -o "$word" "$file" | wc -l)

echo "The word '$word' appears $count times in $file."
