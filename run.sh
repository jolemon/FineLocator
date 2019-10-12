#!/bin/bash

defects4jDatRootDir=$1
scriptRootDir=$2

bugReport4VectorDir=${defects4jDatRootDir}/bugReport4Vector
allMethodsDir=${defects4jDatRootDir}/allMethods
linkedBugMethodsDir=${defects4jDatRootDir}/linked-bugMethods

ptdir=${scriptRootDir}/pt
deeplearning4jdir=${scriptRootDir}/word2vec

expResDir=${scriptRootDir}/expRes

afterPTRootDir=${expResDir}/afterPT
brAfterPTDir=${afterPTRootDir}/br
codeAfterPTDir=${afterPTRootDir}/code
extractAfterPTDir=${afterPTRootDir}/extract

vecRootDir=${expResDir}/vec
brVecRootDir=${vecRootDir}/br
codeVecRootDir=${vecRootDir}/code

vecAfterPoolingDir=${expResDir}/vecAfterPooling
brVecAfterPoolingDir=${vecAfterPoolingDir}/br
codeVecAfterPoolingDir=${vecAfterPoolingDir}/code

python=python3.7


for proj in  "Time" # "Mockito" "Lang"  "Math" "Closure" 
do
    echo "handle project "${proj}"..."

    # step 1 : preprocessing for bug report and method
    ./run_pt.sh ${ptdir} ${bugReport4VectorDir}/${proj} ${allMethodsDir}/${proj} \
                         ${brAfterPTDir}/${proj} ${extractAfterPTDir}/${proj} ${codeAfterPTDir}/${proj}
    cd ${scriptRootDir}

    # step 2 : use deeplearning4j(word2vec) to get vectors of bug reports and methods
    # ./run_word2vec.sh ${deeplearning4jdir} ${brAfterPTDir}/${proj} ${codeAfterPTDir}/${proj}  ${brVecRootDir}/${proj}  ${codeVecRootDir}/${proj}
    cd ${scriptRootDir}

    # step 3 : query expansion for methods
    # ./query_expansion.py


    # step 4 : retrieve methods by similarity ranking on bug reports and augmented methods
    # ./rank.py


done