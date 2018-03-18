# -*- coding: utf-8 -*-
'''
coordmode=J2000

HEAD = NAME   RA               DEC       TYPE  REPC  TDUR  OBS

#--------------

# 5x A-B, 5 min on A, 3 min on B

A          09:53:09         07:55:35.0      0     0    5    0

B          10:12:07        -18:37:04        1     5    3    0

#--------------

# 3x C-D, 5 min on each

C          10:03:20.4      -17:10:56.4      0     0    5    0 

D          10:05:39.8      -16:56:32.4      1     3    5    0

#--------------

# Does E-F-E-G-E-G-E-H-E-I; Each E taking 2 min, all others 3 min.

E          10:06:33.1      -16:20:18.6      0     2    2    0 

F          10:12:17.5      -03:44:48.0      1     1    3    0

G          10:03:33.4      -00:12:15.0      1     2    3    0

H          10:04:16.6      -01:41:33.4      1     1    3    0

I          09:53:09         07:55:35.0      1     1    3    0

#--------------

# 2x Tracks, 4 min each, on PSR

PSR                                        -1     2    4    0

#--------------

# 5x A_1-B_1, 5 min on A_1, 3 min on B_1

A_1        09:53:09         07:55:35.0      0     0    5    0

B_1        10:12:07        -18:37:04        1     5    3    0

 

NOTE:  Cannot use the same source name in a catalog as only the last instance is picked up by Astrid.  Instead, just use a modified source name, as I did for the last sequence.

 

-------------------------------
'''
 

#Potential observing script

 

fname = '/users/jwright/yourcatname.cat'

cat = Catalog(fname)

 

s0=""

for s in cat.keys():

 

    type=cat[s]['type']

    tdur=cat[s]['tdur']

    repc=cat[s]['repc']

    obs=cat[s]['obs']

    # type:

    #      = -1, do a simple Track on the object

    #      = 0, don't observe but store away its info for the next type = 1

    #      = 1, Track the last type = 0 source, then Track the type = 1 source

    # repc:

    #      Number of times to repeat

    # tdur:

    #      Scan duration time in minutes

    # obs:

    #      = 0, not yet been observed

    #      = 1, has been observed

 

    if obs == 0:

        # Not yet observed

         if type == 0:

         # Flag the previous type 1 source as being observed

           # flagSrc(s0, fname)

 

           # Store info for the next type = 1 source

           s0 = s

           tdur0=tdur

 

         if type == 1:

         # Repeat Track'ing the last type = 0 and this type = 1 source

           for i in range(0,repc):

               Track(s0, None, tdur0*60)

               Track(s, None, tdur*60)

           # flagSrc(s, fname)

 

         if type == -1:

         # A simple repeat Track'ing

           for i in range(0,repc):

               Track(s, None, tdur*60)

           # flagSrc(s, fname)

 

 

To Do:

 

Add BT logging?

 

Maybe add a proper way of automatically determining the best calibrator?

 

Eventually, weâ€™d need to add a check that the source(s) are above a specified elevation at the start and end of a sequence.  The BT script does not but should include this check or, otherwise, the script will abort in the middle.

 

flagSrc required only if you want to skip automatically a source that has been observed previously.  Here's an example of flagSrc in pseudo code.  Need to convert to python

 

def flagSrc(srcName, fileName)

 

   open fileName for reading

   open temporary file for writing

 

   foreach inputLine in fileName

      if 1st field in inputLine == srcName && 4th field == 0 then

        replace 4th field with 1

        write to temporary file the altered input line

      else

        write to temporary file the input line

      endif

   endfor

   close fileName and temporary file

   Maybe rename fileName, embedding a timestamp in the new name?

   rename temporary file as fileName