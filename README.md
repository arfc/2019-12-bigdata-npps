# 2019-BigData_NPPs
Big Data for NPPs Workshop, The Ohio State University Columbus, OH - Dec. 10-11, 2019.

Power point presentation for the results: '12-11-19_Presentation-for-BigData-for-NPPS.pptx'

Put "framework/CodeInterfaces/Serpent" directory to your raven installation directory. 

Installation: Just follow the instructions given in the user manual or website of Raven. 

For the issuses related to running the Raven in BlueWaters, look up 'issues_with_raven.txt'.  

Running Raven Framework:

1. Run 'raven_framework grid.xml' in your computer or use job file for BlueWaters. This produces 'Grid_output.csv' and 'hdf5_database.h5' files.  
2. Use 'FeedbackCalc.py' and 'Grid_output.csv' files to obtain the total feedback coefficients. Or run 'raven_framework rom.xml'.
3. Finally, run 'clusterer.py' and 'regressor.py' for cluster and regression analyses.
