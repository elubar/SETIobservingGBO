import time
import subprocess
import os
from __future__ import print_function

catfile_name = "GBT_20180325_lband_psu.cat"
catfile_dir = os.path.dirname(__file__)
catfile = os.path.join(catfile_dir,catfile_name)
logfile = '/users/jwright/obs_log/'+catfile_name+'.log' #future logfile


Catalog(catfile)
Catalog(fluxcal)


#If needed, specify the calibrator here:
cal='3C227'
print('cal %s' % cal)


# If log file does not exist, no observations have been made yet. Hence look at Cal source
ck_file = os.path.isfile(logfile)
if ck_file == False: #only observe if no other stars have been observed
   Track(cal,endOffset=None,scanDuration=120)  #endOffset set to None, it can be used when surveying or mapping
                                               # Then does not stop at the target. Scans through

obs_time = 60.0 * 5
# The number of times to on/off cycle sources. This only affects on_off_sources
# on_only_sources are observed for one obs_time
n_cycles = 1

on_only_srcs = []

def on_only(on, on_time,ind,logfile):
    '''
    INPUT:
        on = Source name
        on_time = Exposure time. Nominally 300 seconds [sec]
        ind = Index of source in on_only_source (No of objects observed)
        logfile = Directory + File name for Log file
        
        
    '''
    # Check if run is real using Now()?    
    real_run = Now()
    if real_run: 
        # If real then open log file and read number of entries.
        # If log file does not exist, create one.
        with open(logfile, 'a+') as log:
            log.seek(0)
            observed = log.readlines()      
            print('Length observed',len(observed))
        if len(observed) <= ind:
            Slew(on)
            Track(on,endOffset=None,scanDuration=on_time)
            with open(logfile, 'a') as fh:
                fh.write("%.3f: %s \n"%(time.time(),"Tracking completed %s"%on))
            print('ind,len = ',ind,len(observed))
        else:
            print('Already observed. Skipping: ',str(on))
            print('ind, Length(observed): ',ind,len(observed))
            return
    else:
        print('Not a real run')
        

# on_only sources are likely to be diagnostic, so observe these first
for ind, source in enumerate(on_only_srcs):
    on_only(source, obs_time,ind,logfile)

n_on_only_srcs = len(on_only_srcs)
n_slews =  n_on_only_srcs
slew_time = 30 * n_slews #approx (a.k.a. made-up)
total_obs_time = obs_time * (n_on_only_srcs )
print('Observing for %d minutes (%d seconds)'%(total_obs_time//60, total_obs_time))
print('Observation will end at approximately', time.ctime(time.time() + total_obs_time + slew_time))


