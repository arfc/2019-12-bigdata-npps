# 2019-BigData_NPPs
Big Data for NPPs Workshop, The Ohio State University Columbus, OH - Dec. 10-11, 2019


Installation: Just follow the instructions given in the user manual or website of Raven. 
Important: There is a bug in the latest Raven version when running an input file on a cluster. Modify your job file in the following way:

from "aprun -n 1 -d 32 raven_framework <input_file>"
to "aprun -n 1 -d 32 /bin/bash raven_framework <input_file>"



Put "framework/CodeInterfaces/Serpent" directory to your raven installation directory. 

