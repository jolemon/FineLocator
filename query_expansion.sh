#!/bin/bash 

queryExpansionDir=$1  # ~/FineLocator/queryexpansion
code_vec_dir=$2       # ~/FineLocator/expRes/vec/code/${proj}
br_vec_dir=$3         # ~/FineLocator/expRes/vec/br/${proj}
save_dir=$4           # ~/FineLocator/expRes/final/${proj}
proj_id=$5            # ${proj_id}
word2vec_dimension=$6 # 
word2vec_model_epochs=$7
PYTHON=$8            # python3.7
ss_dir=$9             # ~/FineLocator/expRes/ss/${proj}
tp_dir=${10}             # ~/FineLocator/expRes/tp/${proj}
cd_dir=${11}          # ~/FineLocator/expRes/cd/${proj}
link_buggy_file=${12}  # ~/Downloads/final_defects4j/linked-bugMethods/${proj}_bugId_buggyMethodsName   
alpha=${13}
beta=${14}
gamma=${15}


rm -f ${save_dir}/${proj_id}
# rm -f ${save_dir}/${proj_id}.acdic

mkdir -p ${save_dir}     
cd ${queryExpansionDir}
${PYTHON} query_expansion.py \
          -ss ${ss_dir}/${proj_id} \
          -tp ${tp_dir}/${proj_id} \
          -cd ${cd_dir}/${proj_id} \
          -c ${code_vec_dir}/${proj_id} \
          -b ${br_vec_dir}/${proj_id} \
          -i ${proj_id} \
          -l ${link_buggy_file} \
          -d ${word2vec_dimension} \
          -s ${save_dir} \
          -e ${word2vec_model_epochs} \
          -alpha ${alpha} \
          -beta ${beta} \
          -gamma ${gamma}


          # /${proj_id}_${word2vec_dimension}_${word2vec_model_epochs}_${alpha}_${alpha}_${beta}_${gamma} \
