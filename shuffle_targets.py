def shuffle_list(in_list, sequence, repeat=1):
  '''
  inlist = list of strings
  sequence = [integers]
  '''

  out = []

  for r in range(repeat):
    for s in sequence:
      out.append( in_list[s] )

  return out


def shuffle2(in_list, sequence, repeat=1, nobj=None):

  if not nobj:
    return shuffle_list( in_list, sequence, repeat )

  else:
    out = []
    nsets = len(in_list) / nobj
    if nsets - round(nsets) > 0.1:
      print('aborting.')
      return
    else:
      nsets = int(nsets)

    for i in range(nsets):
      istart, iend = [ i*nobj,  (i+1)*nobj]
      print((istart, iend))
      ls = in_list[istart:iend]
      print(ls)
      ls2 = shuffle_list( ls, sequence, repeat )
      for o in ls2:
        out.append(o)

  return out

# example: 
# shuffle2(['a', 'b', 'c', 'd'], [0,1],2,nobj=2)
