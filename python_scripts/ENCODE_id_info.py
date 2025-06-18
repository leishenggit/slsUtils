#!/histor/sun/maofb/anaconda3/bin/python
from bs4 import BeautifulSoup
import requests
import argparse
import time
import random



## 设置命令行参数
def setArgs():
	parser = argparse.ArgumentParser(description="function: extract ENCODE accession info")
	taxid_group = parser.add_mutually_exclusive_group(required=True)
	taxid_group.add_argument('--accession', help='accession to process', type=str, nargs="+")
	taxid_group.add_argument('--url', help='URL to extract info', type=str, nargs='+')
	return parser.parse_args()

def getInfo(url):
	res = requests.get(url)
	soup = BeautifulSoup(res.text, 'lxml')
	dls = soup.select('dl[class="key-value"]')
	#print(dls)
	head, rel = ['Accession'], [url.split('/')[-1]]
	for ele in dls[1].contents:
		head.append(ele.contents[0].get_text())
		rel.append(ele.contents[1].get_text())
	return((head, rel))


if __name__ == "__main__":
	args = setArgs()
	#url = 'https://www.encodeproject.org/files/ENCFF010MDK'
	if args.url:
		urls = args.url
		head, rel = getInfo(urls[0])
		print('\t'.join(head))
		print('\t'.join(rel))
		for url in urls[1:]:
			head, rel = getInfo(url)
			print('\t'.join(rel))
			time.sleep(random.randint(1,6))
	else:
		urls = ['https://www.encodeproject.org/files/'+i for i in args.accession]
		head, rel = getInfo(urls[0])
		print('\t'.join(head))
		print('\t'.join(rel))
		for url in urls[1:]:
			head, rel = getInfo(url)
			print('\t'.join(rel))
			time.sleep(random.randint(1,6))


