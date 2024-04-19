#!/bin/bash

declare -a datasets=("amazon-ratings" "chess" "com-dblp" "dimacs9-NY" "ego-facebook" "elec" "email-EuAll" "epinions" "facebook-combined" "facebook-wosn-links" "linux" "munmun_twitter_social" "pajek-erdos" "slashdot-threads" "slashdot-zoo" "sx-mathoverflow" "topology" "web-NotreDame" "wikispeedia")
for i in "${datasets[@]}"
do 
    rm -rf "$i"
    mkdir -p "$i"
done