<html>
<head>
	<meta http-equiv="content-type" content="text/html; charset=utf-8">
	<title></title>
	<meta name="generator" content="LibreOffice 4.2.2.1 (MacOSX)">
	<meta name="created" content="20150729;164323910098000">
	<meta name="changed" content="20150729;164426658219000">
</head>
<body lang="en-US" dir="ltr">
<p style="margin-bottom: 0in; line-height: 100%"><font color="#000000"><font face="Helvetica, serif"><font size="2" style="font-size: 11pt"><span style="text-decoration: none">HDF5
custom output subroutines for NBODY6</span></font></font></font></p>
<p style="margin-bottom: 0in; line-height: 100%; text-decoration: none">
<br>
</p>
<p style="margin-bottom: 0in; line-height: 100%"><font color="#000000"><font face="Helvetica, serif"><font size="2" style="font-size: 11pt"><span style="text-decoration: none">INSTALLATION</span></font></font></font></p>
<p style="margin-bottom: 0in; line-height: 100%"><font color="#000000"><font face="Helvetica, serif"><font size="2" style="font-size: 11pt"><span style="text-decoration: none">1)
</span></font></font></font><font color="#000000"><font face="Helvetica, serif"><font size="2" style="font-size: 11pt"><span style="text-decoration: none">Download
the subroutines: <br>    git clone
https://github.com/maxwelltsai/nbhdf5.git</span></font></font></font></p>
<p style="margin-bottom: 0in; line-height: 100%"><font color="#000000"><font face="Helvetica, serif"><font size="2" style="font-size: 11pt"><span style="text-decoration: none">2)
Uncompress the package: </span></font></font></font>
</p>
<p style="margin-bottom: 0in; line-height: 100%"><font color="#000000"><span style="text-decoration: none">
   <font face="Helvetica, serif"><font size="2" style="font-size: 11pt">tar
zxvf nb6_custom_output.tar.gz</span></font></font></font></p>
<p style="margin-bottom: 0in; line-height: 100%"><font color="#000000"><font face="Helvetica, serif"><font size="2" style="font-size: 11pt"><span style="text-decoration: none">3)
Copy the source code ``custom_output.f'' to the Ncode/ directory</span></font></font></font></p>
<p style="margin-bottom: 0in; line-height: 100%"><font color="#000000"><font face="Helvetica, serif"><font size="2" style="font-size: 11pt"><span style="text-decoration: none">4)
Modify the Makefile: </span></font></font></font>
</p>
<p style="margin-bottom: 0in; line-height: 100%"><font color="#000000"><span style="text-decoration: none">
   <font face="Helvetica, serif"><font size="2" style="font-size: 11pt">add
the ``custom_output.f'' to the src list</span></font></font></font></p>
<p style="margin-bottom: 0in; line-height: 100%"><font color="#000000"><span style="text-decoration: none">
   <font face="Helvetica, serif"><font size="2" style="font-size: 11pt">Change
the compiler ``FC = gfortran'' to ``FC = h5pfc''</span></font></font></font></p>
<p style="margin-bottom: 0in; line-height: 100%"><font color="#000000"><span style="text-decoration: none">
   <font face="Helvetica, serif"><font size="2" style="font-size: 11pt">For
the GPU2 version, modify the ``Makefile.build’’ under the GPU2/
directory, change the compiler ``gfortran'' in the make rule ``gpu''
to ``h5pfc'':</span></font></font></font></p>
<p style="margin-bottom: 0in; line-height: 100%"><font color="#000000"><span style="text-decoration: none">
       <font face="Helvetica, serif"><font size="2" style="font-size: 11pt">gpu:
$(OBJECTS)</span></font></font></font></p>
<p style="margin-bottom: 0in; line-height: 100%"><font color="#000000"><span style="text-decoration: none">
           <font face="Helvetica, serif"><font size="2" style="font-size: 11pt">h5pfc
-o nbody6 $(FFLAGS) $(OBJECTS)  -fopenmp $(LIBCUDA)  -lstdc++ -fPIC
-fopenmp -Wall -O3</span></font></font></font></p>
<p style="margin-bottom: 0in; line-height: 100%; text-decoration: none">
<br>
</p>
<p style="margin-bottom: 0in; line-height: 100%"><font color="#000000"><font face="Helvetica, serif"><font size="2" style="font-size: 11pt"><span style="text-decoration: none">5)
Add a call to the custom output subroutines</span></font></font></font></p>
<p style="margin-bottom: 0in; line-height: 100%"><font color="#000000"><span style="text-decoration: none">
   <font face="Helvetica, serif"><font size="2" style="font-size: 11pt">==&gt;
For the serial version of NBODY6, edit ``intgrt.f'', add the
following line after the ``END IF'' statement of ``GO TO 50'' (around
line 340):</span></font></font></font></p>
<p style="margin-bottom: 0in; line-height: 100%"><font color="#000000"><span style="text-decoration: none">
       <font face="Helvetica, serif"><font size="2" style="font-size: 11pt">CALL
output_intgrt(NXTLST, NXTLEN, 1)</span></font></font></font></p>
<p style="margin-bottom: 0in; line-height: 100%"><font color="#000000"><span style="text-decoration: none">
   <font face="Helvetica, serif"><font size="2" style="font-size: 11pt">==&gt;
For the GPU2 version of NBODY6, switch to the GPU2/ directory:</span></font></font></font></p>
<p style="margin-bottom: 0in; line-height: 100%"><font color="#000000"><span style="text-decoration: none">
       <font face="Helvetica, serif"><font size="2" style="font-size: 11pt">cd
..</span></font></font></font></p>
<p style="margin-bottom: 0in; line-height: 100%"><font color="#000000"><span style="text-decoration: none">
       <font face="Helvetica, serif"><font size="2" style="font-size: 11pt">cd
GPU2/</span></font></font></font></p>
<p style="margin-bottom: 0in; line-height: 100%"><font color="#000000"><span style="text-decoration: none">
       <font face="Helvetica, serif"><font size="2" style="font-size: 11pt">Edit
the source code ``intgrt.omp.f'', Insert the following line BEFORE
the comment ``Exit on KS termination'' (around line 576):</span></font></font></font></p>
<p style="margin-bottom: 0in; line-height: 100%"><font color="#000000"><span style="text-decoration: none">
       <font face="Helvetica, serif"><font size="2" style="font-size: 11pt">CALL
output_intgrt(NXTLST, NXTLEN, 1)</span></font></font></font></p>
<p style="margin-bottom: 0in; line-height: 100%; text-decoration: none">
<br>
</p>
<p style="margin-bottom: 0in; line-height: 100%"><font color="#000000"><font face="Helvetica, serif"><font size="2" style="font-size: 11pt"><span style="text-decoration: none">6)
Install the HDF5 library from the source</span></font></font></font></p>
<p style="margin-bottom: 0in; line-height: 100%"><font color="#000000"><span style="text-decoration: none">
   <font face="Helvetica, serif"><font size="2" style="font-size: 11pt">==&gt;
Download the source code:
http://www.hdfgroup.org/HDF5/release/obtainsrc.html</span></font></font></font></p>
<p style="margin-bottom: 0in; line-height: 100%"><font color="#000000"><span style="text-decoration: none">
   <font face="Helvetica, serif"><font size="2" style="font-size: 11pt">==&gt;
Uncompress the source code package:</span></font></font></font></p>
<p style="margin-bottom: 0in; line-height: 100%"><font color="#000000"><span style="text-decoration: none">
       <font face="Helvetica, serif"><font size="2" style="font-size: 11pt">tar
zxvf hdf5.xx</span></font></font></font></p>
<p style="margin-bottom: 0in; line-height: 100%"><font color="#000000"><span style="text-decoration: none">
   <font face="Helvetica, serif"><font size="2" style="font-size: 11pt">==&gt;
Enter the uncompressed directory</span></font></font></font></p>
<p style="margin-bottom: 0in; line-height: 100%"><font color="#000000"><span style="text-decoration: none">
       <font face="Helvetica, serif"><font size="2" style="font-size: 11pt">cd
hdf5..xx/</span></font></font></font></p>
<p style="margin-bottom: 0in; line-height: 100%"><font color="#000000"><span style="text-decoration: none">
   <font face="Helvetica, serif"><font size="2" style="font-size: 11pt">==&gt;
Configure the source code:</span></font></font></font></p>
<p style="margin-bottom: 0in; line-height: 100%"><font color="#000000"><span style="text-decoration: none">
       <font face="Helvetica, serif"><font size="2" style="font-size: 11pt">./configure
--enable-parallel --enable-fortran --prefix=/usr/local</span></font></font></font></p>
<p style="margin-bottom: 0in; line-height: 100%"><font color="#000000"><span style="text-decoration: none">
   <font face="Helvetica, serif"><font size="2" style="font-size: 11pt">==&gt;
Compile and install</span></font></font></font></p>
<p style="margin-bottom: 0in; line-height: 100%"><font color="#000000"><span style="text-decoration: none">
       <font face="Helvetica, serif"><font size="2" style="font-size: 11pt">make
&amp; make install (you may need the root permisson to execute the
``make install'' command</span></font></font></font></p>
<p style="margin-bottom: 0in; line-height: 100%"><font color="#000000"><font face="Helvetica, serif"><font size="2" style="font-size: 11pt"><span style="text-decoration: none">7)
Compile the NBODY6 code:</span></font></font></font></p>
<p style="margin-bottom: 0in; line-height: 100%"><font color="#000000"><span style="text-decoration: none">
   <font face="Helvetica, serif"><font size="2" style="font-size: 11pt">==&gt;
For the serial version of NBODY6:</span></font></font></font></p>
<p style="margin-bottom: 0in; line-height: 100%"><font color="#000000"><span style="text-decoration: none">
       <font face="Helvetica, serif"><font size="2" style="font-size: 11pt">Switch
to the Ncode/ directory, and type ``make''</span></font></font></font></p>
<p style="margin-bottom: 0in; line-height: 100%"><font color="#000000"><span style="text-decoration: none">
   <font face="Helvetica, serif"><font size="2" style="font-size: 11pt">==&gt;
For the GPU2 version of NBODY6:</span></font></font></font></p>
<p style="margin-bottom: 0in; line-height: 100%"><font color="#000000"><span style="text-decoration: none">
       <font face="Helvetica, serif"><font size="2" style="font-size: 11pt">Switch
to the GPU2 directory, and type ``make gpu''</span></font></font></font></p>
<p style="margin-bottom: 0in; line-height: 100%; text-decoration: none">
<br>
</p>
<p style="margin-bottom: 0in; line-height: 100%"><font color="#000000"><font face="Helvetica, serif"><font size="2" style="font-size: 11pt"><span style="text-decoration: none">8)
After the compilation you should get an executable called ``nbody6''
for the serial version or ``nbody6.gpu'' for the GPU2 version. This
is the executable capable of producing HDF5 outputs.</span></font></font></font></p>
<p style="margin-bottom: 0in; line-height: 100%; text-decoration: none">
<br>
</p>
<p style="margin-bottom: 0in; line-height: 100%; text-decoration: none">
<br>
</p>
<p style="margin-bottom: 0in; line-height: 100%; text-decoration: none">
<br>
</p>
<p style="margin-bottom: 0in; line-height: 100%; text-decoration: none">
<br>
</p>
<p style="margin-bottom: 0in; line-height: 100%"><font color="#000000"><font face="Helvetica, serif"><font size="2" style="font-size: 11pt"><span style="text-decoration: none">CONFIGRATION
OF OUTPUT OPTIONS</span></font></font></font></p>
<p style="margin-bottom: 0in; line-height: 100%"><font color="#000000"><font face="Helvetica, serif"><font size="2" style="font-size: 11pt"><span style="text-decoration: none">In
NBODY6, option #46 and #47 are used to comfigure the output file type
and output frequencies, respectively.</span></font></font></font></p>
<p style="margin-bottom: 0in; line-height: 100%; text-decoration: none">
<br>
</p>
<p style="margin-bottom: 0in; line-height: 100%"><font color="#000000"><span style="text-decoration: none">
   <font face="Helvetica, serif"><font size="2" style="font-size: 11pt">KZ(46)
= 1: Output as HDF5 (active particles only)</span></font></font></font></p>
<p style="margin-bottom: 0in; line-height: 100%"><font color="#000000"><span style="text-decoration: none">
   <font face="Helvetica, serif"><font size="2" style="font-size: 11pt">KZ(46)
= 3: Output as HDF5 (all particles)</span></font></font></font></p>
<p style="margin-bottom: 0in; line-height: 100%"><font color="#000000"><span style="text-decoration: none">
   <font face="Helvetica, serif"><font size="2" style="font-size: 11pt">KZ(46)
= 2: Output as CSV  (active particles only)</span></font></font></font></p>
<p style="margin-bottom: 0in; line-height: 100%"><font color="#000000"><span style="text-decoration: none">
   <font face="Helvetica, serif"><font size="2" style="font-size: 11pt">KZ(46)
= 5: Output as CSV  (all particles)</span></font></font></font></p>
<p style="margin-bottom: 0in; line-height: 100%"><font color="#000000"><span style="text-decoration: none">
   <font face="Helvetica, serif"><font size="2" style="font-size: 11pt">KZ(47):
    Controls the output frequency. Each N-body unit will have
2^KZ(47) outputs.</span></font></font></font></p>
<p style="margin-bottom: 0in; line-height: 100%; text-decoration: none">
<br>
</p>
<p style="margin-bottom: 0in; line-height: 100%; text-decoration: none">
<br>
</p>
<p style="margin-bottom: 0in; line-height: 100%"><font color="#000000"><font face="Helvetica, serif"><font size="2" style="font-size: 11pt"><span style="text-decoration: none">BUGS,
QUESTIONS &amp; FEEDBACK</span></font></font></font></p>
<p style="margin-bottom: 0in; line-height: 100%"><font color="#000000"><span style="text-decoration: none">
   <font face="Helvetica, serif"><font size="2" style="font-size: 11pt">Please
contact Maxwell Xu CAI: maxwellemail_at_gmail.com</span></font></font></font></p>
<p style="margin-bottom: 0in; line-height: 100%; text-decoration: none">
<br>
</p>
<p style="margin-bottom: 0in; line-height: 100%; text-decoration: none">
<br>
</p>
<p style="margin-bottom: 0in; line-height: 100%"><br>
</p>
</body>
</html>
