#!/bin/bash
proj=$1
dim=$2
epochs=$3
finalRootDir=~/en/FineLocator/expRes/final
predictResDir=~/en/FineLocator/expRes/res

for((a=1;a<=10;a+=1))
do
    for((b=1;b<=10-$a;b+=1))
    do
        r=$((10-$a-$b))
        if [[ $r -ge 0 ]]; then
            tar -zcvf ${proj}_${dim}_${epochs}_${a}${b}${r}.tar ${finalRootDir}/${proj}/${proj}_*_${dim}_${epochs}_${a}${b}${r}
        fi
    done
done

tar -zcvf ${proj}_${dim}_${epochs}.tar  ${proj}_${dim}_${epochs}_*.tar
rm ${proj}_${dim}_${epochs}_*.tar