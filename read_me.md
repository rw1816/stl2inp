Welcome to stl2inp, 

BACKGROUND
 
The code will take any .stl model and write out an Abaqus inp file containing a structured, fully cubic mesh of the stl object. This was developed to perform additive manufacturing process simulations, where objects of complex topology are frequently encountered and the native mesh generation tools are not well suited. The code may, however, be of use in other sitations. 

EXECUTION

A wrapper script (stl2inp.py) is called from the command line, usage as follows: 

	python stl2inp.py

This will bring up a windows explorer interface to navigate to the .stl file to convert. The Abaqus input file containing the mesh will then be written out to the same directory. A command line prompt will request the desired element size for the mesh; this must be supplied in the same units as the CAD file. The programme slices through the .stl file z axis and best results are achieved having the part oriented so that the largest dimension is in z. The program will print a warning if this is not so.  	

The script calls on a (freeform) FORTRAN subroutine, "indexing_routines.f90" to index finite elements from nodal coordinates. This must be compiled for python beforehand using the f2py module which is built into the numpy library. The GNU FORTRAN compiler (gcc.gnu.org/fotran/) is available for free across all platforms and was tested and working for this project. Other compilers should also work. The compiler command is issued from the ANACONDA command line as follows: 

	python -m numpy.f2py --compiler=mingw32 -c indexing_routines.f90 -m indexing_routines

CREDIT

This work has built on existing python code 'stltovoxel' by Christian Pedersen (https://github.com/cpederkoff/stl-to-voxel), which in turn uses 'stl_reader' by Sukhbinder Singh(http://sukhbinder.wordpress.com/2013/11/28/binary-stl-file-reader-in-python-powered-by-numpy/). This code would not function without their works. 


Dr Richard J Williams
r.williams16@imperial.ac.uk
Imperial College London
Nov 2020