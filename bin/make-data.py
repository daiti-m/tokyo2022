#!/usr/local/bin/python
# -*- coding: utf-8 -*-
#
#    make-data.py
#    make data statistics from crawled texts.
#    $Id: make-data.py,v 1.4 2022/07/14 01:10:28 daichi Exp $
#

import re
import sys
import numpy as np
from numpy import log
from opts import getopts

data = {}

def read_cands (file):
    data = {}
    pcts = {}
    with open (file, 'r') as fh:
        fields = 0
        person = ''
        votes = -1
        for buf in fh:
            line = buf.rstrip('\n')
            if len(line) > 0:
                fields += 1
                if (fields == 3):
                    person = line
                else:
                    match = re.search(r'^([0-9,]+)[（(]', line)
                    if match:
                        votes = float (match.group(1).replace (',',''))
            else:
                data[person] = votes
                fields = 0
                person = ''
                votes = -1
    if not person == '':
        data[person] = votes

    total = sum(data.values()) + 0.0
    for person,votes in sorted (data.items(), key=lambda x: x[1], reverse=True):
        p = votes / total
        pcts[person] = p
        # print ('%s => %.3f (%d)' % (person, p*100, votes))

    return pcts

def process (file):
    global data
    lines = 0
    area = ''
    votes = 0
    person = ''
    with open(file, 'r') as fh:
        for buf in fh:
            line = buf.rstrip('\n')
            if not len(line) > 0:
                continue
            lines += 1
            if (lines == 1):
                area = line
                data[area] = {}
                # print ('* area = %s' % area)
            elif (lines == 2):
                pass # do nothing
            elif (lines > 3):
                # content for each candidate
                if re.match(r'[0-9,]', line):
                    votes = int(line.replace(',',''))
                elif re.search (r'[（(][0-9.]+', line):
                    match = re.search (r'[（(]([0-9.]+)', line)
                    if match:
                        pct = float(match.group(1))
                        data[area][person] = pct
                        person = ''; votes = -1
                    else:
                        print ('ERROR! line = %s' % line)
                else:
                    person = line

    return data

def save (data, cands, file):
    candidates = list (map (lambda x: x[0], \
                            sorted (cands.items(), key=lambda x: x[1], reverse=True)))
    with open (file + '.csv', 'w') as of:
        for area in sorted (data.keys()):
            of.write ('%s' % area)
            for person in candidates:
                p = cands[person]
                q = data[area][person] / 100
                if q > 0:
                    ratio = log (p) - log(q)
                else:
                    ratio = 0
                of.write(',%.4f' % ratio)
            of.write ('\n')
    with open (file + '.dat', 'w') as of:
        for person in candidates:
            of.write ('%s\n' % person)

def usage ():
    print ('usage: % make-data.py -O output(.{csv,dat}) -C candidates.txt *.txt')
    sys.exit(0)

def main ():
    global data
    opts,args = getopts(["O|output=", "C|candidates=", "h|help"])
    if not len(args) > 0:
        usage ()
    else:
        output = opts['O']
        candidates = opts['C']

    cands = read_cands (candidates)
    
    for file in args:
        process (file)
        
    save (data, cands, output)


if __name__ == "__main__":
    main ()
