import os
import datetime
import numpy as np
import glob
import numpy as np
from astropy.table import Table,join,Column
import matplotlib.pyplot as plt
import astropy.units as u
from astropy.coordinates import SkyCoord
from astropy.time import Time
import warnings
import string
import nasa_exoplanet_archive as archive
from astroquery.simbad import Simbad
import matplotlib
obj = archive.NEA()

targets = np.array([['kepler992b','kepler960b'],['kepler1039b','kepler1098b'],['kepler732c','kepler738b'],
['kepler1053b','kepler1164b'],['kepler1332b','kepler537b'],['kepler446b','kepler723b']]).flatten()

coordinates = np.zeros((len(targets),2))

ra = np.zeros(len(targets))
dec = np.zeros(len(targets))
st_dist = np.zeros(len(targets))

for i in range(0,len(targets)):
    print(i)
    planet = obj.query_planet(targets[i])
    ra[i] = planet['ra'][0]
    dec[i] = planet['dec'][0]
    st_dist[i] = planet['st_dist'][0]

    plt.scatter(ra[i],dec[i])

plt.show()

new_target_name = 'KIC8462852'
targets = np.append(targets, new_target_name)
tabby = Simbad.query_object(new_target_name)
tabby_target = SkyCoord(ra=tabby['RA'][0], dec=tabby['DEC'][0],unit=(u.hourangle, u.deg))

ra = np.append(ra,tabby_target.ra.value)
dec = np.append(dec,tabby_target.dec.value)
st_dist = np.append(st_dist,390)

##############################################################################
# USING PLT.PLOT()
values = st_dist
vmin = min(values)
vmax = max(values)

# Define colour scheme
cmap =matplotlib.cm.Spectral
# Establish colour range based on variable
norm = matplotlib.colors.Normalize(vmin=vmin, vmax=vmax)

# Need to establish a scalar mappable surface since plt.plot is not mappable
sm = plt.cm.ScalarMappable(cmap=cmap, norm=norm)
# Set Array 
sm._A=[]

cmap = matplotlib.cm.Spectral


for i in range(0,len(targets)):
    color = cmap(norm(values[i]))
    plt.scatter(ra[i],dec[i],color = color)
    plt.text(ra[i],dec[i],targets[i])
    
plt.xlabel('RA')
plt.ylabel('Declination')
#plt.xlim(min(Time(Transit_sub['tr_midp_jd'],format='jd',scale='utc').datetime),max(Time(Transit_sub['tr_midp_jd'],format='jd',scale='utc').datetime))
plt.title('Transiting Exoplanets for GBT March 25')
plt.show()
cbar=plt.colorbar(sm)
cbar.set_label('Stellar Distance (pc)', rotation=270)