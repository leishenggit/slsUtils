#!/bin/bash
#PBS -N Uterus.rpkm.txt.wgcna
#PBS -l nodes=1:ppn=26
#PBS -o /histor/sun/maofb/shileisheng/WGCNA
#PBS -j oe
#PBS -q middle

Rscript /histor/sun/maofb/shileisheng/WGCNA/my_wgcna.r /histor/sun/maofb/shileisheng/WGCNA/Uterus.rpkm.txt /histor/sun/maofb/shileisheng/WGCNA

