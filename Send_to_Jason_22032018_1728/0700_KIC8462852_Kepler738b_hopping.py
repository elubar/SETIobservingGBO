
    
# Sample script to be reproduced to do target hopping ABABAB....
    

    
from __future__ import print_function
    
import time
    
import subprocess
    
import os
    
import numpy as np
    

    
# Directory in which the target catalogue is there
    
catdir = '/users/jwright/astro585'
    
# Specify target catalogue file name
    
catname = 'GBT_20180325_lband_psu.cat'
    
    
# Directory to log file
    
logdir = '/users/jwright/astro585'
    
# Log file name 
    
logfname = 'GBT_20180325_lband_psu.log'
    
logfile = os.path.join(logdir,logfname)
    
    
# Path to Target catalogue
    
target_cat = os.path.join(catdir,catname)
    
Catalog(target_cat)
    
obs_time = 60.0 * 5
    

    
targetname = ['KIC8462852', 'Kepler738b']
    
targetlist = np.tile(targetname,24)
    

    
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
    

    