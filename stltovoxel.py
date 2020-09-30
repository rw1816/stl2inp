import argparse
import os.path
import io
import xml.etree.cElementTree as ET

from PIL import Image
import numpy as np

import slice
import stl_reader
import perimeter
from util import arrayToWhiteGreyscalePixel, padVoxelArray


def doExport(inputFilePath, outputFilePath, resolution):
    mesh = list(stl_reader.read_stl_verticies(inputFilePath))
    (scale, shift, bounding_box) = slice.calculateScaleAndShift(mesh, resolution)
    mesh = list(slice.scaleAndShiftMesh(mesh, scale, shift))
    #Note: vol should be addressed with vol[z][x][y]
    vol = np.zeros((bounding_box[2],bounding_box[0],bounding_box[1]), dtype=bool)
    
    for height in range(bounding_box[2]):
        print('Processing layer %d/%d'%(height,bounding_box[2]))
        lines = slice.toIntersectingLines(mesh, height)
        prepixel = np.zeros((bounding_box[0], bounding_box[1]), dtype=bool)
        perimeter.linesToVoxels(lines, prepixel)
        vol[height] = prepixel
    vol, bounding_box = padVoxelArray(vol)
    outputFilePattern, outputFileExtension = os.path.splitext(outputFilePath)
    return vol, bounding_box, scale
#    if outputFileExtension == '.png':
#        exportPngs(vol, bounding_box, outputFilePath)
#    elif outputFileExtension == '.xyz':
#        exportXyz(vol, bounding_box, outputFilePath)
#   elif outputFileExtension == '.svx':
#        exportSvx(vol, bounding_box, outputFilePath, scale, shift)
    

def exportPngs(voxels, bounding_box, outputFilePath):
    size = str(len(str(bounding_box[2]))+1)
    outputFilePattern, outputFileExtension = os.path.splitext(outputFilePath)
    for height in range(bounding_box[2]):
        img = Image.new('L', (bounding_box[0], bounding_box[1]), 'black')  # create a new black image
        pixels = img.load()
        arrayToWhiteGreyscalePixel(voxels[height], pixels)
        path = (outputFilePattern + "%0" + size + "d.png")%height
        img.save(path)

def exportXyz(voxels, bounding_box, outputFilePath):
    output = open(outputFilePath, 'w')
    X=[]
    Y=[]
    Z=[]
    for z in range(bounding_box[2]):
        
        for x in range(bounding_box[0]):
            for y in range(bounding_box[1]):
                if voxels[z][x][y]:
                    output.write('%s, %s, %s\n'%(x,y,z))
                    X=np.append(X, x)
                    Y=np.append(Y,y)
                    Z=np.append(Z,z)
                    
    return X, Y, Z                
    output.close()

def file_choices(choices,fname):
    filename, ext = os.path.splitext(fname)
    if ext == '' or ext not in choices:
        if len(choices) == 1:
            parser.error('%s doesn\'t end with %s'%(fname,choices))
        else:
            parser.error('%s doesn\'t end with one of %s'%(fname,choices))
    return fname

# if __name__ == '__main__':
#     parser = argparse.ArgumentParser(description='Convert STL files to voxels')
#     parser.add_argument('input', nargs='?', type=lambda s:file_choices(('.stl'),s))
#     parser.add_argument('output', nargs='?', type=lambda s:file_choices(('.png', '.xyz', '.svx'),s))
#     args = parser.parse_args()
#     doExport(args.input, args.output, 10)
