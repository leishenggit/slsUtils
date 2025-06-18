#!/bin/bash
#PBS -N kraken2.contigs
#PBS -l nodes=1:ppn=15
#PBS -j oe
#PBS -q middle

cd /histor/sun/wangtao/0_user/3_shixh/shileisheng/20201020_virus/do_megahit

for sample in `cut -f 1 ../meta.txt|sed '1d'`
do
	time kraken2 --db /histor/sun/wangtao/0_user/3_shixh/shileisheng/reference/kraken_db_nt_bv \
					--threads 15 \
					--output $sample.out \
					--report $sample.report \
					$sample/final.contigs.fa
	echo "finish kraken2 $sample"
done

/histor/sun/maofb/anaconda3/envs/R4.0.2/bin/Rscript merge.sls.R --input *.out --out contig_taxonomy.txt

/histor/sun/wangtao/0_user/3_shixh/shileisheng/python_script/filter.py --taxid 2  --taxid_col 4 --head contig_taxonomy.txt > B.contig_taxonomy.txt
/histor/sun/wangtao/0_user/3_shixh/shileisheng/python_script/filter.py --taxid 10239  --taxid_col 4 --head contig_taxonomy.txt > V.contig_taxonomy.txt
/histor/sun/wangtao/0_user/3_shixh/shileisheng/python_script/filter.py --taxid 10239 2 --taxid_col 4 --head contig_taxonomy.txt > BV.contig_taxonomy.txt

