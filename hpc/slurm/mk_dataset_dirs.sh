#!/bin/bash

declare -a datasets=("facebook_combined" "slashdot-threads" "elec" "ego-facebook" "pajek-erdos" "email-EuAll" "epinions")
for i in "${datasets[@]}"
do 
    #rm -r "$i"
    mkdir -p "$i"
done