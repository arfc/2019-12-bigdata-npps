# 2019-BigData_NPPs
Big Data for NPPs Workshop, The Ohio State University Columbus, OH - Dec. 10-11, 2019

Put "framework/CodeInterfaces/Serpent" directory to your raven installation directory. 

Installation: Just follow the instructions given in the user manual or website of Raven. 


Issue-1: There is a bug in the latest Raven version when running an input file on a cluster. 
Solved: Modify your job file in the following way:

from "aprun -n 1 -d 32 raven_framework <input_file>"
to "aprun -n 1 -d 32 /bin/bash raven_framework <input_file>"

Issue-2: When summiting a job using job.pbs file,following error is emerging

socket_connect_unix failed: 15137
socket_connect_unix failed: 15137
socket_connect_unix failed: 15137
qstat: cannot connect to server (null) (errno=15137) could not connect to trqauthd
qstat: Error (15137 - could not connect to trqauthd) 
craylog: WARNING: log tmp dir /var/spool/cray/llm is not writable

