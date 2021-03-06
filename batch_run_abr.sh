#!/bin/bash

. input.properties 

ptDir=${scriptRootDir}/pt
deeplearning4jDir=${scriptRootDir}/word2vec
queryExpansionDir=${scriptRootDir}/queryexpansion 
expResDir=${expResParentDir}/expRes
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
predictResRootDir=${expResDir}/res

vecRootDir=${expResDir}/vec
brVecRootDir=${vecRootDir}/br
codeVecRootDir=${vecRootDir}/code

brTfidfDir=${tfidfRootDir}/br
codeTfidfDir=${tfidfRootDir}/code

vecAfterPoolingDir=${expResDir}/vecAfterPooling
brVecAfterPoolingDir=${vecAfterPoolingDir}/br
codeVecAfterPoolingDir=${vecAfterPoolingDir}/code

buggy_version_file=${queryExpansionDir}/batch_process/all_buggy_version

PYTHON=python3.7
word2vec_model_dimension=200
word2vec_model_epochs=30
proj=$1

source activate FineLocator
for proj_name in $proj # "Time" "Mockito" "Math"  "Closure" "Lang" 
do
    echo "handle project "${proj_name}"..."
    for proj_id in `ls ${allMethodsDir}/${proj_name}`
    do
        echo "handle project "${proj_id}"..."
        begin_time=$(date  "+%Y/%m/%d-%H:%M:%S")
        echo "begin time:" ${begin_time}
        cd ${scriptRootDir}

        echo "step 2 : use deeplearning4j(word2vec) to get vectors of bug reports and methods"
        ./run_word2vec.sh ${deeplearning4jDir} ${queryExpansionDir} ${PYTHON} ${proj_id}\
                          ${brAfterPTDir}/${proj_name} ${codeAfterPTDir}/${proj_name} \
                          ${correspondAfterPTDir}/${proj_name} \
                          ${brTfidfDir}/${proj_name} ${codeTfidfDir}/${proj_name} \
                          ${brVecRootDir}/${proj_name}  ${codeVecRootDir}/${proj_name} \
                          ${word2vec_model_dimension}  ${word2vec_model_epochs}
        cd ${scriptRootDir}

        echo "step 3 : Calculate semantic similarity for all methods"
        ./ss.sh ${queryExpansionDir} ${codeVecRootDir}/${proj_name}  \
                ${ssRootDir}/${proj_name} ${proj_id} ${word2vec_model_dimension} ${PYTHON} 
        cd ${scriptRootDir}

        echo "step 4 : Calculate temporal proximity for all methods"
        ./tp.sh  ${queryExpansionDir} ${correspondAfterPTDir}/${proj_name} ${tpRootDir}/${proj_name} \
                 ${ssRootDir}/${proj_name} ${proj_id} ${PYTHON}
        cd ${scriptRootDir}


        for((a=3;a<=5;a+=1))
        do
            for((b=1;b<10-$a;b+=1))
            do 
                r=$((10-$a-$b))
               	if [[ $r -ge 0 ]]; then 
                    alpha=`echo "scale=1;res=$a/10;if(length(res)==scale(res)) print 0;print res"| bc` 
                    beta=`echo "scale=1;res=$b/10;if(length(res)==scale(res)) print 0;print res"| bc`
                    gamma=`echo "scale=1;res=$r/10;if(length(res)==scale(res)) print 0;print res"| bc` 
               	    echo "step 6 : query expansion , ranking on bug reports and augmented methods. alpha=${alpha}, beta=${beta}, gamma=${gamma}"
                    ./query_expansion.sh ${queryExpansionDir} ${codeVecRootDir}/${proj_name} ${brVecRootDir}/${proj_name} \
                             ${finalRootDir}/${proj_name} ${proj_id} ${word2vec_model_dimension}  ${word2vec_model_epochs} ${PYTHON} \
                             ${ssRootDir}/${proj_name} ${tpRootDir}/${proj_name} ${cdRootDir}/${proj_name} \
                             ${linkedBugMethodsDir}/${proj_name}_bugId_buggyMethodsName \
                             ${alpha} ${beta} ${gamma}
                    cd ${scriptRootDir}
	        fi 
            done
        done

        end_time=$(date  "+%Y/%m/%d-%H:%M:%S")
        echo "begin time: "${begin_time}"  end time:" ${end_time}
   done
done
source deactivate FineLocator
