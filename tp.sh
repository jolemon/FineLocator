#!/bin/bash 

tp_script_dir=$1    # ~/FineLocator/queryexpansion
correspond_dir=$2   # ~/FineLocator/expRes/afterPT/correspond/${proj}
tp_dir=$3           # ~/FineLocator/expRes/tp/${proj}
proj_id=$4          # ${proj_id}
PYTHON=$5           # python3.7

rm -f ${tp_dir}/${proj_id}
mkdir -p ${tp_dir}      
cd ${tp_script_dir}
${PYTHON} tp.py -c ${correspond_dir}/${proj_id} -s ${tp_dir}/${proj_id}