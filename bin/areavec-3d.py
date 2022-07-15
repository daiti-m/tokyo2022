#!/usr/local/bin/python

import sys
import csv
import putil
import numpy as np
import japanize_matplotlib
from mpl_toolkits.mplot3d import Axes3D
from scipy.linalg import svd
from pylab import *

M = 15

def compress (matrix, M):
    U,S,V = svd (matrix[:,0:M])
    return -np.dot (U[:,0:3], diag(sqrt(S[0:3]))), \
           -np.dot(V[0:3,:].T, diag(sqrt(S[0:3])))

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
    global M
    if len(sys.argv) < 4:
        usage ()
    else:
        M = int (sys.argv[1])
        data = sys.argv[2]
        output = sys.argv[3]

    matrix, areas = load (data + '.csv')
    candidates = persons (data + '.dat')
    areavec, candvec = compress (matrix, M)

    fig = figure(figsize=(10,7))
    ax = fig.gca (projection='3d')
    putil.simple3d (ax)

    #
    #  plot areas
    #
    N = areavec.shape[0]
    for n in range(N):
        area = areas[n]
        coord = areavec[n,:]
        ax.text (coord[0], coord[1], coord[2], area, size=10)

    #
    #  plot candidates
    #
    for n in range(M):
        cand = candidates[n]
        coord = candvec[n,:]
        ax.text (coord[0], coord[1], coord[2], cand, size=10, color='blue')

    # whole
#     ax.set_xlim (-0.7,0.7)
#     ax.set_ylim (-0.7,0.7)
#     ax.set_zlim (-0.5,0.7)
    # land
    ax.set_xlim (-0.3,0.3)
    ax.set_ylim (-0.3,0.3)
    ax.set_zlim (-0.3,0.3)
    
    savefig (output, dpi=200)
    show ()



if __name__ == "__main__":
    main ()
