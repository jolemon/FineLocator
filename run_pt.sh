#!/bin/bash

ori_BRDir=$1 #the original dir of bug reports.
ori_codeDir=$2

pt_output_preprocessedBRDir=$3 #the output dir of preprocessed bug reports.
pt_output_preprocessedCodeDir=$4

function runPT(){
    #java -cp preprocessor.jar org.gajnineteen.App  -source ${ori_BRDir}    -target ${pt_output_preprocessedBRDir}   -type br
    java -cp preprocessor.jar org.gajnineteen.App  -source ${ori_codeDir}  -target ${pt_output_preprocessedCodeDir} -type code
}

runPT


# java -cp preprocessor.jar org.gajnineteen.App  -source ~/Downloads/final_defects4j/allMethods -target  ~/FineLocator/expRes/code  -type code
# java -cp preprocessor.jar org.gajnineteen.App  -source ~/Downloads/final_defects4j/bugReport4Vector -target  ~/FineLocator/expRes/br   -type br