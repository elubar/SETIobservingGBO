def in_interval(t1, dt=0.5):
  out = (t1 > ingress + dt) & (t1 < egress - dt)
  return out

def is_overlapping(in1, eg1, dt=0.5):
  '''in1: ingress time
     eg1: egress time
     dt: overlap time, in hours

     assumes ingress, egress are vectors of all target times'''
  if (in_interval(in1, dt)) | (in_interval(eg1, dt)):
    return True
  else:
    return False


