#!/bin/bash

name=""
dataset=""
runs=1
prog=""

while getopts "n:d:r:p:" flag; do
    case "${flag}" in
        n) name="${OPTARG}";;
        d) dataset="${OPTARG}";;
        r) runs="${OPTARG}";;
        p) prog="${OPTARG}";;
    esac
done

echo $name
echo $dataset
echo $runs
echo $prog