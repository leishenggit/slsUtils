#!/public/home/jcli/public/software/Python3.5/bin/python
import time
from multiprocessing import Pool,Manager



def window_cont(key):
	with open("/public/home/jcli/public/database/hg19/chr%s.fa"%key) as fa:
		all_squence=fa.readlines()
		del all_squence[0]
		all_squence=[line.strip("\n").upper() for line in all_squence]
		fastq="".join(all_squence)
	my_dict["chr"+str(key)] = len(fastq)
	#print("length of chr %d is : %d"%(key,len(fastq)))
	
if __name__=="__main__":
	print(time.ctime())
	my_dict = Manager().dict()
	chromo = [i for i in range(1,23)]
	chromo.extend(['X','Y'])
	pool=Pool()
	for i in chromo:
		pool.apply_async(window_cont,(i,))
	pool.close()
	pool.join()
	with open("hg19_length.txt","w") as ref:
		for key in dict(my_dict):ref.write("%s\t%d\n"%(key,my_dict[key]))
	print(time.ctime())
