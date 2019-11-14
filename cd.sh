#!/bin/bash 

ori_code_dir=$1   # ~/Downloads/final_defects4j/allMethods/Time/Time_3
cd_script_dir=$2  # ~/FineLocator/queryexpansion
udb_dir=$3        # ~/FineLocator/expRes/udb/Time
cd_dir=$4         # ~/FineLocator/expRes/cd/Time
proj=$5           # Time_3

und_dir=$6        # /Applications/Understand.app/Contents/MacOS
und_api_path=$7   # /Applications/Understand.app/Contents/MacOS/Python
PYTHON=$8         # python3.7


rm -f ${udb_dir}/${proj}
mkdir -p ${udb_dir}   # udb_dir must exist!
rm -f ${cd_dir}/${proj}
mkdir -p ${cd_dir}

cd ${cd_script_dir}
${und_dir}/und create -db ${udb_dir}/${proj} -languages Java add ${ori_code_dir} analyze -all > ${udb_dir}/${proj}.log
${PYTHON} cd.py -u ${udb_dir}/${proj}.udb -s ${cd_dir}/${proj} -p ${ori_code_dir} -a ${und_api_path}

