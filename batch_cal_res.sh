#!/bin/bash
proj=$1
dim=$2
epochs=$3
finalRootDir=~/en/FineLocator/expRes/final
predictResDir=~/en/FineLocator/expRes/res

mkdir -p ${predictResDir}/${proj}
for((a=1;a<=10;a+=1))
do
    for((b=0;b<=10-$a;b+=1))
    do   
        r=$((10-$a-$b))
        if [[ $r -ge 0 ]]; then
	    ./cal_HitK-MAP-MRR.sh $proj $dim $epochs ${a}${b}${r} ${finalRootDir}
            mv ${proj}_${dim}_${epochs}_${a}${b}${r}_res ${predictResDir}/${proj}/
        fi
    done
done

