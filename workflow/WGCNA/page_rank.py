# -*- coding: utf-8 -*-
"""
使用networkX库实现pagerank库计算
"""
import networkx as nx
import argparse

def buildGraph(edges, directed=False):
	"""
	初始化图
	:param edges: 存储有向边的列表
	:return: 使用有向边构造完毕的有向图
	"""
	if directed:
		G = nx.DiGraph()   # DiGraph()表示有向图
	else:
		G = nx.Graph()   # Graph()表示无向图
	for edge in edges:
		#G.add_edge(edge[0], edge[1])   # 加入边
		G.add_edge(edge[0], edge[1], weight=edge[2])   # 加入带权重的边
	return G


def test():
	edges = [("A", "B", 0.3), ("A", "C", 0.2), ("A", "D", 0.6), ("A", "E", 0.9), ("A", "F", 0.7)]
	G = buildDiGraph(edges)
	# 最Naive的pagerank计算，最朴素的方式没有设置随机跳跃的部分，所以alpha=1
	pr_value = nx.pagerank(G, alpha=1)
	for k in pr_value: print k,pr_value[k]
	## 改进后的pagerank计算，随机跳跃概率为15%，因此alpha=0.85
	#pr_impro_value = nx.pagerank(G, alpha=0.85)
	#print("improved pagerank:", pr_impro_value)

if __name__ == '__main__':
	#for f in /histor/sun/maofb/work/Oncobase/Gene_expression/WGCNA_TCGA/*/AS-green-FPKM-Step-by-step-CytoscapeInput-edges-modules.txt;do echo $f;sed 's/[|][0-9]\+//g' $f > $f.format;done
	parser = argparse.ArgumentParser()
	parser.add_argument('input', type=str, help='input file of edges')
	parser.add_argument('-d', '--direction', help='Whether the graph is directed', action="store_true")
	parser.add_argument('--head', help='Whether drop the first line', action="store_true")
	args = parser.parse_args()
	with open(args.input) as f: content = [l.strip().split('\t') for l in f]
	if args.head: del content[0]
	edges = [(l[0], l[1], float(l[2])) for l in content]
	if args.direction:
		G = buildGraph(edges, True)
	else:
		G = buildGraph(edges)
	pr_value = nx.pagerank(G, alpha=0.85)
	for l in content:
		rel = [l[0], l[1], l[2], str(pr_value.get(l[0], None)), str(pr_value.get(l[1], None))]
		print '\t'.join(rel)
	#for f in /histor/sun/maofb/work/Oncobase/Gene_expression/WGCNA_TCGA/*/*.txt.format;do python page_rank.py $f --head > $f.page_rank & done
	#for f in /histor/sun/maofb/work/Oncobase/Gene_expression/WGCNA_TCGA/*/*.page_rank;do awk -v OFS='\t' '{split(FILENAME,a,"/");print $0,a[9]}' $f;done > /histor/sun/maofb/shileisheng/wgcna_network.txt
