#!/bin/bash
. input.properties 
udbRootDir=${expResDir}/udb
expResDir=${expResParentDir}/expRes
udbRootDir=${expResDir}/udb 
udb_create_dir=~
PYTHON=python3.7

for proj_name in  "Closure"  # "Time" "Mockito"  "Lang"  "Math"  "Closure" 
do
    echo "handle project "${proj_name}"..."
    for proj_id in `ls ${allMethodsDir}/${proj_name}`
    do
    	
        echo $proj_id 
        # cd ${undDir}
        udb_dir=${udbRootDir}/${proj_name} 
        # rm -f ${udb_dir}/${proj_id}
        # mkdir -p ${udb_dir}   # udb_dir must exist!
        # ori_code_dir=${allMethodsDir}/${proj_name}/${proj_id} 
        # ./und create -db ${udb_create_dir}/${proj_id} -languages Java add ${ori_code_dir} analyze -all  > ${udb_dir}/${proj_id}.log
        # mv ${udb_create_dir}/${proj_id}.udb  ${udb_dir}

        cd_dir=${expResDir}/cd/${proj_name}
        ori_code_dir=${allMethodsDir}/${proj_name}/${proj_id}
        und_api_path=${undAPIPath}
        # rm -f ${cd_dir}/${proj_id}*
        # mkdir -p ${cd_dir}
        cd ${scriptRootDir}/queryexpansion 
        echo ${udb_dir}/${proj_id}.udb
        ${PYTHON} cd.py -u ${udb_dir}/${proj_id}.udb -s ${cd_dir}/${proj_id} -p ${ori_code_dir} -a ${und_api_path}





    done
done
