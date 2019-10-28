#!/bin/bash 

ss_script_dir=$1      # ~/FineLocator/queryexpansion
code_vec_dir=$2       # ~/FineLocator/expRes/vec/code/${proj}
br_vec_dir=$3         # ~/FineLocator/expRes/vec/br/${proj}
ss_dir=$4             # ~/FineLocator/expRes/ss/${proj}
proj_id=$5            # ${proj_id}
word2vec_dimension=$6
PYTHON=$7             # python3.7

rm -f ${ss_dir}/${proj_id}
mkdir -p ${ss_dir}      
cd ${ss_script_dir}
${PYTHON} ss.py -br ${br_vec_dir}/${proj_id} -c ${code_vec_dir}/${proj_id} \
                -d ${word2vec_dimension} -s ${ss_dir}/${proj_id}