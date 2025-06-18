#!/bin/bash


THREADS=1
REF=/home/shileisheng/reference/16S/rdp_gold.fa
PERL=$(which perl)
VSEARCH=$(which vsearch)

echo Checking FASTQ format version for one file

time $VSEARCH --fastq_chars $(ls -1 *.fastq | head -1)


for f in *_R1_*.fastq
do
    r=${f/_R1_/_R2_} 
    s=${f/_*/}
	
	$VSEARCH --fastq_mergepairs $f \
        --threads $THREADS \
        --reverse $r \
        --fastq_minovlen 10 \
        --fastq_maxdiffs 10 \
		--fastq_minmergelen 300 \
		--fastq_maxmergelen 500 \
        --fastqout $s.merged.fastq \
        --fastq_eeout

    echo Calculate quality statistics
	
	$VSEARCH --fastq_eestats $s.merged.fastq \
        --output $s.stats

	echo
    echo Quality filtering

	$VSEARCH --fastq_filter $s.merged.fastq \
        --fastq_maxee 0.5 \
        --fastq_minlen 350 \
        --fastq_maxlen 450 \
        --fastq_maxns 0 \
        --fastaout $s.filtered.fasta \
        --fasta_width 0
	
	echo
    echo Dereplicate at sample level and relabel with sample_n

	$VSEARCH --derep_fulllength $s.filtered.fasta \
        --strand plus \
        --output $s.derep.fasta \
        --sizeout \
        --uc $s.derep.uc \
        --relabel $s. \
        --fasta_width 0
done

echo Sum of unique sequences in each sample: $(cat *.derep.fasta | grep -c "^>")

# At this point there should be one fasta file for each sample                  
# It should be quality filtered and dereplicated.
echo
echo Merge all samples

rm -f all.derep.fasta all.nonchimeras.derep.fasta
cat *.derep.fasta > all.fasta

echo Dereplicate across samples and remove singletons

$VSEARCH --derep_fulllength all.fasta \
    --minuniquesize 2 \
    --sizein \
    --sizeout \
    --fasta_width 0 \
    --uc all.derep.uc \
    --output all.derep.fasta

echo Unique non-singleton sequences: $(grep -c "^>" all.derep.fasta)

echo
echo Cluster sequences using VSEARCH

$VSEARCH --cluster_size all.derep.fasta \
    --threads $THREADS \
    --id 0.97 \
    --strand plus \
    --sizein \
    --sizeout \
    --fasta_width 0 \
    --centroids centroids.fasta

echo
echo Clusters: $(grep -c "^>" centroids.fasta)

echo Sort and remove singletons
echo

$VSEARCH --sortbysize centroids.fasta \
    --threads $THREADS \
    --sizein \
    --sizeout \
    --fasta_width 0 \
    --minsize 2 \
    --output sorted.fasta

echo
echo Non-singleton clusters: $(grep -c "^>" sorted.fasta)

echo De novo chimera detection
echo

$VSEARCH --uchime_denovo sorted.fasta \
    --sizein \
    --sizeout \
    --fasta_width 0 \
    --qmask none \
    --nonchimeras denovo.nonchimeras.fasta \

echo
echo Unique sequences after de novo chimera detection: $(grep -c "^>" denovo.nonchimeras.fasta)

echo Reference chimera detection
echo

$VSEARCH --uchime_ref denovo.nonchimeras.fasta \
    --threads $THREADS \
    --db $REF \
    --sizein \
    --sizeout \
    --fasta_width 0 \
    --qmask none \
    --dbmask none \
    --nonchimeras nonchimeras.fasta

echo
echo Unique sequences after reference-based chimera detection: $(grep -c "^>" nonchimeras.fasta)

echo Relabel OTUs
echo

$VSEARCH --fastx_filter nonchimeras.fasta \
    --threads $THREADS \
    --sizein \
    --sizeout \
    --fasta_width 0 \
    --relabel OTU_ \
    --fastaout otus.fasta

echo Number of OTUs: $(grep -c "^>" otus.fasta)

echo Map sequences to OTUs by searching
echo

$VSEARCH --usearch_global all.fasta \
    --threads $THREADS \
    --db otus.fasta \
    --id 0.97 \
    --strand plus \
    --sizein \
    --sizeout \
    --fasta_width 0 \
    --qmask none \
    --dbmask none \
    --otutabout otutab.txt
echo
echo Sort OTU table numerically

sort -k1.5n otutab.txt > otutab.sorted.txt

echo Done

date

