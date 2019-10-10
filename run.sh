#!/bin/bash

defects4jDatRootDir=$1
scriptRootDir=$2

bugReport4VectorDir=${defects4jDatRootDir}/bugReport4Vector
allMethodsDir=${defects4jDatRootDir}/allMethods
linkedBugMethodsDir=${defects4jDatRootDir}/linked-bugMethods

deeplearning4jdir=${scriptRootDir}/word2vec

expResDir=${scriptRootDir}/expRes
codeExpResDir=${expResDir}/code
brExpResDir=${expResDir}/br

brAfterPTRootDir=${brExpResDir}/afterPT
codeAfterPTRootDir=${codeExpResDir}/afterPT

brVecRootDir=${brExpResDir}/vec
codeVecRootDir=${codeExpResDir}/vec

python=python3.7


for proj in  "Time" "Mockito" "Lang"  "Math" "Closure" 
do
    echo "handle project "${proj}"..."

    # step 1 : preprocessing for bug report and method
    ./run_pt.sh ${bugReport4VectorDir}/${proj} ${allMethodsDir}/${proj} ${brAfterPTRootDir}/${proj}  ${codeAfterPTRootDir}/${proj}


    # step 2 : use deeplearning4j(word2vec) to get vectors of bug reports and methods
    ./run_word2vec.sh ${brAfterPTRootDir}/${proj}  ${codeAfterPTRootDir}/${proj}  ${brVecRootDir}/${proj}  ${codeVecRootDir}/${proj}

    # step 3 : query expansion for methods
    ./query_expansion.py


    # step 4 : retrieve methods by similarity ranking on bug reports and augmented methods
    ./rank.py


done