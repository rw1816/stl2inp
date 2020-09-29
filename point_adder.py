# -*- coding: utf-8 -*-
"""
Created on Thu Sep 17 15:44:11 2020

@author: richw
function to append a row of manual points to the mesh nodes
fill_dirn - direction for row tomove in (0,1,2), numpy-like 
"""
import numpy as np

def add_row(first_point, end_point, fill_dirn, scale_factor, x, y, z):
    
    first_point = np.array(first_point)*scale_factor
    end_point = np.array(end_point)*scale_factor
    rng = first_point - end_point
    new_point = first_point
    
    if sum(rng) > 0: #i.e. we are moving in the negative direction
            
        while new_point[fill_dirn] > end_point[fill_dirn]:
            
            x=np.append(x, new_point[0]+1)
            y=np.append(y, new_point[1]+1)
            z=np.append(z, new_point[2]+1)
            new_point[fill_dirn] = new_point[fill_dirn]-1
            
    else:   #we are moving in the positive direction
        
        while new_point[fill_dirn] < end_point[fill_dirn]:
            
            x=np.append(x, new_point[0]+1)
            y=np.append(y, new_point[1]+1)
            z=np.append(z, new_point[2]+1)
            new_point[fill_dirn] = new_point[fill_dirn]+1
            
    return x,y,z

