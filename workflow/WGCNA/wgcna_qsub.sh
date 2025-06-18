#!/bin/bash

if false;then
./GTEx_summary.py "Adrenal Gland" > Adrenal_Gland.rpkm.txt
./GTEx_summary.py "Bladder" > Bladder.rpkm.txt 
./GTEx_summary.py "Brain - Amygdala" > Brain_Amygdala.rpkm.txt
./GTEx_summary.py "Breast - Mammary Tissue" > Breast_Mammary_Tissue.rpkm.txt
./GTEx_summary.py "Colon - Sigmoid" > Colon_Sigmoid.rpkm.txt
./GTEx_summary.py "Colon - Transverse" > Colon_Transverse.rpkm.txt
./GTEx_summary.py "Esophagus - Gastroesophageal Junction" > Esophagus_Gastroesophageal_Junction.rpkm.txt
./GTEx_summary.py "Kidney - Cortex" > Kidney_Cortex.rpkm.txt
./GTEx_summary.py "Liver" > Liver.rpkm.txt
./GTEx_summary.py "Lung" > Lung.rpkm.txt
./GTEx_summary.py "Ovary" > Ovary.rpkm.txt
./GTEx_summary.py "Pancreas" > Pancreas.rpkm.txt
./GTEx_summary.py "Prostate" > Prostate.rpkm.txt
./GTEx_summary.py "Skin - Not Sun Exposed (Suprapubic)" > Skin_Not_Sun_Exposed_Suprapubic.rpkm.txt
./GTEx_summary.py "Stomach" > Stomach.rpkm.txt
./GTEx_summary.py "Testis" > Testis.rpkm.txt
./GTEx_summary.py "Thyroid" > Thyroid.rpkm.txt
./GTEx_summary.py "Uterus" > Uterus.rpkm.txt
./GTEx_summary.py "Whole Blood" > Whole_Blood.rpkm.txt
fi

for f in /histor/sun/maofb/shileisheng/WGCNA/*.rpkm.txt
do
fname=`basename $f`
path="/histor/sun/maofb/shileisheng/WGCNA"

echo "#!/bin/bash
#PBS -N $fname.wgcna
#PBS -l nodes=1:ppn=26
#PBS -o $path
#PBS -j oe
#PBS -q middle

Rscript /histor/sun/maofb/shileisheng/WGCNA/my_wgcna.r $f $path
" > $path/${fname%%.*}.sh
#qsub  $path/${fname%%.*}.sh
done

