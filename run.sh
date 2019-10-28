#!/bin/bash

defects4jDatRootDir=~/Downloads/final_defects4j #$1
scriptRootDir=~/FineLocator #$2

bugReport4VectorDir=${defects4jDatRootDir}/bugReport4Vector
allMethodsDir=${defects4jDatRootDir}/allMethods
linkedBugMethodsDir=${defects4jDatRootDir}/linked-bugMethods

gitRootDir=~/Downloads/bugcode
undDir=/Applications/Understand.app/Contents/MacOS

ptDir=${scriptRootDir}/pt
deeplearning4jDir=${scriptRootDir}/word2vec
queryExpansionDir=${scriptRootDir}/queryexpansion
expResDir=${scriptRootDir}/expRes

afterPTRootDir=${expResDir}/afterPT
brAfterPTDir=${afterPTRootDir}/br
codeAfterPTDir=${afterPTRootDir}/code
extractAfterPTDir=${afterPTRootDir}/extract
correspondAfterPTDir=${afterPTRootDir}/correspond
udbRootDir=${expResDir}/udb
cdRootDir=${expResDir}/cd
tfidfRootDir=${expResDir}/tfidf
tpRootDir=${expResDir}/tp

vecRootDir=${expResDir}/vec
brVecRootDir=${vecRootDir}/br
codeVecRootDir=${vecRootDir}/code

brTfidfDir=${tfidfRootDir}/br
codeTfidfDir=${tfidfRootDir}/code

vecAfterPoolingDir=${expResDir}/vecAfterPooling
brVecAfterPoolingDir=${vecAfterPoolingDir}/br
codeVecAfterPoolingDir=${vecAfterPoolingDir}/code

PYTHON=python3.7
word2vec_model_dimension=300


for proj_name in "Time"  #"Mockito"  "Lang"  "Math"  "Closure" 
do
    echo "handle project "${proj_name}"..."
    for proj_id in "Time_3" # `ls ${allMethodsDir}/${proj_name}`
    do
        echo "handle project "${proj_id}"..."
        # echo "step 1 : preprocessing for bug report and method"
        # ./run_pt.sh ${ptDir} ${bugReport4VectorDir}/${proj_name}/${proj_id} ${allMethodsDir}/${proj_name}/${proj_id} \
        #             ${gitRootDir}/${proj_id}/.git \
        #             ${brAfterPTDir}/${proj_name}/${proj_id} ${extractAfterPTDir}/${proj_name}/${proj_id} \
        #             ${correspondAfterPTDir}/${proj_name}/${proj_id} ${codeAfterPTDir}/${proj_name}/${proj_id} 
        # cd ${scriptRootDir}

        # echo "step 2 : call Java Understand to extract Call Dependency for method"
        # ./cd.sh ${allMethodsDir}/${proj_name}/${proj_id}  ${queryExpansionDir}  ${udbRootDir}/${proj_name}\
        #          ${cdRootDir}/${proj_name}  ${proj_id}  ${undDir}  ${PYTHON}
        # cd ${scriptRootDir}

        echo "step 3 : Calculate temporal proximity for all methods"
        ./tp.sh  ${correspondAfterPTDir}/${proj_name}  ${queryExpansionDir} ${tpRootDir}/${proj_name} \
                 ${proj_id} ${PYTHON}

        echo "step 4 : use deeplearning4j(word2vec) to get vectors of bug reports and methods"
        ./run_word2vec.sh ${deeplearning4jDir} ${queryExpansionDir} ${PYTHON} ${proj_id}\
                          ${brAfterPTDir}/${proj_name} ${codeAfterPTDir}/${proj_name} \
                          ${correspondAfterPTDir}/${proj_name} \
                          ${brTfidfDir}/${proj_name} ${codeTfidfDir}/${proj_name} \
                          ${brVecRootDir}/${proj_name}  ${codeVecRootDir}/${proj_name} \
                          ${word2vec_model_dimension}
        cd ${scriptRootDir}

        # echo "step 5 : query expansion for methods"
        # ./query_expansion.py


        # echo "step 6 : retrieve methods by similarity ranking on bug reports and augmented methods"
        # ./rank.py 
    done

    break 
done

