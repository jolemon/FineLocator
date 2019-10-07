#!/bin/bash

ori_BRDir=$2 #the original dir of bug reports.
pt_output_preprocessedBRDir=$3 #the output dir of preprocessed bug reports.
function runPT(){
    # tool 'pt' to preprocess bugReport4vector ... 
    #call pt jar:  
    # java -jar pt.jar ${ori_BRDir} ${pt_output_preprocessedBRDir}  
    java -cp preprocessor.jar org.gajnineteen.Preprocessor -source ${ori_BRDir} -target ${pt_output_preprocessedBRDir}
}

runPT