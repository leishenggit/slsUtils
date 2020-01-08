#!/public/home/jcli/public/software/Python3.5/bin/python
from multiprocessing import Pool, Manager


def getFasta(chr,sequence):
	filepath = "/public/home/jcli/public/database/hg19/"+chr+".fa"
	with open(filepath) as f:
		fasta = f.readlines()
		del fasta[0]
		strs = [l.strip("\n") for l in fasta]
		sequence[chr]="".join(strs)
	print("success gain fasta data of "+chr)

	
def getLowerPos(chr,seq):
	start,flag = 0,0
	with open("repeat_"+chr+".txt","w") as f:
		for idx,char in enumerate(seq):
			if char in ["a","t","c","g"]:
				if flag == 0:
					start = idx+1
					flag = 1
			elif flag != 0:
				f.write(chr+"\t"+str(start)+"\t"+str(idx)+"\n")
				flag = 0
		if flag != 0 :f.write(chr+"\t"+str(start)+"\t"+str(idx+1)+"\n")
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
		p.apply_async(getLowerPos,(chromo[i],sequence[chromo[i]]))
	p.close()
	p.join()
	print("finish !")
