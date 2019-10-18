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

vecRootDir=${expResDir}/vec
brVecRootDir=${vecRootDir}/br
codeVecRootDir=${vecRootDir}/code

vecAfterPoolingDir=${expResDir}/vecAfterPooling
brVecAfterPoolingDir=${vecAfterPoolingDir}/br
codeVecAfterPoolingDir=${vecAfterPoolingDir}/code

PYTHON=python3.7


for proj_name in "Time"  #"Mockito"  "Lang"  "Math"  "Closure" 
do
    echo "handle project "${proj_name}"..."
    for proj_id in "Time_3" # `ls ${allMethodsDir}/${proj_name}`
    do
        echo "handle project "${proj_id}"..."
        # step 1 : preprocessing for bug report and method
        # ./run_pt.sh ${ptDir} ${bugReport4VectorDir}/${proj_name}/${proj_id} ${allMethodsDir}/${proj_name}/${proj_id} \
        #             ${gitRootDir}/${proj_id}/.git \
        #             ${brAfterPTDir}/${proj_name}/${proj_id} ${extractAfterPTDir}/${proj_name}/${proj_id} \
        #             ${correspondAfterPTDir}/${proj_name}/${proj_id} ${codeAfterPTDir}/${proj_name}/${proj_id} 
        # cd ${scriptRootDir}

        # step 2 : call Java Understand to extract Call Dependency for method
        ./und.sh ${allMethodsDir}/${proj_name}/${proj_id}  ${queryExpansionDir}  ${udbRootDir}/${proj_name}\
                 ${cdRootDir}/${proj_name}  ${proj_id}  ${undDir}  ${PYTHON}
        cd ${scriptRootDir}

        # step 3 : use deeplearning4j(word2vec) to get vectors of bug reports and methods
        # ./run_word2vec.sh ${deeplearning4jDir} ${brAfterPTDir}/${proj_name}/${proj} ${codeAfterPTDir}/${proj_name}/${proj} \
        #                   ${brVecRootDir}/${proj_name}/${proj}  ${codeVecRootDir}/${proj_name}/${proj}
        # cd ${scriptRootDir}

        # step 4 : query expansion for methods
        # ./query_expansion.py


        # step 5 : retrieve methods by similarity ranking on bug reports and augmented methods
        # ./rank.py
        break
    done

    break 
done

