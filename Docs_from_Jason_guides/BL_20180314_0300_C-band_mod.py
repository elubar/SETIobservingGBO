import time
import subprocess
import os
catfile_name = 'BL_20180314_0300_C-band.cat'
catfile_dir = '/users/hisaacso/scripts/'
catfile = catfile_dir + catfile_name
logfile = '/users/jhickish/obs_log/'+catfile_name+'.log' #future logfile
newlinefile = '/users/jhickish/obs_log/newline_do_not_delete.absurd'

Catalog(catfile)
Catalog(fluxcal)
cat = Catalog('/users/hisaacso/catalogs/fluxcal2.cat')

# Choose calibrator that is nearest to current LST
lst = GetLST()
# Dummy value when validating
if lst is None:
    lst = 16

for s in cat.keys():
    #h, m, s = cat[s]['ra'].split(':')
    #ra = float(h) + float(m)/60.0 + float(s)/3600.0
    ra = cat[s]['ra']/15.0
    ha = lst - ra
    if ha < -12:
        ha += 24
    elif ha > +12:
        ha -= 24
    if abs(ha) < min:
        min = abs(ha)
        cal = s

print('LST %f' % lst)
print('cal %s' % cal)

#If needed, specify the calibrator here:
#cal='3C227'

ck_file = os.path.isfile(logfile)
if ck_file == False: #only observe if no other stars have been observed
   Track(cal,endOffset=None,scanDuration=120)  #endOffset set to None, it can be used when surveying or mapping

with open(newlinefile, 'r') as fh:
    newline = fh.read()

# This script assumes all sources are observed for the same amount of time
# and there are no 'off' positions, only named stars used as off positions.
# Read the sources from the catalog file and put them in a nice list.

# Put sources which have no off positions (e.g. pulsars) in this list
on_only_srcs = [
'DIAG_PSR_J0953+0755',
'HIP49973',
'HIP49258',
'HIP49973',
'HIP49444',
'HIP49973',
'HIP49512',
'HIP49986',
'HIP49280',
'HIP49986',
'HIP49335',
'HIP49986',
'HIP49390',
'HIP50341',
'HIP49812',
'HIP50341',
'HIP50202',
'HIP50341',
'HIP50213',
'HIP50384',
'HIP49677',
'HIP50384',
'HIP49691',
'HIP50384',
'HIP49719',
'HIP50564',
'HIP49831',
'HIP50564',
'HIP49882',
'HIP50564',
'HIP49970',
'HIP65420',
'HIP64674',
'HIP65420',
'HIP64721',
'HIP65420',
'HIP64963',
'HIP65714',
'HIP64960',
'HIP65714',
'HIP64980',
'HIP65714',
'HIP65360',
'HIP65859',
'HIP65104',
'HIP65859',
'HIP65130',
'HIP65859',
'HIP65214',
'HIP66077',
'HIP65363',
'HIP66077',
'HIP65416',
'HIP66077',
'HIP65510',
'HIP66147',
'HIP65496',
'HIP66147',
'HIP65578',
'HIP66147',
'HIP65599',
'HIP66193',
'HIP65443',
'HIP66193',
'HIP65541',
'HIP66193',
'HIP65612',
]# The observation time for each source per cycle. For on/off sources, both
# on and off observations are performed for this time.
obs_time = 60.0 * 5
# The number of times to on/off cycle sources. This only affects on_off_sources
# on_only_sources are observed for one obs_time
n_cycles = 1

def write_log_line(filename, message):
    with open(filename, 'a') as fh:
        fh.write("%.3f: %s"%(time.time(), message))
        fh.write(newline)

def test_real():
    real_run = Now()
    if real_run == None:
       print("Not a real run")
       return False
    else: 
       return True

def on_only(on, on_time,ind,logfile):
  real_run = test_real()
  if real_run:
    if not os.path.exists(logfile):
        # create file if it doesn't exist. There must be a better way.
        fh = open(logfile, 'w')
        fh.close()
        log=open(logfile,'r+')
        observed = []
    else:
        log = open(logfile,'r+')
        observed = []
        observed = log.readlines()
    print('len observed',len(observed))
    if len(observed) <= ind:
        Slew(on)
        Track(on,endOffset=None,scanDuration=on_time)
        if real_run: write_log_line(logfile, "Tracking completed %s"%on)
        print('ind,len,',ind,len(observed))
    else:
        print('Already observed. Skipping: ',str(on))
        print('ind, len(observed): ',ind,len(observed))
        return;

n_on_only_srcs = len(on_only_srcs)
n_slews =  n_on_only_srcs
slew_time = 30 * n_slews #approx (a.k.a. made-up)
total_obs_time = obs_time * (n_on_only_srcs )
print('Observing for %d minutes (%d seconds)'%(total_obs_time//60, total_obs_time))
print('Observation will end at approximately', time.ctime(time.time() + total_obs_time + slew_time))

# on_only sources are likely to be diagnostic, so observe these first
for ind, source in enumerate(on_only_srcs):
    on_only(source, obs_time,ind,logfile)

#for source in on_only_srcs:
#    on_only(source, obs_time)

# Lazy check that things are in the catalog
with open(catfile, 'r') as fh:
  # This split doesn't bother to discriminate between columns.
  catsplit = fh.read().split()

for source in on_only_srcs:
    if source not in catsplit:
        print('ERROR: %s does not exist in catalog %s'%(source, catfile))
        exit()

n_on_only_srcs = len(on_only_srcs)
n_slews =  n_on_only_srcs
slew_time = 30 * n_slews #approx (a.k.a. made-up)
total_obs_time = obs_time * (n_on_only_srcs )
print('Observing for %d minutes (%d seconds)'%(total_obs_time//60, total_obs_time))
print('Observation will end at approximately', time.ctime(time.time() + total_obs_time + slew_time))

