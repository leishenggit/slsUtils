#!/bin/bash
#PBS -N do_cherry
#PBS -l nodes=1:ppn=15
#PBS -j oe
#PBS -q middle

cd /histor/sun/wangtao/0_user/3_shixh/shileisheng/20201020_virus/do_megahit
##filter out all RNA virus contigs
../../python_script/filter.py --taxid 2559587  --taxid_col 4 V.contig_taxonomy.txt --head > 2559587.txt
awk -F'\t' -v OFS='\t' 'NR==FNR{a[$4]=0}NR>FNR{if($4 in a)next;print $0}' 2559587.txt V.contig_taxonomy.txt  > V.contig_taxonomy.1.txt
##get all virus contigs to Predicting host for viruses
awk -F'\t' -v OFS='\t' '{ref=$1".virus.contigs";print $3 > ref}' V.contig_taxonomy.1.txt
for sample in `cut -f 1 ../meta.txt|sed '1d'`;do seqkit grep -f $sample.virus.contigs $sample/final.contigs.fa > $sample.virus.contigs.fa; done
for sample in `cut -f 1 ../meta.txt|sed '1d'`;do awk -v filename=$sample '{if($1 ~ "^>")$1=$1"_"filename;print $0;}' $sample.virus.contigs.fa ;done > all.virus.contigs.fa
awk -F'\t' -v OFS='\t' '{print $3"_"$1,$0}' V.contig_taxonomy.1.txt > V.contig_taxonomy.2.txt

source activate cherry

cd /histor/sun/wangtao/0_user/3_shixh/shileisheng/software/CHERRY-main/

time python run_Speed_up.py --contigs /histor/sun/wangtao/0_user/3_shixh/shileisheng/20201020_virus/do_megahit/all.virus.contigs.fa  --mode virus --len 8000 --model pretrain --topk 1 --t 15

awk -F'\t' -v OFS='\t' 'NR==FNR{tax[$1]=$5}NR>FNR&&FNR==1{print "taxid",$0}NR>FNR&&FNR>1{print tax[$1],$0}' V.contig_taxonomy.2.txt final_prediction.csv > final_prediction.1.csv

awk -F'\t' -v OFS='\t' 'NR==FNR{name[$1]=$3;rank[$1]=$2}NR>FNR&&FNR==1{print "rank","name",$0}NR>FNR&&FNR>1{print rank[$1],name[$1],$0}' ../../reference/taxonomy/taxonomy.tbl final_prediction.1.csv > final_prediction.2.csv



