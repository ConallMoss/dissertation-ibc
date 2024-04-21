#!/bin/bash

declare -a datasets_rem=("amazon-ratings" "chess" "com-dblp" "dimacs9-NY" "ego-facebook" "elec" "email-EuAll" "epinions" "facebook-combined" "facebook-wosn-links" "linux" "munmun_twitter_social" "pajek-erdos" "slashdot-threads" "slashdot-zoo" "sx-mathoverflow" "topology" "web-NotreDame" "wikispeedia")
declare -a datasets_new=("chess" "ego-facebook" "elec" "email-EuAll" "epinions" "facebook-combined" "linux" "pajek-erdos" "slashdot-threads" "slashdot-zoo" "sx-mathoverflow" "topology" "wikispeedia")
for i in "${datasets_rem[@]}"
do 
    rm -rf "$i"
    #mkdir -p "$i"
done
for i in "${datasets_new[@]}"
do 
    #rm -rf "$i"
    mkdir -p "$i"
done