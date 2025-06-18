#!/bin/bash

for f in *.rma6; do /usr/local/megan/tools/rma2info -c2c Taxonomy -i $f > $f.out;done
/home/shileisheng/python_script/summerized.1.py *.rma6.out > summerized.log 2>&1 &
wait
/home/shileisheng/anaconda3/envs/R3.6/bin/Rscript /home/shileisheng/R_script/merge_blast_tax.R *.tax.txt  --out merged.tax.txt
bash /home/shileisheng/shell_script/tax.sh merged.tax.txt

