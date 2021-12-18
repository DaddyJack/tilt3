# -*- coding: utf-8 -*-
import os
import sys
import numpy as np

def getFileNames(ext=".dat"):
    if len(sys.argv) > 1:
        path = sys.argv[1]
    else:
        path = "."
    files = os.listdir(path)
    dataFiles = []
    for f in files:
        if f.find(ext, -len(ext)) >= 0:
            dataFiles.append(f)
    return dataFiles

def main():
    slopeLevels = 9
    typeLevels = 4
    sumSlope = np.zeros((typeLevels, slopeLevels))
    nSlope = np.zeros((typeLevels, slopeLevels))
    slope = (-35, -25, -15, -5, 5, 15, 25, 35, 720)
    i = list(range(9))
    sl = dict(list(zip(slope, i)))
    invsl = dict(list(zip(i, slope)))
   
    df = getFileNames()
    subject = 0
    for f in df:
        lines = open(f, 'r').readlines()
        subject += 1
        for line in lines:
            if line[0] == ';':
                continue
            args = line.split()
            type = int(args[0])
            if type == 2:
                slope = int(args[1])
            else:
                slope = int(args[2])
            fpse = float(args[7])
            sumSlope[type, sl[slope]] += fpse
            nSlope[type, sl[slope]] += 1.0
        for i in range(typeLevels):
            for j in range(slopeLevels):
                if nSlope[i,j] != 0.0:
                    mean = sumSlope[i,j] / nSlope[i, j]
                    print(subject, i, invsl[j], mean, nSlope[i, j])        
            
if __name__ == "__main__":
    main()

        
