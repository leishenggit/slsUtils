import argparse
from bs4 import BeautifulSoup


def out_indent(e):
	s = e.attrs['href']
	id = s[s.find('=')+1:]
	name = e.get_text().rstrip().replace('\n','')
	n_tab = e.get_text().rstrip().count('\t') - e.get_text().strip().count('\t')
	return(name, id, n_tab)

def get_indent(e):
	s = e.attrs['href']
	id = s[s.find('=')+1:]
	n_tab = e.get_text().rstrip().count('\t') - e.get_text().strip().count('\t')
	return(id, n_tab)

def get_id_name(e):
	s = e.attrs['href']
	id = s[s.find('=')+1:]
	name = e.get_text().strip().replace('\n','').replace('\t','')
	return(id,name)


## 设置命令行参数
def setArgs():
	parser = argparse.ArgumentParser(description="Parsing metaCyc pathway information")
	parser.add_argument('--html', help='命令行指定html文件', type=str)
	return parser.parse_args()

if __name__ == "__main__":
	## 获得参数
	args = setArgs()
	bsObj = BeautifulSoup(open(args.html), 'lxml')
	eles = bsObj.select('a[class="ygtvlabel"]')
	id_name = set(map(get_id_name, eles))
	print("Total item :", len(id_name))
	with open('metaCyc_id_name.txt','w') as f: 
		for item in id_name: f.write('\t'.join(item)+'\n')
	#output level relationship
	id_tab = list(map(get_indent, eles))
	N, rel = 0, []
	with open('metaCyc.txt','w') as f: 
		for e in id_tab:
			if e[1] > N:
				rel.append(e[0])
				N = e[1]
			elif e[1] == N:
				f.write('\t'.join(rel)+'\n')
				rel[-1] = e[0]
			else:
				f.write('\t'.join(rel)+'\n')
				idx = int((N - e[1]) / 2) + 1
				del rel[-idx:]
				rel.append(e[0])
				N = e[1]
### open https://metacyc.org/META/class-tree?object=Pathways to download info and go to https://www.sojson.com/jshtml.html to format html code
###  pathway details URL: https://metacyc.org/META/new-image?object=id_of_pathway
