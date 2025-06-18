#!/bin/bash
#PBS -N blastdb_2_fa
#PBS -l nodes=1:ppn=4
#PBS -j oe
#PBS -p 100
#PBS -q GPUfat


cd /histor/sun/wangtao/0_user/3_shixh/shileisheng/reference/NCBI_nt_fa

for id in 2 10239 4751 2157
do
    taxonkit list --ids $id --indent "" > $id.taxid.txt

    /histor/sun/wangtao/3_software/anaconda3/envs/biobakery3/bin/blastdbcmd -db /histor/sun/wangtao/0_user/3_shixh/shileisheng/reference/NCBI_nt/nt -entry all -outfmt "%a %T" | csvtk grep -d ' ' -D $'\t' -f 2 -P $id.taxid.txt  > $id.acc2taxid.txt

	cut -f 1 $id.acc2taxid.txt > $id.acc.txt

   /histor/sun/wangtao/3_software/anaconda3/envs/biobakery3/bin/blastdbcmd -db /histor/sun/wangtao/0_user/3_shixh/shileisheng/reference/NCBI_nt/nt -entry_batch $id.acc.txt -out  nt.$id.fa
done

