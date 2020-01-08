#!/home/shileisheng/anaconda3/bin/python
import sys


def lca(ts):
    if len(ts) != 1:    
        f = ts[0].split(':')
        l = ts[-1].split(':')
        for i in range(len(f)):
            if f[i] != l[i]:
                return f[i-1]
            else:
                continue
        return f[-1]
    else:
        return ts[0].split(':')[-1]

if __name__ == '__main__':
    # read tax info
    tax_file = open('/home/shileisheng/reference/taxonomy.tbl', 'r')
    content = [l.strip().split('\t') for l in tax_file]
    tax_d = {l[0]:l for l in content}
    tax_file.close()
    ts = [tax_d[taxid][3] for taxid in sys.argv[1:]]
    re = lca(sorted(ts))
    print('\t'.join(tax_d[re]))

