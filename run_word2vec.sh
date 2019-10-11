#!/bin/bash

brAfterPTDir=$1
codeAfterPTDir=$2

brVecDir=$3
codeVecDir=$4

function runWord2Vec(){
    rm -rf ${brVecDir}
    rm -rf ${codeVecDir}
    mkdir -p ${brVecDir}
    mkdir -p ${codeVecDir}
    
    java -cp word2vec.jar App  -source ${brAfterPTDir}    -target ${brVecDir}   
    java -cp word2vec.jar App  -source ${codeAfterPTDir}  -target ${codeVecDir} 
}

runWord2Vec

