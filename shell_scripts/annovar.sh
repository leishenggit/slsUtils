perl /home/shileisheng/software/annovar/annotate_variation.pl \
	--buildver MN908947 \
	--geneanno \
	--outfile $1.annotation.txt \
	--dbtype refGene \
	--hgvs \
	$1 \
	/home/shileisheng/software/annovar/ncov/

