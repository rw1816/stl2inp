# -*- coding: utf-8 -*-
"""
wrapper script for stl-to-voxel package

Created on Mon Aug 17 12:36:04 2020

@author: Dr Richard J Williams, Imperial College London
"""
import numpy as np
import os
import sys
import stltovoxel
import fort_subs
from shutil import copyfile
import point_adder

out_file_path = 'D:/ABAQUS/meshes/final_test/test_nodes_txt.xyz'
stl_file = "D:\ABAQUS\meshes/accel_repaired.stl"
abq_file = "D:/ABAQUS/meshes/accel_05.inp"

num_divisions = 152

#note the programe slices through the z axis in the CAD file, so perhaps re-orient z up?
#scale is set by the largest XY dimension. The largest XY dimension divided by the number of divisions
# gives this value

voxels, bounding_box, scale = stltovoxel.doExport(stl_file, 'D:/ABAQUS/meshes/wrapper_test.xyz', num_divisions)
x, y, z = stltovoxel.exportXyz(voxels, bounding_box, out_file_path)

## pad the extra layer at the bottom
mask = x == 1
[bottom_x, bottom_y, bottom_z] = x[mask], y[mask], z[mask]
bottom_x[:]=0
x=np.hstack((x,bottom_x))
y=np.hstack((y,bottom_y))
z=np.hstack((z,bottom_z))

root_coords = np.array((min(x), min(y), min(z)));
step = 1
inc_x = np.array([step, 0, 0]);
inc_y = np.array([0, step, 0]);
inc_z = np.array([0, 0, step]);
length = len(x)

scale_factor = scale[0]

## add additional rows
add_point_1 = np.array([57.5, 30.0, 20.5])*scale_factor
add_point_2 = np.array([56.5, 21.5, 20.5])*scale_factor
add_point_3 = np.array([59.5, 25.0, 20.5])*scale_factor
add_point_4 = np.array([61.0, 28.0, 20.5])*scale_factor
add_point_5 = np.array([59.0, 24.5, 20.5])*scale_factor
z_back = 16*scale_factor

for i in range(int(z_back), int(add_point_1[2]+2)):
    x=np.append(x, add_point_1[0])
    x=np.append(x, add_point_2[0])
    x=np.append(x, add_point_3[0])
    x=np.append(x, add_point_4[0])
    x=np.append(x, add_point_5[0])
    y=np.append(y, add_point_1[1]+1)
    y=np.append(y, add_point_2[1]+1)
    y=np.append(y, add_point_3[1]+1)
    y=np.append(y, add_point_4[1]+1)
    y=np.append(y, add_point_5[1]+1)
    z=np.append(z, i+1)
    z=np.append(z, i+1)
    z=np.append(z, i+1)
    z=np.append(z, i+1)
    z=np.append(z, i+1)

x, y, z = point_adder.add_row([70, 8.5, 3.5], [64.5, 8.5, 3.5], 0, scale_factor, x, y, z)
x, y, z = point_adder.add_row([70, 7.5, 4.5], [66.5, 7.5, 4.5], 0, scale_factor, x, y, z)
x, y, z = point_adder.add_row([70, 9, 7], [65.5, 9, 7], 0, scale_factor, x, y, z)
x, y, z = point_adder.add_row([70.0, 44.5, 8.0],[65, 44.5, 8.0], 0, scale_factor, x, y, z)
x, y, z = point_adder.add_row([70.,44,3.5],[65, 44,3.5], 0, scale_factor, x, y, z)
x, y, z = point_adder.add_row([70.,44.5,3.5],[65, 44.5,3.5], 0, scale_factor, x, y, z)
x, y, z = point_adder.add_row([70.,44.,4.5],[65,44.,4.5], 0, scale_factor, x, y, z)
x, y, z = point_adder.add_row([70.,44.,5],[66.,44.,5], 0, scale_factor, x, y, z)

# generate vector of node numbers    
node_num = np.arange(1, len(x)+1, 1)

## here call the FORTRAN routine
els_all = fort_subs.index_els(x, y, z, node_num, 1)


x=(x)/scale_factor
y=(y-1)/scale_factor
z=(z-1)/scale_factor

#remove unreferences elements
mask = els_all != 0
els_all = np.reshape(els_all[mask], (((int(len(els_all[mask])/8)), 8))) # this line is a bit scary

## form input file
el_num = np.arange(1, len(els_all)+1, 1)
elements= np.transpose(np.vstack((el_num, np.transpose(els_all))))
nodes = np.transpose(np.vstack((node_num, x, y, z)))

blank_inp = "blank_abq_inp.inp"
copyfile("blank_abq_inp.inp", abq_file)
fmt = '%i',' %1.5f',' %1.5f',' %1.5f'

with open(abq_file, 'a+') as f:
    f.write('*Node\n')
    np.savetxt(f, nodes, fmt=fmt, delimiter=',')
    f.write('*Element, type=C3D8R\n')
    np.savetxt(f, elements, '%i', delimiter=',')
    

#write_abq_inp(nodes, elements)
#writematrix(els, 'D:/ABAQUS/elements.txt')
#
#nodes=horzcat(node_num', DV);
#writematrix(nodes, 'D:/ABAQUS/meshes/nodes.txt')


"""## check for 2 node connectivity and add nodes to correct it
el_centroid = np.vstack((x, y, z))
el_centroid= np.transpose(el_centroid)
el_centroid=el_centroid[el_centroid[:,0].argsort()] #sort according to x coordinate

for element in el_centroid: #loop through the elements

    if  np.size(np.hstack((np.where((el_centroid == (np.add(element,[0,0.5,0]))).all(axis=1)),
        np.where((el_centroid == (np.add(element, [0,-0.5,0]))).all(axis=1)),
        np.where((el_centroid == (np.add(element, [0,0,0.5]))).all(axis=1)),
        np.where((el_centroid == (np.add(element, [0,0,-0.5]))).all(axis=1))))) == 2:
    #check for pixel adjacency in xy (yz here), i.e. all pixels should have 2 adjacent
            print('yes')
            print(element)"""