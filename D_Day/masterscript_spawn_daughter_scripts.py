import numpy as np

scriptdirectory = ''

targets = np.array([['kepler992b','kepler960b'],['kepler1039b','kepler1098b'],['kepler732c','kepler738b'],
['kepler1053b','kepler1164b'],['kepler1332b','kepler537b'],['kepler446b','kepler723b']]).flatten()

transit_times = []
catdir = ""
catname = ""
logdir = ""
midpoint = ""
targetname = ""


content = """

# Sample script to be reproduced to observe transit midpoint of target.
import time
import subprocess
import os
from __future__ import print_function

# Directory in which the target catalogue is there
catdir = {}
# Specify target catalogue file name
catname = {}

# Directory to log file
logdir = {}
# Log file name 
logfname = 'GBT_20180325_lband_psu.log'
logfile = os.path.join(logdir,logfname)

# Path to Target catalogue
target_cat = os.path.join(catdir,catname)

Catalog(target_cat)


obs_time = 60.0 * 5

midpoint = {} # Specify local time of midpoint transit
targetname = {} 


start = time.ctime(time.time())
print("Beginning tracking of '%s' at %s." %(targetname,start))
Track(targetname,endOffset=None,scanDuration=obs_time)
end = time.ctime(time.time())
print ("'%s' observed. Midpoint was at %s. Tracking ended at %s" %(targetname,midpoint,end))

with open(logfile, 'a') as fh:
    fh.write("Tracking for target %s completed at %s" %(targetname,end))

""".format(catdir,catname,logdir,midpoint,targetname)
    
    
#format(catdir,catname,logdir,midpoint,targetname)    
