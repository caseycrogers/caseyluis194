from digifab import *
import math
import numpy

def cloud_optimize(cloud, edges):
  while(optimize(cloud, edges)):
    pass
  return

# Attempts ten times to improve the worst point in the cloud
# ALMOST DONE, BOUNDING BOX
def optimize(cloud, edges):
  # find the bounding box of the sculpture

  # finish

  i = 0
  while (i < 10):
    i += 1

    before = h(cloud, edges)
    worstPT = findWorstPoint(cloud, edges, bounds)
    originalPos = randomMove(worstPT, radius)

    if not originalPos:
      return false

    after = hCloud(cloud,edges)
    if after > before:
      return True
    else:
      cloud[worstPTI] = originalPos
      return False

  return False

# Returns a number for goodness of fit given a point, higher = better
# DONE
def hPoint(cloud, edges, index):
  return worst_angle(cloud, edges, index)

# Returns a number for goodness of fit for the cloud, higher = better
# DONE
def hCloud(cloud, edges):
  worst = None

  for i in range(len(cloud)):
    h = hPoint(cloud, edges, i)

    if worst == None:
      worst = h
    else:
      worst = min(h, worst)

  return worst

# Finds the point with the most acute diahedral angle
# DONE
def findWorstPoint(cloud, edges):
  worstPT = None
  worstVal = None

  for i in range(len(cloud)):
    h = hPoint(cloud, edges, i)

    if worstPT == None:
      worstVal = h
      worstPT = i
    elif h < worstVal:
      worstVal = h
      worstPT = i

  return worstPT


# Moves the point within radius sphere randomly
def randomMove(pt, radius, bounds):
  # make sure new point isn't too close to any other point - 15mm minimum
  # make sure new point isn't out of bounds
  # try ten times, if failure, return Null
  return original position of point

# Vector constructor #
# DONE
def pts_to_vec (pt_a, pt_b):
  start = numpy.asarray(pt_a)
  end = numpy.asarray(pt_b)
  vec = end - start
  return vec

# Find the diahedral angle given two vectors #
# DONE
def vectors_angle (vec_0, vec_1):
  dot_product = numpy.dot(vec_0, vec_1)
  vec_0_norm = numpy.linalg.norm(vec_0)
  vec_1_norm = numpy.linalg.norm(vec_1)
  return math.acos(dot_product / (vec_0_norm * vec_1_norm))

# Find the worst angle given a point # 
#DONE
def worst_angle (cloud, edges, p_i):
  neighbors_pts = neighbors_pts(edges, p_i)
  vector_lst = []
  angle_lst = []
  
  for i in range(len(neighbors_pts)):
    vector_lst.append(pts_to_vec(cloud[p_i], cloud[neighbors_pts[i]]))
  
  prev = vector_lst[-1]
  for i in (range(len(vector_list))):
    angle_lst.append(vectors_angle(axes[i], prev))
    prev = vector_lst[i]

  return min(angle_lst)


# Find the points a given point is connected to
# DONE
def neighbors(edges, index):
  n = []

  for edge in edges:
    if edge[0] == index:
      n.append(edge[1])
    elif edge[1] == index:
      n.append(edge[0])

  return n
