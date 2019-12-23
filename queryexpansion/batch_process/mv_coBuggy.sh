#!/bin/bash

buggyVersionMainCodeDir=need_to_mv_projs
allMethodsDir=~/Downloads/final_defects4j/allMethods

for l in $(cat $buggyVersionMainCodeDir)
do
    bid=$(echo $l | cut -f1 -d ",")
    proj=$(echo $bid | cut -f1 -d "_")
    buggyVersion=$(echo $l | cut -f2 -d ",")
    mainCodeDir=$(echo $l | cut -f3 -d ",")

    echo $proj $bid $buggyVersion $mainCodeDir
    cd $allMethodsDir/$proj/$bid
    cp -r java src/main
    rm -r java
done