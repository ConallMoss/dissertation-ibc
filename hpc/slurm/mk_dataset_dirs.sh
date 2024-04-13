#!/bin/bash

declare -a datasets=("amazon-ratings" "chess" "com-dblp" "dimacs9-NY" "ego-facebook" "elec" "email-EuAll" "epinions" "facebook-wosn-links" "github" "linux" "munmun_twitter_social" "pajek-erdos" "slashdot-threads" "sx-mathoverflow" "web-NotreDame" "youtube-groupmemberships" "facebook_combined")
for i in "${datasets[@]}"
do 
    rm -rf "$i"
    mkdir -p "$i"
done