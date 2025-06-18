#!/home/shileisheng/anaconda3/bin/python
import json


if __name__ == '__main__':
    f_in = 'ko00001.json'
    with open(f_in) as f : nodes = json.load(f)
    for B in nodes.get('children'): 
        B['name'] = B['name']
        for C in B.get('children'): 
            C['name'] = B['name']+'\t'+C['name']
            for D in C.get('children', []): 
                D['name'] = C['name']+'\t'+D['name']
                for E in D.get('children', []): 
                    E['name'] = D['name']+'\t'+E['name']
                    print(E['name'])

#https://www.genome.jp/kegg-bin/get_htext?ko00001 
