#!/public/home/jcli/public/software/Python3.5/bin/python
#PBS -N position 
#PBS -o /public/home/shileisheng/other/position
#PBS -e /public/home/shileisheng/other/position
#PBS -l nodes=node8
import time
from multiprocessing import Pool, Manager


def getFasta(chr,sequence):
	filepath = "/public/home/jcli/public/database/hg19/"+chr+".fa"
	with open(filepath) as f:
		fasta = f.readlines()
		del fasta[0]
		strs = [l.strip("\n") for l in fasta]
		sequence[chr]="".join(strs)
	print("success gain fasta data of "+chr)

	
def getUpperPos(chr,seq):
	start,end,flag = 0,0,0
	with open("N_"+chr+".txt","w") as f:
		for idx,char in enumerate(seq):
			if char == "N" and flag == 0:
				start = idx+1
				flag = 1
			elif char == "N" and flag == 1:
				end = idx + 1
				if end == len(seq):f.write(chr+"\t"+str(start)+"\t"+str(end)+"\n")
			elif flag == 1:
				if end < start:end = start
				f.write(chr+"\t"+str(start)+"\t"+str(end)+"\n")
				flag = 0
		
	print("finish extract position of "+chr)
	
if __name__=="__main__":
	chromo = ["chr"+str(i) for i in range(1,23)]
	sequence = Manager().dict()
	#sequence = {key:"" for key in chromo}
	p = Pool()
	for i in range(22):
		p.apply_async(getFasta,args = (chromo[i],sequence))
	p.close()
	p.join()
	
	print("finish read fasta file !")
	
	p = Pool()
	for i in range(22):
		p.apply_async(getUpperPos,(chromo[i],sequence[chromo[i]]))
	p.close()
	p.join()
	print("finish !")
