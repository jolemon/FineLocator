#!/bin/bash
deeplearning4jdir=$1
brAfterPTDir=$2
codeAfterPTDir=$3
brVecDir=$4
codeVecDir=$5
proj_id=$6

function runWord2Vec(){
    rm -rf ${brVecDir}/${proj_id}
    rm -rf ${codeVecDir}/${proj_id}
    # mkdir -p ${brVecDir}/${proj_id}
    mkdir -p ${codeVecDir}/${proj_id}
     
    echo "train word2vec model.."
    copyBrBeforeFit
    java -cp word2vec.jar App -source ${codeAfterPTDir}/${proj_id} --fit 1
    clearTmpDir
    echo "train word2vec model finished."

    echo "export br vector..."
    java -cp word2vec.jar App -source ${brAfterPTDir}/${proj_id}   -target ${brVecDir}/${proj_id}   
    echo "export br vector finished."

    echo "export code vector..."
    java -cp word2vec.jar App -source ${codeAfterPTDir}/${proj_id} -target ${codeVecDir}/${proj_id}
    echo "export code vector finished."
}

function copyBrBeforeFit(){
	array=($(ls ${brAfterPTDir} | sort -t "_" -k 2n))
	for ((i=0;i<${#array[*]};i++))
    do
        if [[ "${array[i]}" == "${proj_id}" ]]; then 
    	    rm   -rf ${codeAfterPTDir}/${proj_id}/tmp
            mkdir -p ${codeAfterPTDir}/${proj_id}/tmp
            for ((j=0;j<=$i;j++))
            do
                cp ${brAfterPTDir}/${array[j]} ${codeAfterPTDir}/${proj_id}/tmp
            done
            break
        fi
    done
}

function clearTmpDir(){
	rm -rf ${codeAfterPTDir}/${proj_id}/tmp
}


cd ${deeplearning4jdir}

runWord2Vec
# clearTmpDir


