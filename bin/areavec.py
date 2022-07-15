#!/usr/local/bin/python

import sys
import csv
import numpy as np
import japanize_matplotlib
from scipy.linalg import svd
from pylab import *

M = 10

def compress (matrix, K):
    U,S,V = svd (matrix[:,0:M])
    return -np.dot (U[:,0:K], diag(sqrt(S[0:K]))), \
           -np.dot(V[0:K,:].T, diag(sqrt(S[0:K])))

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

def persons (file):
    candidates = []
    with open (file, 'r') as fh:
        for buf in fh:
            line = buf.rstrip('\n')
            candidates.append (line)
    return candidates

def usage ():
    print ('usage: % areavec.py K tokyo(.{csv,dat}) output')
    sys.exit (0)

def main ():
    if len(sys.argv) < 4:
        usage ()
    else:
        K = int (sys.argv[1])
        data = sys.argv[2]
        output = sys.argv[3]

    matrix, areas = load (data + '.csv')
    candidates = persons (data + '.dat')
    areavec, candvec = compress (matrix, K)

    #
    #  plot areas
    #
    N = areavec.shape[0]
    for n in range(N):
        area = areas[n]
        coord = areavec[n,:]
        text (-coord[0], coord[1], area, size=10)

    #
    #  plot candidates
    #
    for n in range(M):
        cand = candidates[n]
        coord = candvec[n,:]
        text (-coord[0], coord[1], cand, size=10, color='red')

    axis ([-0.7,1.6,-1,1.2])     # whole
    # axis ([-0.3,1,-0.2,0.35])  # land
    savefig (output, dpi=200)
    show ()





if __name__ == "__main__":
    main ()
