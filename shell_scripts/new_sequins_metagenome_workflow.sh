#!/bin/bash

if [ $# -ne 2 ];then
echo "Need 2 arguments, first is a R1 fq; second is R2"
exit 500
fi

dir=`dirname $1`

#fastp去除polyG
fastp --in1 $1 --out1 $dir/R1fastp.gz --in2 $2 --out2 $dir/R2fastp.gz --unpaired1 $dir/fastpunpaired.gz --unpaired2 $dir/fastpunpaired.gz -Q -l 50 -A -g -w 16

#BBDuk: 过滤低复杂度序列
bbduk.sh in1=$dir/R1fastp.gz in2=$dir/R2fastp.gz out1=$1.bbduk out2=$2.bbduk entropy=0.7 entropywindow=50 entropyk=5 -Xmx30g

bbduk.sh in1=$dir/fastpunpaired.gz out1=$dir/fastpunpaired.gz.bbduk entropy=0.7 entropywindow=50 entropyk=5 -Xmx30g
rm -f $dir/fastpunpaired.gz $dir/R1fastp.gz $dir/R2fastp.gz

#flash: merge 重叠序列
flash -z -M 150 -o flash -d $dir -t 20 $1.bbduk  $2.bbduk
rm $dir/flash.hist $dir/flash.histogram

#Trimmomatic: 去接头
java -jar /software/Trimmomatic-0.36/trimmomatic-0.36.jar PE\
	-threads 30\
	-phred33\
	$dir/flash.notCombined_1.fastq.gz\
	$dir/flash.notCombined_2.fastq.gz\
	$1.trimmomatic.1p.fq.gz\
	$1.trimmomatic.1s.fq.gz\
	$2.trimmomatic.2p.fq.gz\
	$2.trimmomatic.2s.fq.gz\
	ILLUMINACLIP:/software/Trimmomatic-0.36/adapters/TruSeq3-PE-2.fa:2:30:6 LEADING:3 TRAILING:3 SLIDINGWINDOW:4:10 MINLEN:70
	
rm -f $dir/flash.notCombined_1.fastq.gz $dir/flash.notCombined_2.fastq.gz $2.bbduk $1.bbduk
gunzip -f $1.trimmomatic.1p.fq.gz $1.trimmomatic.1s.fq.gz $2.trimmomatic.2p.fq.gz $2.trimmomatic.2s.fq.gz $dir/flash.extendedFrags.fastq.gz

java -jar /software/Trimmomatic-0.36/trimmomatic-0.36.jar SE\
	-threads 30\
	-phred33\
	$dir/fastpunpaired.gz.bbduk\
	$dir/fastpunpaired.trimmomatic.fq.gz\
	ILLUMINACLIP:/software/Trimmomatic-0.36/adapters/TruSeq3-SE-2.fa:2:30:6 LEADING:3 TRAILING:3 SLIDINGWINDOW:4:10 MINLEN:70
rm -f $dir/fastpunpaired.gz.bbduk
gunzip -f $dir/fastpunpaired.trimmomatic.fq.gz

#把所有未配对的reads合并起来
#flash.extendedFrags.fastq是merge起来的reads，不用去接头？
cat $1.trimmomatic.1s.fq $2.trimmomatic.2s.fq $dir/flash.extendedFrags.fastq $dir/fastpunpaired.trimmomatic.fq > $dir/sh.bm

rm -f $1.trimmomatic.1s.fq $2.trimmomatic.2s.fq $dir/flash.extendedFrags.fastq $dir/fastpunpaired.trimmomatic.fq

#把双端reads叠起来
/software/sortmerna-2.1b/scripts/merge-paired-reads.sh $1.trimmomatic.1p.fq $2.trimmomatic.2p.fq $dir/ph.bm

seqp=`wc -l $dir/ph.bm | cut -d' ' -f 1`
seqs=`wc -l $dir/sh.bm | cut -d' ' -f 1`
let sizep=$seqp/8
let sizes=$seqs/4
echo $sizep paired reads, $sizes single reads

##ANAQUIN
#paired-reads
~/decontamination/Anaquin/anaquin meta -t 24 -o $dir/anaquin_results_paired -1 $1.trimmomatic.1p.fq -2 $2.trimmomatic.2p.fq --mix C
#single reads
~/decontamination/Anaquin/anaquin meta -t 24 -o $dir/anaquin_results_single -1 $dir/sh.bm --mix C

#sample-reads进行物种分类
#Kraken2比对
#把paired-reads转成ph.bm
gunzip $dir/anaquin_results_paired/meta_sample_1.fq.gz $dir/anaquin_results_paired/meta_sample_2.fq.gz
/software/sortmerna-2.1b/scripts/merge-paired-reads.sh $dir/anaquin_results_paired/meta_sample_1.fq $dir/anaquin_results_paired/meta_sample_2.fq $dir/sample_ph.bm
#使用脚本对ph的R1R2转换为R1NNNNNNR2
python /home/shileisheng/python_script/concatenate.py $dir/sample_ph.bm
#合并sh ph
gunzip $dir/anaquin_results_single/meta_sample_1.fq.gz
cat $dir/anaquin_results_single/meta_sample_1.fq $dir/sample_ph.bm.concatenate > $dir/sample_shph.fastq

kraken2 --db /home/shileisheng/software/kraken2/kraken2_database/ \
	--threads 30 --use-names --report $dir/shph_kraken_report.txt \
	--classified-out $dir/kraken_classified#.txt --unclassified-out $dir/kraken_unclassified#.txt \
	--output $dir/shph.krk $dir/sample_shph.fastq

rm -f $dir/sample_shph.fastq $dir/sample_ph.bm.concatenate












