#!/bin/bash
#run: ./cal_HitK-MAP-MRR.sh ${repo_predictRes} 
# predictResult=$1
# Time Mockito Lang Math Closure
proj=$1
dim=300       #$2
epochs=10     #$3
final_dir=/data/expRes/final   #$5
divide=$2    #$4

dir=${final_dir}/${proj}/${proj}_*_${dim}_${epochs}_${divide}

predictRes=${proj}_${dim}_${epochs}_${divide}

function cal_hitK_MAP_MRR(){
    rankRes=$1 #data file format: bugid, rank (started with 0)
    map=$(awk -F "," '{brCnt[$1]=1;hit[$1]+=1;eachPreci[$1]+=hit[$1]/($2+1);}END{for(i in brCnt){sum+=eachPreci[i]/hit[i]}print "MAP:"sum/length(brCnt)}' $rankRes)
    echo $map
    mrr=$(awk -F "," 'BEGIN{arr[a]=1}{if($1 in arr){if(($2+1)<arr[$1]){arr[$1]=($2+1)}}else{arr[$1]=($2+1)}}END{for(i in arr){s+=1/arr[i];n+=1}print "MRR:"(s-1)/(n-1)}' $rankRes)
    echo $mrr
    for k in 1 5 10 20 #`seq 1 20`
    do
        hitK=$(awk -F "," -v topk="$k" '{brr[$1]=1;if(($2+1)<=topk)arr[$1]=1}END{print "Hit-"topk":"length(arr)/length(brr)}' $rankRes)
        echo $hitK
    done
}

function hitK_MAP_MRR4repos(){
    predictRes=$1
    res_file=${predictRes}_res
    echo "MAP, MRR, Hit-K for $predictRes saved to $res_file."
    sort -k 1,1 -k 2,2r -t "$" $predictRes | awk -F "$" 'BEGIN{arr[0]=1;idx=0}{if($1 in arr){idx+=1}else{idx=0;arr[$1]=0}if($3==1){print $1","idx}}' > tmpres
    cal_hitK_MAP_MRR tmpres > ${res_file}
    rm tmpres
} 


# cat $dir > $predictRes 


for file in `ls $dir`
do
    cat $file >> $predictRes
    echo >> $predictRes
done

hitK_MAP_MRR4repos ${predictRes}
rm $predictRes
