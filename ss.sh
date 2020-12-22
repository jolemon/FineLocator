#!/bin/bash 

ss_script_dir=$1       # ~/FineLocator/queryexpansion
code_vec_dir=$2        # ~/FineLocator/expRes/vec/code/${proj} 
correspond_dir=$3      # ~/FineLocator/expRes/afterPT/correspond/${proj}
ss_dir=$4              # ~/FineLocator/expRes/ss/${proj}
proj_id=$5             # ${proj_id}
word2vec_dimension=$6 
PYTHON=$7              # python3.7

rm -f ${ss_dir}/${proj_id}
mkdir -p ${ss_dir}      
cd ${ss_script_dir}
${PYTHON} sstp.py --code_vector_dir ${code_vec_dir}/${proj_id} \
				  --correspond_path ${correspond_dir}/${proj_id} \
                  --dim ${word2vec_dimension} \
                  --save_path ${ss_dir}/${proj_id}

# ${PYTHON} ss.py --code_vector_dir ${code_vec_dir}/${proj_id} \
#                 --dim ${word2vec_dimension} \
#                 --save_path ${ss_dir}/${proj_id}