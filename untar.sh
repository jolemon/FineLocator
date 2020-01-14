#!/bin/bash
proj=$1
dim=$2
epochs=$3
tar_name=${proj}_${dim}_${epochs}
predictResDir=~/en/FineLocator/expRes/res

tar -zxvf ~/${tar_name}.tar
mkdir -p ${tar_name}
mv ${tar_name}_*.tar ${tar_name}/
for dir in `ls ${tar_name}`
do    
    divide=$(echo "$dir" | awk -F "_" '{print $NF}' | awk -F "." '{print $1}')
    cd ${tar_name}
    tar -zxvf ${dir}
    cd ..
    ./cal_HitK-MAP-MRR.sh ${proj} ${dim} ${epochs} ${divide} ${tar_name}
    cd ${tar_name}
    rm -r ${proj}
    cd .. 
done

mkdir -p cal_res/${proj}
mv ${tar_name}_*_res cal_res/${proj}/

rm -r ${proj}_${dim}_${epochs}