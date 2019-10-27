#!/bin/bash 

correspond_dir=$1   # ~/FineLocator/expRes/afterPT/correspond/${proj}
tp_script_dir=$2    # ~/FineLocator/queryexpansion
tp_dir=$3           # ~/FineLocator/expRes/${proj}
proj=$4             # ${proj_id}
PYTHON=$5           # python3.7

rm -f ${tp_dir}/${proj}
mkdir -p ${tp_dir}      
cd ${tp_script_dir}
${PYTHON} tp.py -u ${udb_dir}/${proj}.udb -s ${cd_dir}/${proj}