import os
import datetime
import numpy as np
import glob
import numpy as np
from astropy.table import Table,join,Column
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
#from exoplanet_archive import download_NASA_exoplanet_archive_table as archive_table
#from me_def import compactString
from astropy.coordinates import EarthLocation
from astropy.time import Time
import matplotlib

'''
## TO START FROM SCRATCH ## 
coordinates = EarthLocation.of_site('Green Bank Telescope').lat,EarthLocation.of_site('Green Bank Telescope').lon

# Read file generated by Gummi

location = os.path.dirname(__file__)
fpath = os.path.join(location,'UT20180323T160000-UT20180326T000000_green_bank_target_up.csv')

gummi_transit = Table.read(fpath,format='ascii')

cols = gummi_transit.colnames
trans_planets = np.array([compactString(i) for i in gummi_transit['_pl_name']])
gummi_transit.add_column(Column(trans_planets,name='Planet Name'),index = 0)

transit_host_name = np.array([x[:-2] for x in trans_planets])   # 619 transiting planets

# Read names from NASA Exoplanet Archive
archive,colnames = archive_table()
pl_hosts = np.array(archive['pl_hostname'])
pl_letter = np.array(archive['pl_letter'])
archive_planets = np.array([compactString(pl_hosts[i]+pl_letter[i]) for i in range(0,len(pl_hosts))])
archive.add_column(Column(archive_planets,name='Planet Name'),index=0)

indices = []

for i in range(0,len(trans_planets)):
    indices.append(np.where(archive_planets == trans_planets[i])[0][0])
    
# Filtered table from NEA    
transiting_archive = archive[[indices]]

New_table = join(transiting_archive,gummi_transit)
#New_table.write(location+'transiting_planets_gummi_ra.csv',delimiter=',',format='ascii')




# Subset columns
Transit_sub = New_table['pl_hostname','ra','dec','Planet Name','st_dist','pl_orbper','pl_bmassj','st_teff','pl_discmethod','st_optmag','tr_midp_jd','pl_trandur']
Transit_sub.sort('st_dist')
Transit_sub.write(os.path.join(location,'transiting_planets_gummi_sub.csv'),delimiter=',',format='ascii')
'''

# IF FILE WITH REQD COLUMNS ALREADY EXISTS
location = os.path.dirname(__file__)
fpath = os.path.join(location,'transiting_planets_gummi_sub.csv')
Transit_sub=Table.read(fpath)

# Mask missing values
Transit_sub['pl_trandur'].fill_value = 0
Transit_sub['st_dist'].fill_value = np.nan


Trans_dur = Transit_sub.filled()['pl_trandur']
Transit_duration = [datetime.timedelta(days = x/2) for x in Trans_dur]
Transit_duration_half = Trans_dur/2
# Convert degrees to hours
Transit_sub['ra']/=15.


# Distance filter
i20 = Transit_sub['st_dist']<=20
i50 = (Transit_sub['st_dist']>20) & (Transit_sub['st_dist']<=50)
i100 = (Transit_sub['st_dist']>50) & (Transit_sub['st_dist']<=100)
igreat = Transit_sub['st_dist']>100
mask = Transit_sub['st_dist'].mask




'''
# Closest 100 stars from Tarter paper
##  http://iopscience.iop.org/article/10.1086/379320/fulltext/58676.text.html#tb2   ##
closest_100 = Table.read('C:/Users/shbhu/Box Sync/Courses/SETI/GBT/Tarter_2003_58676.tb2.txt',format='ascii.tab')
 
result_100=[]
b = np.array(closest_100['ID'])
 
for i in b: 
    a = (Simbad.query_object(i))
    if a != None:
        result_100.append(a)
        
Name = []
RA100 = np.zeros(len(result_100))
DEC100 = np.zeros(len(result_100))

        
for j in range(0,len(result_100)):
    a = result_100[j]['RA'][0].split(' ')
    a = (float(a[0])+float(a[1])/60.+float(a[2])/3600)
    RA100[j] = a
    a = result_100[j]['DEC'][0].split(' ')
    a = (float(a[0])+float(a[1])/60.+float(a[2])/3600)   
    DEC100[j] = a
    Name.append(result_100[j]['MAIN_ID'][0])


new_RA100 = Time((RA100-lst)/24. +start_time.jd,format='jd',scale='utc').datetime
'''

# Convert RA to time at Zenith
start_time = Time(datetime.datetime(2018,3,23,0),format='datetime',scale='utc')  # Friday midnight 23rd March
lst = start_time.sidereal_time('apparent','greenwich').value

new_x = Time((Transit_sub['ra']-lst)/24. + start_time.jd,format='jd',scale='utc').datetime


plt.title('Transiting Exoplanets')
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%m/%d  %H:00'))
plt.gcf().autofmt_xdate()
plt.plot(new_x[mask],Transit_sub['dec'][mask],'c.',alpha=0.4,label='d = nan')

#plt.plot(new_RA100,DEC100,'.y',alpha=0.4,label='Closest 100 d < 7 pc')
plt.plot(new_x[igreat],Transit_sub['dec'][igreat],'m.',alpha=0.4,label='d > 100 pc')
plt.plot(new_x[i100],Transit_sub['dec'][i100],'g.',alpha=0.4,label='50 < d <=100 pc')
plt.plot(new_x[i50],Transit_sub['dec'][i50],'r.',alpha=0.4,label='20 < d <=50 pc')
plt.plot(new_x[i20],Transit_sub['dec'][i20],'b.',alpha=0.5,label='d <=20 pc')


plt.legend(loc=8,ncol=2)

plt.show()

# Plot for transit center time
'''
#USING SCATTER PLOT
cmap = matplotlib.cm.Spectral
colour = Transit_sub['st_teff']

plt.figure()
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%m/%d  %H:00'))
plt.gcf().autofmt_xdate()
plt.scatter(Time(Transit_sub['tr_midp_jd'],format='jd',scale='utc').datetime,Transit_sub['st_dist'],c=colour,s=10,cmap=cmap)
#plt.errorbar(Time(Transit_sub['tr_midp_jd'],format='jd',scale='utc').datetime,Transit_sub['st_dist'],xerr=Transit_duration,fmt='o',c=colour)

plt.xlabel('Transit midpoints')
plt.ylabel('Distance (pc)')
plt.xlim(min(Time(Transit_sub['tr_midp_jd'],format='jd',scale='utc').datetime),max(Time(Transit_sub['tr_midp_jd'],format='jd',scale='utc').datetime))
plt.title('Transiting Exoplanets for GBT March 23-25')
plt.show()

cbar = plt.colorbar()
cbar.set_label('Stellar Temperature (K)', rotation=270)
'''

#####
'''

# USING PLT.PLOT()
values = Transit_sub['st_teff']
vmin = min(values)
vmax = max(values)

# Define colour scheme
cmap = matplotlib.cm.Spectral
# Establish colour range based on variable
norm = matplotlib.colors.Normalize(vmin=vmin, vmax=vmax)

# Need to establish a scalar mappable surface since plt.plot is not mappable
sm = plt.cm.ScalarMappable(cmap=cmap, norm=norm)
# Set Array 
sm._A=[]

plt.figure()
# Format x axis for dates
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%m/%d  %H:00'))
plt.gcf().autofmt_xdate()


for i in range(len(values)):
    color = cmap(norm(values[i]))
    #plt.plot(Time(Transit_sub['tr_midp_jd'],format='jd',scale='utc').datetime[i],Transit_sub['st_dist'][i], linestyle='none', color=color, marker='o')
    plt.errorbar(Time(Transit_sub['tr_midp_jd'],format='jd',scale='utc').datetime[i] - datetime.timedelta(hours=4),Transit_sub['dec'][i],xerr=Transit_duration[i],fmt='o',color=color)


plt.xlabel('Transit midpoints (Local ET)')
plt.ylabel('Declination')
#plt.xlim(min(Time(Transit_sub['tr_midp_jd'],format='jd',scale='utc').datetime),max(Time(Transit_sub['tr_midp_jd'],format='jd',scale='utc').datetime))
plt.title('Transiting Exoplanets for GBT March 23-25')
plt.show()
cbar=plt.colorbar(sm)
cbar.set_label('Stellar Temperature (K)', rotation=270)
'''
#####################################################################

# Find and add ingress, egress
egress = Transit_sub['tr_midp_jd'] + Transit_duration_half
egress = np.array(Time(egress,format='jd',scale='utc').datetime -  datetime.timedelta(hours=4))
ingress = Transit_sub['tr_midp_jd'] - Transit_duration_half
ingress = np.array(Time(ingress,format='jd',scale='utc').datetime -  datetime.timedelta(hours=4))
tr_midp_date = Time(Transit_sub['tr_midp_jd'],format='jd',scale='utc').datetime - datetime.timedelta(hours=4)

Transit_sub.add_column(Column(ingress,name='Ingress'),index=0)
Transit_sub.add_column(Column(egress,name='Egress'),index=0)
Transit_sub.add_column(Column(tr_midp_date,name='Tr_midp_date'),index=0)

# Filter for time period
target_indices = np.where((ingress >  datetime.datetime(2018, 3, 25, 5)) & (egress <  datetime.datetime(2018, 3, 25, 17)))[0]
Transit_targets = Transit_sub[target_indices]

# Time cushion between ingress and egress
time_cushion = 0.75

def radec_distance_exact(ra1,dec1,ra2,dec2):
    #Returns the angular separation between a pair of stars in DEGREES, assuming it is fed equatorial coordinates in DEGREES.
    ra1 = ra1 * np.pi / 180.
    ra2 = ra2 * np.pi / 180.
    dec1 = dec1 * np.pi / 180.
    dec2 = dec2 * np.pi / 180.
    return 180/np.pi * np.arccos( np.sin(ra1) * np.sin(ra2) + np.cos(ra1) * np.cos(ra2) *  np.cos(np.abs(dec2 - dec1)) )
 
coincident1 = []
coincident2 = []

for i in range(0,len(target_indices)):
    for j in range(i+1,len(target_indices)):
        ang_dist = radec_distance_exact(Transit_targets['ra'][i]*15.,Transit_targets['dec'][i],Transit_targets['ra'][j]*15.,Transit_targets['dec'][j])
        if ((ang_dist>2) & (ang_dist<=4)) & (Transit_targets['Egress'][i] - Transit_targets['Ingress'][j] > datetime.timedelta(hours=time_cushion)) & (Transit_targets['Egress'][j] - Transit_targets['Ingress'][i] > datetime.timedelta(hours=time_cushion)):
            coincident1.append(i)
            coincident2.append(j)            
            #print(ang_dist,Transit_targets['Ingress'][i],Transit_targets['Egress'][i],Transit_targets['Ingress'][j],Transit_targets['Egress'][j])
            
coincident1 = np.array(coincident1)
coincident2 = np.array(coincident2)

Trans_dur = Transit_targets.filled()['pl_trandur']
Transit_duration = [datetime.timedelta(days = x/2) for x in Trans_dur]        
                        
##############################################################################
# USING PLT.PLOT()
values = Transit_targets['st_dist']
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

plt.figure()
# Format x axis for dates
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%m/%d  %H:%M'))
plt.gcf().autofmt_xdate()



for i in coincident1:
    color = cmap(norm(values[i]))
    #plt.plot(Time(Transit_sub['tr_midp_jd'],format='jd',scale='utc').datetime[i],Transit_sub['st_dist'][i], linestyle='none', color=color, marker='o')
    plt.errorbar(Transit_targets['Tr_midp_date'][i],Transit_targets['dec'][i],fmt='o',xerr=Transit_duration[i],color=color)
    #plt.errorbar(Transit_targets['ra'][i],Transit_targets['dec'][i],fmt='o',color=color)


plt.xlabel('Transit midpoints (Local ET)')
plt.ylabel('Declination')
#plt.xlim(min(Time(Transit_sub['tr_midp_jd'],format='jd',scale='utc').datetime),max(Time(Transit_sub['tr_midp_jd'],format='jd',scale='utc').datetime))
plt.title('Transiting Exoplanets for GBT March 23-25')
plt.show()
cbar=plt.colorbar(sm)
cbar.set_label('Stellar Distance (pc)', rotation=270)

def find_it(dec,tr_midp):
    threshold = 0.1
    thresh_time = datetime.timedelta(hours=0.05)
    tr_midp_datetime = datetime.datetime(2018,3,25,*tr_midp)
    dec_dist = np.abs(dec - Transit_targets['dec'])
    euclid_time_dist = np.abs(tr_midp_datetime - Transit_targets['Tr_midp_date'])
    a = np.where((dec_dist < threshold) & (euclid_time_dist < thresh_time))[0]
   
    return Transit_targets['pl_hostname'][a],Transit_targets['dec'][a],a
  
def find_companions(dec,tr_midp):
    '''
    INPUT: 
        dec : In degrees [scalar]. Eg. 43.21
        tr_midp : List of hours and minutes, assumes March 25th. Example : [12,43]. This implies 2018,3,25,12,43 or 12.43pm on 25th March 2018
    OUTPUT:
        The first output is the name of the primary, the names after that are the pairs it can match with.
    '''
    index = find_it(dec,tr_midp)[2]
    list1_pairs = np.where(np.array(coincident1)==index)[0]   
    list2_pairs = coincident2[list1_pairs]
 
    targets = Transit_targets['pl_hostname'][list2_pairs]
    
    return Transit_targets['pl_hostname'][index],targets


'''    
def find_it_ra(ra,dec):
    threshold_dec = 0.2
    threshold_ra = 0.2

    dec_dist = np.abs(dec - Transit_targets['dec'])
    ra_dist = np.abs(ra - Transit_targets['ra'])
    a = np.where((dec_dist < threshold_dec) & (ra_dist < threshold_ra))[0]

    
    return Transit_targets['pl_hostname'][a],Transit_targets['dec'][a],a
'''
#Bower_2009 = Table.read(location+'\\bower_2009_apj316039t2_ascii.txt',format='ascii')
