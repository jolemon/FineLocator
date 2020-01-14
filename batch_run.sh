#!/bin/bash

. input.properties 

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
word2vec_model_epochs=10

for proj_name in  "Mockito" # "Time" "Mockito"  "Lang"  "Math"  "Closure" 
do
    echo "handle project "${proj_name}"..."
    for proj_id in `ls ${allMethodsDir}/${proj_name}`
    do
    	echo "handle project "${proj_id}"..."
        begin_time=$(date  "+%Y/%m/%d-%H:%M:%S")
        echo "begin time:" ${begin_time}
        cd ${scriptRootDir}
    #    echo "Common Step 1 : preprocessing for bug report and method"
    #    ./run_pt.sh ${ptDir} ${bugReport4VectorDir}/${proj_name} ${allMethodsDir}/${proj_name} \
    #                ${gitRootDir}  ${proj_id} \
    #                ${brAfterPTDir}/${proj_name}  ${extractAfterPTDir}/${proj_name} \
    #                ${correspondAfterPTDir}/${proj_name} ${codeAfterPTDir}/${proj_name}  
    #	echo "Common Step 2 : calculate time proximity"
    #    cd ${scriptRootDir} 
    #    ./tp.sh  ${queryExpansionDir} ${correspondAfterPTDir}/${proj_name} ${tpRootDir}/${proj_name} \
    #             ${proj_id} ${PYTHON}
    #    echo "Common Step 3 : calculate call dependency"
    #    cd ${scriptRootDir}
    #    ./cd.sh ${allMethodsDir}/${proj_name}/${proj_id}  ${queryExpansionDir} ${udbCreateDir} ${udbRootDir}/${proj_name} \
    #             ${cdRootDir}/${proj_name}  ${proj_id}  ${undDir} ${undAPIPath} ${PYTHON}
    #    echo "Step 3 : train word2vec to get vector and further to obtain semantic similarities between method pairs"
    #    cd ${scriptRootDir}
    #    for((dimension=100;dimension<=500;dimension+=100))
    #    do
    #    	echo "train word2vec model to get vector with dimension ${dimension}"
    #    	./run_word2vec.sh ${deeplearning4jDir} ${queryExpansionDir} ${PYTHON} ${proj_id}\
    #                      ${brAfterPTDir}/${proj_name} ${codeAfterPTDir}/${proj_name} \
    #                      ${correspondAfterPTDir}/${proj_name} \
    #                      ${brTfidfDir}/${proj_name} ${codeTfidfDir}/${proj_name} \
    #                      ${brVecRootDir}/${proj_name}  ${codeVecRootDir}/${proj_name} \
    #                      ${dimension}  ${word2vec_model_epochs}
    #        cd ${scriptRootDir}

    #        echo "Calculate semantic similarity with dimension ${dimension}"
    #        ./ss.sh ${queryExpansionDir} ${codeVecRootDir}/${proj_name}  \
    #            ${ssRootDir}/${proj_name} ${proj_id} ${dimension} ${PYTHON} 
    #        cd ${scriptRootDir}
            
            echo "query expansion , ranking on bug reports and augmented methods. alpha=${alpha}, beta=${beta}, gamma=${gamma}"
            
            for((a=1;a<=10;a+=1))
            do
                for((b=1;b<=10-$a;b+=1))
                do 
                	r=$((10-$a-$b))
                	if [[ $r -ge 0 ]]; then 
                	    alpha=`echo "scale=1;res=$a/10;if(length(res)==scale(res)) print 0;print res"| bc` 
                	    beta=`echo "scale=1;res=$b/10;if(length(res)==scale(res)) print 0;print res"| bc`
                	    gamma=`echo "scale=1;res=$r/10;if(length(res)==scale(res)) print 0;print res"| bc` 
                            ./query_expansion.sh ${queryExpansionDir} ${codeVecRootDir}/${proj_name} ${brVecRootDir}/${proj_name} \
                            ${finalRootDir}/${proj_name} ${proj_id} ${word2vec_model_dimension}  ${word2vec_model_epochs} ${PYTHON} \
                            ${ssRootDir}/${proj_name} ${tpRootDir}/${proj_name} ${cdRootDir}/${proj_name} \
                            ${linkedBugMethodsDir}/${proj_name}_bugId_buggyMethodsName \
                            ${alpha} ${beta} ${gamma}
			    cd ${scriptRootDir} 
                	fi 
                done
            done
            # echo "clear large file ss."
            # rm -f ${ssRootDir}/${proj_name}/${proj_id}*
        # done
        # echo "clear large file tp."
        # rm -f ${tpRootDir}/${proj_name}/${proj_id}*
    done
done
