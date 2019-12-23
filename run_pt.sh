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

function runPT(){
    rm -rf ${pt_output_preprocessedBRDir}/${proj_id}
    java -cp preprocessor.jar org.gajnineteen.App  -source ${ori_BRDir}/${proj_id}    -target ${pt_output_preprocessedBRDir}/${proj_id}   -type br

    rm -rf ${pt_output_extractMethodDir}/${proj_id}
    rm -rf ${pt_output_correspondDir}/${proj_id} 
    java -cp preprocessor.jar org.gajnineteen.App  -source ${ori_codeDir}/${proj_id}  -target ${pt_output_extractMethodDir}/${proj_id} \
                                                   -correspond ${pt_output_correspondDir}/${proj_id} -type extract \
                                                   -git ${gitDir}/${proj_id}/.git \
                                                   -commitID ${buggy_version_commitID}

    rm -rf ${pt_output_preprocessedCodeDir}/${proj_id}
    mkdir -p ${pt_output_preprocessedCodeDir}/${proj_id}
    java -cp preprocessor.jar org.gajnineteen.App  -source ${pt_output_extractMethodDir}/${proj_id}  -target ${pt_output_preprocessedCodeDir}/${proj_id} -type code	
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
echo ${proj_id}' buggy version commitID is '${buggy_version_commitID}
cd ${ptdir}
runPT
  

# java -cp preprocessor.jar org.gajnineteen.App -source /Users/lienming/Downloads/final_defects4j/allMethods/Time/Time_3 -target /Users/lienming/FineLocator/expRes/afterPT/extract/Time/Time_3 \
#      -correspond /Users/lienming/FineLocator/expRes/afterPT/correspond/Time/Time_3 -type extract -git /Users/lienming/Downloads/bugcode/Time_3/.git