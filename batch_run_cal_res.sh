#!/bin/bash
proj=$1 
dim=$2         #300
epochs=$3      #10 
finalRootDir=~/en/FineLocator/expRes/final   
predictResDir=~/en/FineLocator/expRes/res

for((a=1;a<=10;a+=1))
do
    for((b=1;b<=10-$a;b+=1))
    do
        r=$((10-$a-$b))
        if [[ $r -ge 0 ]]; then          
            echo "calculate MAP, MRR, Hit-K for ${proj}_${dim}_${epochs}_${a}${b}${r}..."
            ./cal_HitK-MAP-MRR.sh $proj ${dim} ${epochs} $a$b$r ${finalRootDir}
            mkdir -p ${predictResDir}/${proj}
            mv ${proj}_${dim}_${epochs}_${a}${b}${r}_res ${predictResDir}/${proj}/
        fi   
    done
done