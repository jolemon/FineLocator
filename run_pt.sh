#!/bin/bash

ptdir=$1
ori_BRDir=$2 #the original dir of bug reports.
ori_codeDir=$3
gitDir=$4
proj_id=$5

pt_output_preprocessedBRDir=$6 #the output dir of preprocessed bug reports.
pt_output_extractMethodDir=$7
pt_output_correspondDir=$8
pt_output_preprocessedCodeDir=$9

buggy_version_file=${10}
buggy_version_commitID=0
proj=${11}
threads=${12}

function runPT(){
    rm -rf ${pt_output_preprocessedBRDir}/${proj_id}
    java -cp preprocessor.jar org.gajnineteen.App \
         -source ${ori_BRDir}/${proj_id} \
         -target ${pt_output_preprocessedBRDir}/${proj_id} \
         -type br \
         --num_threads ${threads}

    # 避免Windows提交导致的"^M"问题，应该先在linux下对allMethods执行
    # 以下指令 : find . -type f -name "*.java" -print0 | xargs -0 sed -i 's/^M//g'
    rm -rf ${pt_output_extractMethodDir}/${proj_id}
    rm -rf ${pt_output_correspondDir}/${proj_id}
    echo "git:  "${gitDir}"/.git" 
    java -cp preprocessor.jar org.gajnineteen.App \
         -source ${ori_codeDir}/${proj_id}/${proj} \
         -target ${pt_output_extractMethodDir}/${proj_id}/${proj} \
         -correspond ${pt_output_correspondDir}/${proj_id}/${proj} \
         -type extract \
         -commitID ${buggy_version_commitID} \
         -git ${gitDir}/.git \
         --num_threads ${threads}

    rm -rf ${pt_output_preprocessedCodeDir}/${proj_id}
    mkdir -p ${pt_output_preprocessedCodeDir}/${proj_id}
    java -cp preprocessor.jar org.gajnineteen.App \
         -source ${pt_output_extractMethodDir}/${proj_id}/${proj} \
         -target ${pt_output_preprocessedCodeDir}/${proj_id}/${proj} \
         -type code \
         --num_threads ${threads}
}



function getBuggyVersionCommitID(){
    for l in $(cat ${buggy_version_file})
    do
        bid=$(echo $l | cut -f1 -d ",")
        buggyVersion=$(echo $l | cut -f2 -d ",") 
        if [[ $proj_id = $bid  ]]; then
            buggy_version_commitID=$buggyVersion
            break
        fi
    done
}

getBuggyVersionCommitID
echo ${proj_id}' buggyCommitSHA: '${buggy_version_commitID}
cd ${ptdir}
if [[ ! -e ${pt_output_preprocessedBRDir}/${proj_id} ]]; then
    runPT
else
    echo "skip ${proj_id}"
fi
# runPT
  

# for Defects4J
#     java -cp preprocessor.jar org.gajnineteen.App  
#          -source ${ori_codeDir}/${proj_id}  
#          -target ${pt_output_extractMethodDir}/${proj_id} \
#          -correspond ${pt_output_correspondDir}/${proj_id} -type extract \
#          -commitID ${buggy_version_commitID} \
#          -git ${gitDir}/${proj_id}/.git 
#     java -cp preprocessor.jar org.gajnineteen.App \
#          -source ${pt_output_extractMethodDir}/${proj_id} \
#          -target ${pt_output_preprocessedCodeDir}/${proj_id} \
#          -type code
