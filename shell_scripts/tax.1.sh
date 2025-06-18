#!/bin/bash

input=$1

awk -F'\t'  -v OFS='\t' 'NR==FNR{tax[$1]=$0}NR>FNR&&FNR==1{$1="path";print "taxid","rank","tax_name",$0}NR>FNR&&FNR>1{if($1 in tax){$1=tax[$1];print $0;}else{next}}' /Newdata/home/zhongjx/kraken/nt2107/taxonomy/taxonomy.tbl $input > $input.1 

/home/shileisheng/python_script/filter.py $input.1 --taxid 2  2157 4751 10239  --head > $input.1.ABFV

