 #!/bin/bash
# ls expRes/afterPT/br/Time | sort -t "_" -k 2n
array=($(ls expRes/afterPT/br/Time | sort -t "_" -k 2n))

for ((i=0;i<${#array[*]};i++))
do
    if [[ "${array[i]}" == "Time_25" ]]; then 
    	rm -rf expRes/afterPT/tmp
        mkdir -p expRes/afterPT/tmp 
        echo $i
        for ((j=0;j<=$i;j++))
        do
            cp expRes/afterPT/br/Time/${array[j]} expRes/afterPT/tmp
        done
        break
    fi
done