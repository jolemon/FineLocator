#!/bin/bash

defects4jDatRootDir=$1
scriptRootDir=$2

bugReport4VectorDir=${defects4jDatRootDir}/bugReport4Vector
allMethodsDir=${defects4jDatRootDir}/allMethods
linkedBugMethodsDir=${defects4jDatRootDir}/linked-bugMethods

deeplearning4jdir=${scriptRootDir}/deeplearning4j

python=python3.7

# step1 : use deeplearning4j(word2vec) to get vectors of bug reports and methods
# call jar to handle bug report and code, vector saved to files

# step2 : query expansion for methods

# step3 : retrieve methods by similarity ranking on bug reports and augmented methods

for proj in  "Time" "Mockito" "Lang"  "Math" "Closure" 
do
    echo "handle project "${proj}"..."

    ./run_pt ${bugReport4VectorDir}/${proj} ${afterPTRootDir}/${proj} 

    ./run_word2vec

    ./query_expansion.py

    ./rank.py


done