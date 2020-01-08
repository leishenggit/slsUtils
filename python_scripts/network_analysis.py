#!/home/shileisheng/anaconda3/bin/python
import networkx as nx
import numpy as np
import argparse


def output(source, target, verbose):
	try:
		p = nx.shortest_path(G, source, target)
		distance = nx.shortest_path_length(G, source, target)
		if verbose: print('%s--->%s, shortest_path: %s, shortest_path_length: %d' % (source, target, p, distance))
		print("%s\t%s\t%.4f" %(source, target, distance))
	except:
		print('No path between %s and %s.' % (source, target))


def output_1(source, target, verbose):
	try:
		p = nx.shortest_path(G, source, target)
		del p[source]
		avg_len = 0
		for target in p:
			#distance = nx.shortest_path_length(G, source, target)
			distance = len(p[target]) - 1
			avg_len += distance
			if verbose: print('%s--->%s, shortest_path: %s, shortest_path_length: %d' % (source, target, p[target], distance))
		if len(p) > 0:
			print("%s\t%.4f" %(source, avg_len/len(p)))
	except:
		print('No link to %s.' % (source))


def output_2(source, target, verbose):
	try:
		p = nx.shortest_path(G, source, target)
		del p[target]
		avg_len = 0
		for source in p:
			#distance = nx.shortest_path_length(G, source, target)
			distance = len(p[source]) - 1
			avg_len += distance
			if verbose: print('%s--->%s, shortest_path: %s, shortest_path_length: %d' % (source, target, p[source], distance))
		if len(p) > 0:
			print("%s\t%.4f" %(target, avg_len/len(p)))
	except:
		print('No link to %s.' % (target))


def output_3(source, target, verbose):
	try:
		p = nx.shortest_path(G, source, target)
		for source in p:
			del p[source][source]
			avg_len = 0
			for target in p[source]:
				distance = len(p[source][target]) - 1
				avg_len += distance
				if verbose: print('%s--->%s, shortest_path: %s, shortest_path_length: %d' % (source, target, p[source][target], distance))
			if len(p[source]) > 0:
				print("%s\t%.4f" %(source, avg_len/len(p[source])))
	except:
		print('No link in the Graph.')

if __name__=="__main__":
	parser = argparse.ArgumentParser(description = 'A program for extracted shortest_path and shortest_path_length')
	parser.add_argument('input', help='Please input a file contain 2 cols of gene', type=str)
	parser.add_argument('-s', '--source', help='Please input source gene', type=str, default=None)
	parser.add_argument('-t', '--target', help='Please input target gene', type=str, default=None)
	parser.add_argument('-d', '--direction', help='Whether the graph is directed', action="store_true")
	parser.add_argument('-v', '--verbose', help='Print every shortest path detail', action="store_true")
	args = parser.parse_args()
	#自定义网络
	with open(args.input) as f: content = [l.strip().split('\t') for l in f]
	ss = [l[0] for l in content]
	tt = [l[1] for l in content]
	row=np.array(ss)
	col=np.array(tt)
	ss.extend(tt)
	if args.direction:
		print('生成一个空的有向图')
		G=nx.DiGraph()
	else:
		print('生成一个空的无向图')
		G=nx.Graph()
	print('为这个网络添加节点...')
	for i in set(ss): G.add_node(i) 
	# G.add_nodes_from(set(ss)) 
	print('在网络中添加无权的边...')
	for i in range(np.size(row)): G.add_edge(row[i],col[i])
	# G.add_edges_from([(row[i],col[i]) for i in range(len(np.size(row)))])
	print('给网路设置布局...')
	pos = nx.shell_layout(G)
	print('画出网络图像：===============')
	print('Not supported on linux :)')
	source, target, verbose = args.source, args.target, args.verbose
	if source and target:
		output(source, target, verbose)
	elif source and not target:
		output_1(source, target, verbose)
	elif not source and target:
		output_2(source, target, verbose)
	else:
		output_3(source, target, verbose)

