#!/bin/bash

python parser_metaCyc.py --html sojson.com_.js 

awk -F'\t' '{print NF}'  metaCyc.txt | sort | uniq -c

awk -F'\t' -v OFS='\t' 'NR==FNR{a[$1]=0}NR>FNR{if($NF in a)print $0}' ~/reference/utility_mapping/metacyc_pathways_structured_filtered ~/reference/metaCyc/metaCyc.txt > metacyc_humann2.txt

awk -F'\t' -v OFS='\t' 'NF>1{print $1, $NF}' metacyc_humann2.txt > level_1.txt
awk -F'\t' -v OFS='\t' 'NF>2{print $2, $NF}' metacyc_humann2.txt > level_2.txt 

sed -E -i  's/[(][0-9]+.*[)]//' metaCyc_id_name.txt 

awk -F'\t' -v OFS='\t' 'NR==FNR{name[$1]=$2}NR>FNR{print $2, name[$1]}' metaCyc_id_name.txt level_2.txt | awk '!a[$1]++' > level_2.name.txt
