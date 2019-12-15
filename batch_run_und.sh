#!/bin/bash
. input.properties 
udbRootDir=${expResDir}/udb
expResDir=${expResParentDir}/expRes
udbRootDir=${expResDir}/udb 
udb_create_dir=~

for proj_name in "Closure" "Math"  #"Time" "Mockito"  "Lang"  "Math"  "Closure" 
do
    echo "handle project "${proj_name}"..."
    for proj_id in `ls ${allMethodsDir}/${proj_name}`
    do
    	cd ${undDir}
        echo $proj_id 
        udb_dir=${udbRootDir}/${proj_name} 

        rm -f ${udb_dir}/${proj_id}
        mkdir -p ${udb_dir}   # udb_dir must exist!
        ori_code_dir=${allMethodsDir}/${proj_name}/${proj_id} 
        ./und create -db ${udb_create_dir}/${proj_id} -languages Java add ${ori_code_dir} analyze -all  > ${udb_dir}/${proj_id}.log
        mv ${udb_create_dir}/${proj_id}.udb  ${udb_dir}
    done
done
