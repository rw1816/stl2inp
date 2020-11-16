# -*- coding: utf-8 -*-
"""
wrapper script for stl-to-input programme

Created on Mon Aug 17 12:36:04 2020

@author: Dr Richard J Williams, Imperial College London
         r.williams16@imperial.ac.uk

INPUT: A CAD (.stl) file of the part to convert to Abqus input
OUTPUT: A blank Abaqus input file containing a structured, cubic mesh of the part
        written out to the same directory as the input file

"""
import numpy as np
import stltovoxel
import indexing_routines
from shutil import copyfile
from util import rescale_mesh
from tkinter import *
from tkinter.filedialog import askopenfilename

## grab file
root=Tk()
root.withdraw() # we don't want a full GUI, so keep the root window from appearing
root.update()
root.filename = askopenfilename(title='Select STL file') # show an "Open" dialog box and return the path to the selected file
root.destroy()

stl_file = root.filename

element_size = float(input('Specify element size '))

#note the programe slices through the z axis in the CAD file, so orient z up in the CAD.
#Scale is set by the largest XY dimension. The largest XY dimension divided by the number of divisions
#gives this value. Element size must be in the same unit as the CAD file. 

#grab the stl_vertices and calculate size
num_divisions_xy, mesh = stltovoxel.getResolution(stl_file, element_size)

#call stltovoxel and calculate voxel centroids
voxel_cent_x, voxel_cent_y, voxel_cent_z, scale = stltovoxel.getVoxels(mesh, num_divisions_xy)
centroids_all = np.transpose(np.vstack((voxel_cent_x, voxel_cent_y, voxel_cent_z)))
#everything is unscaled working with arbitrary element size of 1
num_voxels = len(centroids_all)

#call write_nodes and get nodal coordinates
print('Getting nodal coordinates ...')
all_nodes = indexing_routines.write_nodes(centroids_all, num_voxels)
all_nodes = [tuple(row) for row in all_nodes]
nodes = np.unique(all_nodes, axis=0)    #remove duplicate nodes
nodes = nodes - 0.5
node_num = np.arange(1, len(nodes[:,0]) +1, 1)
num_nodes = len(nodes)

# index elements
## here call the FORTRAN routine 2
print('Indexing elements ...')

els_all, inc_x = indexing_routines.index_els(nodes[:,0], nodes[:,1], nodes[:,2], node_num, 1)
mask = els_all != 0
els_all = np.reshape(els_all[mask], (((int(len(els_all[mask])/8)), 8))) # this line is a bit scary

## form input file
print('Writing input file ...')

nodes = rescale_mesh(nodes, element_size)     #now we drop back into scale
el_num = np.arange(1, len(els_all)+1, 1)
elements= np.transpose(np.vstack((el_num, np.transpose(els_all))))
nodes = np.column_stack((node_num, nodes))

blank_inp = "blank_abq_inp.inp"
abq_file = root.filename[0:-4] + '_mesh.inp'
copyfile("blank_abq_inp.inp", abq_file)
fmt = '%i',' %1.5f',' %1.5f',' %1.5f'

with open(abq_file, 'a+') as f:
    f.write('*Node\n')
    np.savetxt(f, nodes, fmt=fmt, delimiter=',')
    f.write('*Element, type=C3D8R\n')
    np.savetxt(f, elements, '%i', delimiter=',')

print('Complete!')    