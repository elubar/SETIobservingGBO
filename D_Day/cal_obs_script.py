# Script to observe cal source. Need to specify fluxcal directory and catalogue name
from __future__ import print_function
import time
import subprocess



Catalog("fluxcal")

# Cal source suggested by Ron
cal='3C295'

#cal = '3C48'

# Observe cal source for x seconds
calexptime = 120 #[s]

#OnOff(cal,endOffset=None,scanDuration=calexptime)
OnOff(cal, Offset('AzEl', 1.0, 0.0, cosv=False), calexptime, '1')

print('Observed cal source -  {} at {} for {} seconds'.format(cal,time.ctime(time.time())),calexptime)

