
    
# Sample script to be reproduced to do target hopping ABABAB....
    

    
import time
    
import subprocess
    
import os
    
import numpy as np
    
from __future__ import print_function
    

    
# Directory in which the target catalogue is there
    
catdir = ''
    
# Specify target catalogue file name
    
catname = ''
    

    
# Directory to log file
    
logdir = ''
    
# Log file name 
    
logfname = 'GBT_20180325_lband_psu.log'
    
logfile = os.path.join(logdir,logfname)
    

    
# Path to Target catalogue
    
target_cat = os.path.join(catdir,catname)
    

    
Catalog(target_cat)
    

    
obs_time = 60.0 * 5
    

    
targetname = ['Kepler723b', 'Kepler537b']
    
targetlist = np.tile(targetname,12)
    

    
real_run = Now()
    
if real_run: 
    
    for t in targetlist:
    
        start = time.ctime(time.time())
    
        print("Beginning tracking of '%s' at %s." %(targetname,start))
    
        Track(t,endOffset=None,scanDuration=obs_time)
    
        end = time.ctime(time.time())
    
        print ("'%s' observed. Tracking ended at %s" %(targetname,end))
    
    
    
        with open(logfile, 'a') as fh:
    
            fh.write("Tracking for target %s completed at %s" %(targetname,end))
    

    
else:
    
    print('Not a real run')
    

    