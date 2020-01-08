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

if __name__ == '__main__':
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
