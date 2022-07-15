#!/usr/local/bin/python

import sys
import csv
import numpy as np
import japanize_matplotlib
from sklearn.manifold import TSNE
from pylab import *

def load (file):
    matrix = []
    areas = []
    with open (file, 'r') as fh:
        reader = csv.reader (fh)
        for fields in reader:
            area = fields[0]
            vector = np.array (list(map(float, fields[1:])))
            matrix.append (vector)
            areas.append (area)

    return np.array(matrix), areas

def usage ():
    print ('usage: % areavec.py K tokyo.csv output')
    sys.exit (0)

def main ():
    if len(sys.argv) < 4:
        usage ()
    else:
        K = int (sys.argv[1])
        data = sys.argv[2]
        output = sys.argv[3]
        

    matrix, areas = load (data)
    X = TSNE(n_components=2,random_state=0).fit_transform (matrix[:,0:10])
    N = X.shape[0]
    for n in range(N):
        text (X[n,0], X[n,1], areas[n], size=10)
    axis ([-7.5,4,-6,0.5])
    savefig (output, dpi=200)
    show ()
    



if __name__ == "__main__":
    main ()
