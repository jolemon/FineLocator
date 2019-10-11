#!/bin/bash

ptdir=$1
ori_BRDir=$2 #the original dir of bug reports.
ori_codeDir=$3

pt_output_preprocessedBRDir=$4 #the output dir of preprocessed bug reports.
pt_output_preprocessedCodeDir=$5

function runPT(){
    rm -rf ${pt_output_preprocessedBRDir}
    rm -rf ${pt_output_preprocessedCodeDir}
    mkdir -p ${pt_output_preprocessedBRDir}
    mkdir -p ${pt_output_preprocessedCodeDir}
    java -cp preprocessor.jar org.gajnineteen.App  -source ${ori_BRDir}    -target ${pt_output_preprocessedBRDir}   -type br
    java -cp preprocessor.jar org.gajnineteen.App  -source ${ori_codeDir}  -target ${pt_output_preprocessedCodeDir} -type code
}

cd ${ptdir}
runPT

# java -cp preprocessor.jar org.gajnineteen.App  -source ~/Downloads/final_defects4j/allMethods       -target  ~/FineLocater/expRes/code  -type code
# java -cp preprocessor.jar org.gajnineteen.App  -source ~/Downloads/final_defects4j/bugReport4Vector -target  ~/FineLocator/expRes/br    -type br