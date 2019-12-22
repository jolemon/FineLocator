#!/bin/bash

buggyVersionMainCodeDir=all_buggy_version
gitRoot=~/Downloads/bugcode
allMethodsDir=~/Downloads/allMethods

for l in $(cat $buggyVersionMainCodeDir)
do
    bid=$(echo $l | cut -f1 -d ",")
    buggyVersion=$(echo $l | cut -f2 -d ",")
    mainCodeDir=$(echo $l | cut -f3 -d ",")
    echo $bid $buggyVersion $mainCodeDir
    cd $gitRoot/$bid
    git checkout $buggyVersion
    mkdir -p $allMethodsDir/$bid
    cp -r $mainCodeDir $allMethodsDir/$bid/
done

