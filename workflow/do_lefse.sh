#!/bin/bash

run_lefse(){

echo "#!/bin/bash
#PBS -N $1
#PBS -l nodes=1:ppn=1
#PBS -o $2
#PBS -j oe
#PBS -q silver

cd $2

source activate lefse
# 格式转换为lefse内部格式
lefse-format_input.py $1 $1.input.in -c 1 -o 1000000

# 运行lefse
run_lefse.py $1.input.in $1.input.res

# 绘制所有差异features柱状图
lefse-plot_res.py $1.input.res $1.res.pdf --format pdf --dpi 600

# 批量绘制所有差异features柱状图，慎用(几百张差异结果柱状图阅读也很困难)
mkdir -p $1.features
lefse-plot_features.py -f diff --archive none --format pdf $1.input.in $1.input.res $1.features/

" > $1.sh
qsub $1.sh
}

dir=`pwd`

for f in *.lefse
do
	run_lefse $f $dir
done
