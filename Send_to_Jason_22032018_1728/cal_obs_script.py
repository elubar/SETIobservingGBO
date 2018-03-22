# Script to observe cal source. Need to specify fluxcal directory and catalogue name
from __future__ import print_function
import time
import subprocess
import os


# Directory in which the flux calibrator catalogue is there
fluxcal_catdir = '/users/jwright/astro585'
# Specify flux cal file name
fluxcal_catname = ''
fluxcal = os.path.join(fluxcal_catdir,fluxcal_catname)
# Load fluxcal catalogue
Catalog(fluxcal)

# Cal source suggested by Ron
cal='3C295'

# Observe cal source for x seconds
calexptime = 120 #[s]

Track(cal,endOffset=None,scanDuration=calexptime)

print('Observed cal source -  {} at {} for {} seconds'.format(cal,time.ctime(time.time())),calexptime)

