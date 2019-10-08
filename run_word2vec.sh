#!/bin/bash

brAfterPTDir=$1
codeAfterPTDir=$2

brVecDir=$3
codeVecDir=$4

function runWord2Vec(){
    java -cp word2vec.jar org.gajnineteen.App  -source ${brAfterPTDir}    -target ${brVecDir}   -type br
    java -cp word2vec.jar org.gajnineteen.App  -source ${codeAfterPTDir}  -target ${codeVecDir} -type code
}

runWord2Vec

