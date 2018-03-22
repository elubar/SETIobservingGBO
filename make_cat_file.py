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

#t=Table(,names=('Pair','Name','RA','Dec','UTC_Ingress','UTC_midpoint','UTC_egress','Flux'))

start_query = Time('2018-03-25 11:00:00') # 7am to 1pm local
stop_query = Time('2018-03-25 18:00:00')

name = np.array([])
pair = np.array([]) # Assign pair numbers to each
ingress = np.array([])
egress = np.array([])
midpoint = np.array([])
ra = np.array([]) #hms
dec = np.array([]) #dms

def deg2sexagesimal(target_coord):
    ra = target_coord.ra.hms
    dec = target_coord.dec.dms
    try:    
        ra_string = "{}:{}:{}".format(int(ra.h),int(ra.m),round(ra.s,2))
        dec_string = "{}:{}:{}".format(int(dec.d),int(dec.m),round(dec.s,2))
    except:
        ra_string = "{}:{}:00".format(int(ra.h),int(ra.m))
        dec_string = "{}:{}:00".format(int(dec.d),int(dec.m))
        
    
    return ra_string,dec_string

warnings.filterwarnings('ignore', category=Warning, append=True)    

for i in range(0,len(targets)):
    pl_name = targets[i]
    try:
        target = obj.query_planet(pl_name)
        target_coord = SkyCoord(ra=target['ra']*u.deg, dec=target['dec']*u.deg)
        full = obj.find_next_fulltransit_observable(pl_name,observatory = Observer.at_site('GBT', timezone='US/Eastern'),start_query = start_query, stop_query = stop_query, min_local_time = datetime.time(6,0),
                                        max_local_time = datetime.time(18,0),min_altitude = 0, min_moon_sep = 0)
        mid = obj.find_next_midtransit_observable(pl_name,observatory = Observer.at_site('GBT', timezone='US/Eastern'),start_query = start_query, stop_query = stop_query, min_local_time = datetime.time(6,0),
                                        max_local_time = datetime.time(18,0),min_altitude = 0, min_moon_sep = 0)
    
        if full:
            pair = np.append(pair,string.ascii_uppercase[i])
            name = np.append(name,pl_name)
            ingress = np.append(ingress,full[0][0].datetime)
            egress = np.append(egress,full[0][1].datetime)
            midpoint = np.append(midpoint,mid)
            
            temp = deg2sexagesimal(target_coord)
            ra = np.append(ra,temp[0])
            dec = np.append(dec,temp[1])
            
    except ValueError:
        next
        
ingress = np.array(["'"+i.strftime("%Y/%m/%d %H:%M:%S") + " UTC'" for i in ingress])
egress = np.array(["'"+i.strftime("%Y/%m/%d %H:%M:%S") + " UTC'" for i in egress])
midpoint1 = np.array(["'"+i.datetime.strftime("%Y/%m/%d %H:%M:%S") + " UTC'" for i in midpoint])


new_target_name = 'KIC 8462852'
tabby = Simbad.query_object(new_target_name)
tabby_target = SkyCoord(ra=tabby['RA'][0], dec=tabby['DEC'][0],unit=(u.hourangle, u.deg))




#t=Table([pair,name,ra,dec,ingress,midpoint,egress,np.zeros(len(pair))],names=('NAME','RA','DEC','PAIR','UTC_INGRESS','UTC_MIDPOINT','UTC_EGRESS','OBS'))
t=Table([name,ra,dec,pair,ingress,midpoint1,egress,np.zeros(len(pair))],names=('','','','','','','',''))
t.add_row([new_target_name,*deg2sexagesimal(tabby_target),'M',"'2018/03/25 00:00:00 UTC'","'2018/03/25 00:00:00 UTC'","'2018/03/25 00:00:00 UTC'",0])

location = os.path.dirname(__file__)
t.write(os.path.join(location,'D_Day',"GBT_20180325_lband_psu.cat"), format='ascii.fixed_width') 

'''
f = open(os.path.join(location,'D_Day',"GBT_20180325_lband_psu.cat"),'r+')
#f.seek(0)
f.write('coordmode=J2000 \nHEAD = NAME    RA    DEC    PAIR    UTC_INGRESS    UTC_MIDPOINT     UTC_EGRESS    OBS                                     ')
f.close()
'''

'''
coordmode=J2000 
HEAD = NAME    RA    DEC    PAIR    UTC_INGRESS    UTC_MIDPOINT     UTC_EGRESS    OBS
'''
