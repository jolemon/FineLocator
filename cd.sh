#!/bin/bash 

ori_code_dir=$1   # ~/Downloads/final_defects4j/allMethods/${proj}/${proj_id}
cd_script_dir=$2  # ~/FineLocator/queryexpansion
udb_create_dir=$3 # ~
udb_dir=$4        # ~/FineLocator/expRes/udb/${proj}
cd_dir=$5         # ~/FineLocator/expRes/cd/${proj}
proj_id=$6        

und_dir=$7        # /Applications/Understand.app/Contents/MacOS
und_api_path=$8   # /Applications/Understand.app/Contents/MacOS/Python
PYTHON=$9         # python3.7


echo "There exists license expiration problem in Scitool.Understand"
echo "So batch_run_und.sh for all project and get all *.udb files."
rm -f ${udb_dir}/${proj_id}
mkdir -p ${udb_dir}   # udb_dir must exist!
cd ${und_dir}
./und create -db ${udb_create_dir}/${proj_id} -languages Java add ${ori_code_dir} analyze -all > ${udb_dir}/${proj_id}.log
mv ${udb_create_dir}/${proj_id}.udb  ${udb_dir}


rm -f ${cd_dir}/${proj_id}
mkdir -p ${cd_dir}
cd ${cd_script_dir}
${PYTHON} cd.py --udb_path ${udb_dir}/${proj_id}.udb \
                --save_path ${cd_dir}/${proj_id} \
                --parent_dir ${ori_code_dir} \
                --api_path ${und_api_path}

