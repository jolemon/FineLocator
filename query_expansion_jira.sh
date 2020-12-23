#!/bin/bash 

queryExpansionDir=$1   # ~/FineLocator/queryexpansion
code_vec_dir=$2        # ~/FineLocator/expRes/vec/code/${proj}
br_vec_dir=$3          # ~/FineLocator/expRes/vec/br/${proj}
save_dir=$4            # ~/FineLocator/expRes/final/${proj}
proj_id=$5             # ${proj_id}
word2vec_dimension=$6  
word2vec_model_epochs=$7
PYTHON=$8              # python3.7
sstp_dir=$9            # ~/FineLocator/expRes/ss/${proj} 
ac_dir=${10}
cd_dir=${11}           # ~/FineLocator/expRes/cd/${proj}
link_buggy_file=${12}  # ~/Downloads/final_defects4j/linked-bugMethods/${proj}_bugId_buggyMethodsName   
alpha=${13}
beta=${14}
gamma=${15}


rm -f ${save_dir}/${proj_id} 
rm -f ${ac_dir}/${proj_id}

mkdir -p ${save_dir} ${ac_dir}
cd ${queryExpansionDir}
${PYTHON} query_expansion_v2.py --sstp_path ${sstp_dir}/${proj_id} \
                             --cd_path ${cd_dir}/${proj_id} \
                             --code_vector_dir ${code_vec_dir}/${proj_id} \
                             --ac_save_path ${ac_dir}/${proj_id} \
                             --save_dir ${save_dir} \
                             --br_path ${br_vec_dir}/${proj_id} \
                             --br_id ${proj_id} \
                             --link_buggy_path ${link_buggy_file} \
                             --dim ${word2vec_dimension} \
                             --epochs ${word2vec_model_epochs} \
                             --alpha ${alpha}  --beta ${beta} --gamma ${gamma} 

