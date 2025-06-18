#!/bin/bash
#PBS -N make_kraken2_db
#PBS -l nodes=1:ppn=20
#PBS -j oe
#PBS -q GPUfat
set -e

cd /histor/sun/maofb/shileisheng/reference/NCBI_nt_fa

for f in nt.10239.fa
do
	kraken2-build --add-to-library $f --db /histor/sun/maofb/shileisheng/reference/kraken_db_nt_bv
done

kraken2-build --build --db /histor/sun/maofb/shileisheng/reference/kraken_db_nt_bv --threads 20
bracken-build -d /histor/sun/maofb/shileisheng/reference/kraken_db_nt_bv -t 20 -k 35 -l 150

for f in nt.4751.fa
do
	kraken2-build --add-to-library $f --db /histor/sun/maofb/shileisheng/reference/kraken_db_nt_bf
done

kraken2-build --build --db /histor/sun/maofb/shileisheng/reference/kraken_db_nt_bf --threads 20
bracken-build -d /histor/sun/maofb/shileisheng/reference/kraken_db_nt_bf -t 20 -k 35 -l 150

