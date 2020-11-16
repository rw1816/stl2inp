import numpy as np

import slice
import perimeter
from util import padVoxelArray

def getVoxels(mesh, resolution):
    
    (scale, shift, bounding_box) = slice.calculateScaleAndShift(mesh, resolution)
    mesh = list(slice.scaleAndShiftMesh(mesh, scale, shift))
    #Note: vol should be addressed with vol[z][x][y]
    voxels = np.zeros((bounding_box[2],bounding_box[0],bounding_box[1]), dtype=bool)
    
    print('Getting voxels...')
    print('Part has {0} layers in z axis '.format(bounding_box[2]))

    for height in range(bounding_box[2]):
        
        
        lines = slice.toIntersectingLines(mesh, height)
        prepixel = np.zeros((bounding_box[0], bounding_box[1]), dtype=bool)
        perimeter.linesToVoxels(lines, prepixel)
        voxels[height] = prepixel
        
    voxels, bounding_box = padVoxelArray(voxels)
    
    X=[]
    Y=[]
    Z=[]
    
    for z in range(bounding_box[2]):
        
        for x in range(bounding_box[0]):
            for y in range(bounding_box[1]):
                if voxels[z][x][y]:
                    
                    X=np.append(X, x)
                    Y=np.append(Y,y)
                    Z=np.append(Z,z)
    
    return X, Y, Z, scale[0]

def getResolution(stl_file, element_size):
    
    import stl_reader
    
    mesh = list(stl_reader.read_stl_verticies(stl_file))
    mesh_array = np.array(mesh).reshape(len(mesh)*3, 3)
    bound_x = abs(max(mesh_array[:,0]) - min(mesh_array[:,0]))
    bound_y = abs(max(mesh_array[:,1]) - min(mesh_array[:,1]))
    bound_z = abs(max(mesh_array[:,2]) - min(mesh_array[:,2]))
    num_divisions = int((int(max(bound_x, bound_y)) / element_size))
    
    del(mesh_array)
    
    if max(bound_x, bound_y, bound_z) != bound_z:
        print('** WARNING ** z is not the largest dimension, results may vary')
        
    return num_divisions, mesh