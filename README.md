# stl2inp
 Produce a cubic, fully structured Abaqus finite element mesh from STL files.

Welcome to stl2inp, 

BACKGROUND
 
The code will take any .stl model and write out an Abaqus inp file containing a structured, fully cubic mesh of the stl object.This was developed to perform additive manufacturing process simulations, where object of complex topology are frequently encountered.The code may, however, be of use in other sitations. 

EXECUTION
I have not currently set this up to run from the command line, rather use an IDE and modify the "wrapper.py" script to read a given .stl object and write where you please.I may change this once the code is robust, however at the present time it is WIP. Inaccuracies persist in slicing the stl into a stack of pixels. I have added a function named point_adder.py to add a row of elements which can be used to patch and repair any errors in the generated .inp file, for now.

The script calls on a (freeform) FORTRAN subroutine, "fortran_subroutine.f90" to index finite elements from nodal coordinates. This must be compiled for python beforehand using the f2py module which is built into the numpy library. The GNU FORTRAN compiler (gcc.gnu.org/fotran/) is available for free across all platforms and was tested and working for this project. Other compilers should also work. The compiler command is issued from the ANACONDA command line as follows: 

 python -m numpy.f2py --compiler=mingw32 -c fortran_source.f90 -m output_name

CREDIT

This work has built on existing python code 'stltovoxel' by Christian Pedersen (https://github.com/cpederkoff/stl-to-voxel), which in turn uses 'stl_reader' by Sukhbinder Singh(http://sukhbinder.wordpress.com/2013/11/28/binary-stl-file-reader-in-python-powered-by-numpy/)  . 


Dr Richard J Williams
Imperial College London
Oct 2020
