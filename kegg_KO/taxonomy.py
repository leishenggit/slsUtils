#!/home/shileisheng/anaconda3/bin/python
import sys


if __name__ == '__main__':
    f_in = sys.argv[1]
    with open(f_in) as f : content = [l.strip().split('\t') for l in f]
    head = content[0]
    #KO = []
    level = ['level_'+str(i) for i in range(1,len(head)+1)]
    for l in content:
        path = [i[:i.index(' ')] for i in l]
        for i in range(len(l)):
            idx = l[i].index(' ')
            k = l[i][:idx]
            #if k in KO: continue
            rel = [k, level[i], l[i][idx:].strip(), ':'.join(path[:i+1])]
            print('\t'.join(rel))
            #KO.append(k)
            