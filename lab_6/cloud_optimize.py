from digifab import *
import math
import numpy

cloud_optimize(cloud, edges):
  while(optimize(cloud, edges)):
    pass
  return

# Attempts ten times to improve the worst point in the cloud
optimize(cloud, edges):
  # find the bounding box of the sculpture

  # finish


  i = 0
  while (i < 10):
    hBefore = h(cloud, edges)
    i += 1
    worstPT = findWorstPoint(cloud, edges, bounds)
    originalPos = randomMove(worstPT, radius)
  return false

# Returns a number for goodness of fit, higher = better
h(cloud, edges):
  return number

# Finds the point with the most acute diahedral angle
findWorstPoint(cloud, edges):
  return worst point


# Moves the point within radius sphere randomly
randomMove(pt, radius, bounds):
  # make sure new point isn't too close to any other point
  # make sure new point isn't out of bounds
  # try ten times, if failure, return Null
  return original position of point

# Find the diahedral angle given two vectors

# Find the worst diahedral angle in a point