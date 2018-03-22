import numpy as np
from astropy.time import Time
import astropy.units as u
import datetime
import os

scriptdirectory = os.path.join(os.path.dirname(__file__),"Sample_midpoint_scripts")

targets = np.array([['kepler992b','kepler960b'],['kepler1039b','kepler1098b'],['kepler732c','kepler738b'],
['kepler1053b','kepler1164b'],['kepler1332b','kepler537b'],['kepler446b','kepler723b']]).flatten()

transit_times = ['2018-03-25 11:58:33.987',
 '2018-03-25 12:38:42.374',
 '2018-03-25 12:29:59.162',
 '2018-03-25 12:15:50.923',
 '2018-03-25 12:41:15.775',
 '2018-03-25 13:00:16.719',
 '2018-03-25 13:47:06.685',
 '2018-03-25 14:00:07.211',
 '2018-03-25 14:18:36.719',
 '2018-03-25 14:51:48.987',
 '2018-03-25 16:18:09.557',
 '2018-03-25 15:23:15.287']
# in UTC

midptime = [Time(datetime.datetime.strptime(i,"%Y-%m-%d %H:%M:%S.%f"),format='datetime',scale='utc') - 4*u.hour - 2*u.min for i in transit_times]
midp_string = ["{}-{}".format(i.datetime.time().hour,i.datetime.time().minute) for i in midptime]

catdir = ""
catname = ""
logdir = ""

midpoint = ""
targetname = ""

for i in range(0,len(midp_string)):
    midpoint = midp_string[i]
    targetname = targets[i]

    content = """
    \nfrom __future__ import print_function
    \n# Sample script to be reproduced to observe transit midpoint of target.
    \nimport time
    \nimport subprocess
    \nimport os

    
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
    
    \nmidpoint = '{}' # Specify local time of midpoint transit
    \ntargetname = '{}' 
    
    \nreal_run = Now()
    \nif real_run: 
    \n    start = time.ctime(time.time())
    \n    print("Beginning tracking of '%s' at %s." %(targetname,start))
    \n    Track(t,endOffset=None,scanDuration=obs_time)
    \n    end = time.ctime(time.time())
    \n    print ("'%s' observed. Midpoint was at %s. Tracking ended at %s" %(targetname,midpoint,end))
    
    \n    with open(logfile, 'a') as fh:
    \n        fh.write("Tracking for target %s completed at %s" %(targetname,end))

    \nelse:
    \n    print('Not a real run')
    
    """.format(catdir,catname,logdir,midpoint,targetname)
    
    f = open(os.path.join(scriptdirectory,"{}_{}.py".format(midpoint,targetname)),'w')
    f.write(content)
    f.close()
    
    print(targetname)
    
        
 
