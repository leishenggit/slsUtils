#!/software/biosoft/software/python/python3/bin/python
from bs4 import BeautifulSoup
import sys

def get_info(html_f):
	fname = html_f.split('/')[-1]
	soup = BeautifulSoup(open(html_f), 'html.parser')
	summary = soup.find("div", id="summary")
	tbs = summary.find_all("table", class_="summary_table")
	head, rel = ['fname'], [fname]
	for table in tbs:
		for tr in table.find_all("tr"):
			head.append(tr.contents[0].get_text())
			rel.append(tr.contents[1].get_text())
	return((head,rel))

if __name__ == "__main__":
	head,rel = get_info(sys.argv[1])
	print('\t'.join(head))
	print('\t'.join(rel))
	for html_f in sys.argv[2:]:
		head,rel = get_info(html_f)
		print('\t'.join(rel))


