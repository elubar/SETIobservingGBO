import time
import subprocess
import os

catfile_name = 'BL_20180314_0300_C-band.cat'
catfile_dir = '/users/hisaacso/scripts'
catfile = os.path.join(catfile_dir,catfile_name)
logfile = '/users/jhickish/obs_log/'+catfile_name+'.log' #future logfile
newlinefile = '/users/jhickish/obs_log/newline_do_not_delete.absurd'