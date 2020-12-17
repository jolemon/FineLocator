#!/bin/bash 

tp_script_dir=$1    # ~/FineLocator/queryexpansion
correspond_dir=$2   # ~/FineLocator/expRes/afterPT/correspond/${proj}
tp_dir=$3           # ~/FineLocator/expRes/tp/${proj}
ss_dir=$4
proj_id=$5          # ${proj_id}
PYTHON=$6           # python3.7

rm -f ${tp_dir}/${proj_id}
mkdir -p ${tp_dir}      
cd ${tp_script_dir}
${PYTHON} tp.py --correspond_path ${correspond_dir}/${proj_id} \
                --save_path ${tp_dir}/${proj_id} \
                --ss_dic_path ${ss_dir}/${proj_id}.dic