#!/bin/bash

function do_qc(){

sample=$1

echo "#!/bin/bash
#PBS -N $sample.megahit
#PBS -q silver
#PBS -j oe
#PBS -l nodes=1:ppn=8,walltime=1000:00:00

cd /histor/sun/wangtao/0_user/3_shixh/shileisheng/20201020_virus/do_megahit

time /histor/sun/maofb/anaconda3/bin/megahit -1 /histor/sun/wangtao/0_user/3_shixh/shileisheng/20201020_virus/do_qc/$sample/virus.fq.1.gz -2 /histor/sun/wangtao/0_user/3_shixh/shileisheng/20201020_virus/do_qc/$sample/virus.fq.2.gz -o $sample --num-cpu-threads 10 --min-contig-len 300

" > $sample.megahit.sh
echo $sample
qsub $sample.megahit.sh
}


for sample in `cut -f 1 ../meta.txt|sed 1d`
do
	do_qc $sample
done

### check whether jobs run success
#for dir in `cut -f 1 ../meta.txt|sed 1d`;do if [ -e $dir/final.contigs.fa ];then echo $dir; fi done > samples.done
#awk 'NR==FNR{a[$1]=0}NR>FNR{if($1 in a)next;print}' samples.done samples > samples.to.run

#contigs number 
for f in `cut -f 1 ../meta.txt|sed 1d`; do info=`grep "contigs, total" $f/log`; echo -e $f"\t"$info; done | awk -v OFS='\t' '{print $1,$5}'> contig.count.res.txt

#contigs length
for f in `cut -f 1 ../meta.txt|sed 1d`; do grep "^>" $f/final.contigs.fa | awk -v OFS='\t' -v sample=$f '{print sample,substr($1,2), substr($NF,5)}';done > contig.len.res.txt
