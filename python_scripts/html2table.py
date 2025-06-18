#!/home/shileisheng/anaconda3/bin/python
from bs4 import BeautifulSoup
import requests
import pandas as pd
import argparse
import sys

if __name__ == "__main__":
	parser = argparse.ArgumentParser(description = 'A program for extract table info from HTML file or URL')
	taxid_group = parser.add_mutually_exclusive_group(required=True)
	taxid_group.add_argument('--html', help='HTML file to scan table', type=str)
	taxid_group.add_argument('--url', help='URL to scan table', type=str)
	parser.add_argument('--out', help='output result file', type=str)
	args = parser.parse_args()
	#url = 'https://segmentfault.com/a/1190000007688656'
	if args.url:
		url = args.url
		res = requests.get(url)
		soup = BeautifulSoup(res.text, 'lxml')
	else:
		soup = BeautifulSoup(open(args.html), 'lxml')
	tables = soup.select('table')
	for i in range(len(tables)):
		df = pd.concat(pd.read_html(tables[i].prettify()))
		if args.out:
			out_f = args.out
			df.to_csv(out_f+"."+str(i),  index=False, sep='\t')
		else:
			df.to_csv(sys.stdout, index=False, sep='\t')
