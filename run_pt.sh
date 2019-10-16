#!/bin/bash

ptdir=$1
ori_BRDir=$2 #the original dir of bug reports.
ori_codeDir=$3
gitDir=$4

pt_output_preprocessedBRDir=$5 #the output dir of preprocessed bug reports.
pt_output_extractMethodDir=$6
pt_output_correspondDir=$7
pt_output_preprocessedCodeDir=$8

function runPT(){
    # rm -rf ${pt_output_preprocessedBRDir}
    # java -cp preprocessor.jar org.gajnineteen.App  -source ${ori_BRDir}    -target ${pt_output_preprocessedBRDir}   -type br

    rm -rf ${pt_output_extractMethodDir} 
    java -cp preprocessor.jar org.gajnineteen.App  -source ${ori_codeDir}  -target ${pt_output_extractMethodDir} \
                                                   -correspond ${pt_output_correspondDir} -type extract \
                                                   -git ${gitDir}

    # rm -rf ${pt_output_preprocessedCodeDir}
    # mkdir -p ${pt_output_preprocessedCodeDir}
    # java -cp preprocessor.jar org.gajnineteen.App  -source ${pt_output_extractMethodDir}  -target ${pt_output_preprocessedCodeDir} -type code	
}



cd ${ptdir}
runPT

# java -cp preprocessor.jar org.gajnineteen.App  -source ~/Downloads/final_defects4j/allMethods       -target  ~/FineLocater/expRes/code  -type code
# java -cp preprocessor.jar org.gajnineteen.App  -source ~/Downloads/final_defects4j/bugReport4Vector -target  ~/FineLocator/expRes/br    -type br

# java -cp preprocessor.jar org.gajnineteen.App -source /Users/lienming/Downloads/final_defects4j/allMethods/Time/Time_3 -target /Users/lienming/FineLocator/expRes/afterPT/extract/Time/Time_3 \
#      -correspond /Users/lienming/FineLocator/expRes/afterPT/correspond/Time/Time_3 -type extract -git /Users/lienming/Downloads/bugcode/Time_3/.git