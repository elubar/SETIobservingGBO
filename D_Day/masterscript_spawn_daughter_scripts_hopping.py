import numpy as np
from astropy.time import Time
import astropy.units as u
import datetime
import os

scriptdirectory = os.path.join(os.path.dirname(__file__),"Sample_hopping_scripts")

sequence = [['KIC8462852','Kepler738b'],['Kepler738b','Kepler992b'],['Kepler1039b','Kepler732c'],['Kepler732c','Kepler1164b'],['Kepler738b','Kepler1332b'],
['Kepler1053b','Kepler738b'],['Kepler1164b','Kepler723b'],['Kepler723b','Kepler537b'],['Kepler1332b','Kepler723b'],['Kepler446b','Kepler723b'],['Kepler446b','Kepler723b']]
# Tabby, F: F,A: C,E: E,H: F,I: G,F: H,L: L,J: I,L: K,L: K,L:
start_times = np.array(['0700','0802','0845','0905','0951','1004','1022','1055','1127','1158','1222'])

catdir = '/users/jwright/astro585'
catname = 'GBT_20180325_lband_psu.cat'
logdir = '/users/jwright/astro585'

for i in range(0,len(start_times)):


    content = """
    \n# Sample script to be reproduced to do target hopping ABABAB....
    \n
    \nfrom __future__ import print_function
    \nimport time
    \nimport subprocess
    \nimport os
    \nimport numpy as np
    \n
    \n# Directory in which the target catalogue is there
    \ncatdir = '{}'
    \n# Specify target catalogue file name
    \ncatname = '{}'
    
    \n# Directory to log file
    \nlogdir = '{}'
    \n# Log file name 
    \nlogfname = 'GBT_20180325_lband_psu.log'
    \nlogfile = os.path.join(logdir,logfname)
    
    \n# Path to Target catalogue
    \ntarget_cat = os.path.join(catdir,catname)
    \nCatalog(target_cat)
    \nobs_time = 60.0 * 5
    \n
    \ntargetname = {}
    \ntargetlist = np.tile(targetname,24)
    \n
    \nreal_run = Now()
    \nif real_run: 
    \n    for t in targetlist:
    \n        start = time.ctime(time.time())
    \n        print("Beginning tracking of '%s' at %s." %(targetname,start))
    \n        Track(t,endOffset=None,scanDuration=obs_time)
    \n        end = time.ctime(time.time())
    \n        print ("'%s' observed. Tracking ended at %s" %(targetname,end))
    \n    
    \n        with open(logfile, 'a') as fh:
    \n            fh.write("Tracking for target %s completed at %s" %(targetname,end))
    \n
    \nelse:
    \n    print('Not a real run')
    

    """.format(catdir,catname,logdir,sequence[i])
    
    f = open(os.path.join(scriptdirectory,"{}_{}_{}_hopping.py".format(start_times[i],sequence[i][0],sequence[i][1])),'w')
    f.write(content)
    f.close()
    
    print(sequence[i])
    
        
 
