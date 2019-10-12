#!/bin/bash

deeplearning4jdir=$1
brAfterPTDir=$2
codeAfterPTDir=$3

brVecDir=$4
codeVecDir=$5

function runWord2Vec(){
    rm -rf ${brVecDir}
    rm -rf ${codeVecDir}
    mkdir -p ${brVecDir}
    mkdir -p ${codeVecDir}
    
    # java -cp word2vec.jar App  -source ${brAfterPTDir}    -target ${brVecDir}   
    java -cp word2vec.jar App  -source ${codeAfterPTDir}  -target ${codeVecDir} 
}

cd ${deeplearning4jdir}
runWord2Vec

