# -*- coding: utf-8 -*-
import numpy as np


def manhattanDistance(p1, p2, d=2):
    assert (len(p1) == len(p2))
    allDistances = 0
    for i in range(d):
        allDistances += abs(p1[i] - p2[i])
    return allDistances


def printBigArray(big, yes='1', no='0'):
    print()
    for line in big:
        for char in line:
            if char:
                print(yes, end=" ")
            else:
                print(no, end=" ")
        print()


def removeDupsFromPointList(ptList):
    newList = ptList[:]
    return tuple(set(newList))

def arrayToWhiteGreyscalePixel(array, pixels):
    for i in range(array.shape[0]):
        for j in range(array.shape[1]):
            if array[i, j]:
                pixels[i, j] = 255

def padVoxelArray(voxels):
    shape = voxels.shape
    new_shape = (shape[0]+2,shape[1]+2,shape[2]+2)
    vol = np.zeros(new_shape, dtype=bool)
    for a in range(shape[0]):
        for b in range(shape[1]):
            for c in range(shape[2]):
                vol[a+1,b+1,c+1] = voxels[a,b,c]
    return vol, (new_shape[1],new_shape[2],new_shape[0])

def rescale_mesh(nodes, element_size):
    
    nodes=nodes*element_size
    apparent_elsize = sum(nodes[1,1:4]-nodes[0,1:4])
    
    if apparent_elsize != element_size:
    
        nodes=np.divide(nodes, apparent_elsize)
        nodes=np.multiply(nodes, element_size)
        print('*warning* nodes re-scaled')
        
    return nodes