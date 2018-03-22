import os
import datetime
import numpy as np
import glob
import numpy as np
from astropy.table import Table,join,Column
import matplotlib.pyplot as plt
import astropy.units as u
from astroplan import EclipsingSystem, Observer, FixedTarget
from astropy.coordinates import SkyCoord
from astropy.time import Time
import warnings
import string
import nasa_exoplanet_archive as archive
from astroquery.simbad import Simbad
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


cmap = matplotlib.cm.Spectral
colour = st_dist

for i in range(0,len(targets)):
    plt.scatter(ra[i],dec[i],
    plt.text(ra,dec,targets)