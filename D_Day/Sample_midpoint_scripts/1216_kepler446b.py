
    
from __future__ import print_function
    
# Sample script to be reproduced to observe transit midpoint of target.
    
import time
    
import subprocess
    
import os

    
    
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
    
    
midpoint = '1216' # Specify local time of midpoint transit
    
targetname = 'kepler446b' 
    
    
real_run = Now()
    
if real_run: 
    
    start = time.ctime(time.time())
    
    print("Beginning tracking of '%s' at %s." %(targetname,start))
    
    Track(t,endOffset=None,scanDuration=obs_time)
    
    end = time.ctime(time.time())
    
    print ("'%s' observed. Midpoint was at %s. Tracking ended at %s" %(targetname,midpoint,end))
    
    
    with open(logfile, 'a') as fh:
    
        fh.write("Tracking for target %s completed at %s" %(targetname,end))

    
else:
    
    print('Not a real run')
    
    