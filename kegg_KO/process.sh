python json2tsv.py > ko00001.tsv

python taxonomy.py ko00001.tsv | sort -u > taxonomy.tbl

awk -F'\t' '$2=="level_4"' taxonomy.tbl | cut -f 4 | sed 's/:/\t/g' | awk '$1!="09180" && $1!="09190"' > id_map.tbl

cut -f 2,4 id_map.tbl | sort -u > level_2.txt
cut -f 3,4 id_map.tbl | sort -u > level_3.txt
cut -f 1,4 id_map.tbl | sort -u > level_1.txt

cut -f 1,3 taxonomy.tbl | sort -u > id_name.txt

#======= specific to Metabolism 09100
awk '$1=="09100"' id_map.tbl | cut -f 2,4 | sort -u > Metabolism.level_2.txt
awk '$1=="09100"' id_map.tbl | cut -f 3,4 | sort -u > Metabolism.level_3.txt

