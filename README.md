HDF5 custom output subroutines for NBODY6

INSTALLATION
1) Download the custom ouput subroutine from http://silkroad.bao.ac.cn/~maxwell/hdf5
2) Uncompress the package: 
    tar zxvf nb6_custom_output.tar.gz
3) Copy the source code ``custom_output.f'' to the Ncode/ directory
4) Modify the Makefile: 
    add the ``custom_output.f'' to the src list
    Change the compiler ``FC = gfortran'' to ``FC = h5pfc''
    For the GPU2 version, modify the ``Makefile.build’’ under the GPU2/ directory, change the compiler ``gfortran'' in the make rule ``gpu'' to ``h5pfc'':
        gpu: $(OBJECTS)
            h5pfc -o nbody6 $(FFLAGS) $(OBJECTS)  -fopenmp $(LIBCUDA)  -lstdc++ -fPIC -fopenmp -Wall -O3

5) Add a call to the custom output subroutines
    ==> For the serial version of NBODY6, edit ``intgrt.f'', add the following line after the ``END IF'' statement of ``GO TO 50'' (around line 340):
        CALL output_intgrt(NXTLST, NXTLEN, 1)
    ==> For the GPU2 version of NBODY6, switch to the GPU2/ directory:
        cd ..
        cd GPU2/
        Edit the source code ``intgrt.omp.f'', Insert the following line BEFORE the comment ``Exit on KS termination'' (around line 576):
        CALL output_intgrt(NXTLST, NXTLEN, 1)

6) Install the HDF5 library from the source
    ==> Download the source code: http://www.hdfgroup.org/HDF5/release/obtainsrc.html
    ==> Uncompress the source code package:
        tar zxvf hdf5.xx
    ==> Enter the uncompressed directory
        cd hdf5..xx/
    ==> Configure the source code:
        ./configure --enable-parallel --enable-fortran --prefix=/usr/local
    ==> Compile and install
        make & make install (you may need the root permisson to execute the ``make install'' command
7) Compile the NBODY6 code:
    ==> For the serial version of NBODY6:
        Switch to the Ncode/ directory, and type ``make''
    ==> For the GPU2 version of NBODY6:
        Switch to the GPU2 directory, and type ``make gpu''

8) After the compilation you should get an executable called ``nbody6'' for the serial version or ``nbody6.gpu'' for the GPU2 version. This is the executable capable of producing HDF5 outputs.




CONFIGRATION OF OUTPUT OPTIONS
In NBODY6, option #46 and #47 are used to comfigure the output file type and output frequencies, respectively.

    KZ(46) = 1: Output as HDF5 (active particles only)
    KZ(46) = 3: Output as HDF5 (all particles)
    KZ(46) = 2: Output as CSV  (active particles only)
    KZ(46) = 5: Output as CSV  (all particles)
    KZ(47):     Controls the output frequency. Each N-body unit will have 2^KZ(47) outputs.


BUGS, QUESTIONS & FEEDBACK
    Please contact Maxwell Xu CAI: maxwellemail@gmail.com


