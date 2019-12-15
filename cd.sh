#!/bin/bash 

ori_code_dir=$1   # ~/Downloads/final_defects4j/allMethods/Time/Time_3
cd_script_dir=$2  # ~/FineLocator/queryexpansion
udb_create_dir=$3 # ~/phd_gogogo
udb_dir=$4        # ~/FineLocator/expRes/udb/Time
cd_dir=$5         # ~/FineLocator/expRes/cd/Time
proj=$6           # Time_3

und_dir=$7        # /Applications/Understand.app/Contents/MacOS
und_api_path=$8   # /Applications/Understand.app/Contents/MacOS/Python
PYTHON=$9         # python3.7


echo "There exists license expiration problem in Scitool.Understand"
echo "So batch_run_und.sh for all project and get all *.udb files."
# rm -f ${udb_dir}/${proj}
# mkdir -p ${udb_dir}   # udb_dir must exist!
# cd ${und_dir}
# ./und create -db ${udb_create_dir}/${proj} -languages Java add ${ori_code_dir} analyze -all  > ${udb_dir}/${proj}.log
# mv ${udb_create_dir}/${proj}.udb  ${udb_dir}


rm -f ${cd_dir}/${proj}
mkdir -p ${cd_dir}
cd ${cd_script_dir}
${PYTHON} cd.py -u ${udb_dir}/${proj}.udb -s ${cd_dir}/${proj} -p ${ori_code_dir} -a ${und_api_path}

