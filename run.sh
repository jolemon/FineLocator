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
ssRootDir=${expResDir}/ss
finalRootDir=${expResDir}/final

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


for proj_name in "Mockito" # "Time" "Mockito"  "Lang"  "Math"  "Closure" 
do
    echo "handle project "${proj_name}"..."
    for proj_id in "Mockito_35" # `ls ${allMethodsDir}/${proj_name}`
    do
        echo "handle project "${proj_id}"..."
        # echo "step 1 : preprocessing for bug report and method"
        # ./run_pt.sh ${ptDir} ${bugReport4VectorDir}/${proj_name} ${allMethodsDir}/${proj_name} \
        #             ${gitRootDir}  ${proj_id} \
        #             ${brAfterPTDir}/${proj_name}  ${extractAfterPTDir}/${proj_name} \
        #             ${correspondAfterPTDir}/${proj_name} ${codeAfterPTDir}/${proj_name} 
        # cd ${scriptRootDir}

        # echo "step 2 : use deeplearning4j(word2vec) to get vectors of bug reports and methods"
        # ./run_word2vec.sh ${deeplearning4jDir} ${queryExpansionDir} ${PYTHON} ${proj_id}\
        #                   ${brAfterPTDir}/${proj_name} ${codeAfterPTDir}/${proj_name} \
        #                   ${correspondAfterPTDir}/${proj_name} \
        #                   ${brTfidfDir}/${proj_name} ${codeTfidfDir}/${proj_name} \
        #                   ${brVecRootDir}/${proj_name}  ${codeVecRootDir}/${proj_name} \
        #                   ${word2vec_model_dimension}
        # cd ${scriptRootDir}

        echo "step 3 : Calculate semantic similarity for all methods"
        ./ss.sh ${queryExpansionDir} ${codeVecRootDir}/${proj_name} ${brVecRootDir}/${proj_name} \
                ${ssRootDir}/${proj_name} ${proj_id} ${word2vec_model_dimension} ${PYTHON} 
        cd ${scriptRootDir}

        # echo "step 4 : Calculate temporal proximity for all methods"
        # ./tp.sh  ${queryExpansionDir} ${correspondAfterPTDir}/${proj_name} ${tpRootDir}/${proj_name} \
        #          ${proj_id} ${PYTHON}
        # cd ${scriptRootDir}

        # echo "step 5 : use Java Understand to extract Call Dependency for method"
        # ./cd.sh ${allMethodsDir}/${proj_name}/${proj_id}  ${queryExpansionDir}  ${udbRootDir}/${proj_name}\
        #          ${cdRootDir}/${proj_name}  ${proj_id}  ${undDir}  ${PYTHON}
        # cd ${scriptRootDir}

        echo "step 6 : query expansion , ranking on bug reports and augmented methods"
        ./query_expansion.sh ${queryExpansionDir} ${codeVecRootDir}/${proj_name} ${brVecRootDir}/${proj_name} \
                             ${finalRootDir}/${proj_name} ${proj_id} ${word2vec_model_dimension} ${PYTHON} \
                             ${ssRootDir}/${proj_name} ${tpRootDir}/${proj_name} ${cdRootDir}/${proj_name} \
                             ${linkedBugMethodsDir}/${proj_name}_bugId_buggyMethodsName
        cd ${scriptRootDir}

    done

    break 
done

