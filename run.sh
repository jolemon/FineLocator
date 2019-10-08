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

python=python3.7

# step 1 : preprocessing for bug report

# step 2 : preprocessing for method

# step 3 : use deeplearning4j(word2vec) to get vectors of bug reports and methods

# step 4 : query expansion for methods

# step 5 : retrieve methods by similarity ranking on bug reports and augmented methods

for proj in  "Time" "Mockito" "Lang"  "Math" "Closure" 
do
    echo "handle project "${proj}"..."

    ./run_pt.sh ${bugReport4VectorDir}/${proj} ${allMethodsDir}/${proj} ${brAfterPTRootDir}/${proj}  ${codeAfterPTRootDir}/${proj}

    ./run_word2vec

    ./query_expansion.py

    ./rank.py


done