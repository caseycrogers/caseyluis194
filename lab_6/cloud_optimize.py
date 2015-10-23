from digifab import *
import math
import numpy

def cloud_optimize(cloud, edges):
  while(optimize(cloud, edges)):
    pass
  return

# Attempts ten times to improve the worst point in the cloud
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
def hPoint(cloud, edges, index):

  return number

# Returns a number for goodness of fit for the cloud, higher = better
def hCloud(cloud, edges):
  return number

# Finds the point with the most acute diahedral angle
def findWorstPoint(cloud, edges):
  return worst point


# Moves the point within radius sphere randomly
def randomMove(pt, radius, bounds):
  # make sure new point isn't too close to any other point
  # make sure new point isn't out of bounds
  # try ten times, if failure, return Null
  return original position of point

# Vector constructor #
def pts_to_vec (pt_a, pt_b):
  start = numpy.asarray(pt_a)
  end = numpy.asarray(pt_b)
  vec = end - start
  return vec

# Find the diahedral angle given two vectors #
def vectors_angle (vec_0, vec_1):
  dot_product = numpy.dot(vec_0, vec_1)
  vec_0_norm = numpy.linalg.norm(vec_0)
  vec_1_norm = numpy.linalg.norm(vec_1)
  return math.acos(dot_product / (vec_0_norm * vec_1_norm))

# Find the points a given point is connected to
def neighbors(edges, index):
  n = []
  for edge in edges:
    if edge[0] == index:
      n.append(edge[1])
    elif edge[1] == index:
      n.append(edge[0])
  return n
