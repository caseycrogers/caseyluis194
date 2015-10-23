from digifab import *
import math
import numpy

# Writing bounds #
bounds= numpy.asarray([[0,0,0],[150,150,150]])


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
    originalPos = randomMove(cloud, worstPT, radius, bounds)

    if not originalPos:
      return False

    after = hCloud(cloud,edges)
    if after > before:
      return True
    else:
      cloud[worstPTI] = originalPos

  return False

# Returns a number for goodness of fit given a point, higher = better
# DONE
def hPoint(cloud, edges, index):
  return worst_angle(cloud, edges, index)

# Returns a number for goodness of fit for the cloud, higher = better
# DONE
def hCloud(cloud, edges):
  worst = 0

  for i in range(len(cloud)):
    h = hPoint(cloud, edges, i)

    worst += h

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
# DONE
def randomMove(cloud, index, radius, bounds):
  
  rand_vec = numpy.random.uniform(0.0,25.0,3) # just to give a specific arbitrary direction
  rand_radius = numpy.random.uniform(0.0, radius, 1)[0]
  rand_norm = numpy.array([rand_vec[0]/rand_radius, rand_vec[1]/rand_radius, rand_vec[2]/rand_radius]) # normalize the vector to radius distance
  
  # Moving the point #
  mv_cloud = cloud[index].copy
  mv_cloud += rand_norm

  def dist(a,b):
    return numpy.linalg.norm(pts_to_vec(a,b))

  def off_bounds(pts,bds):
    return (bds[0][0] <= pts[0] <= bds[1][0]) and (bds[0][1] <= pts[1] <= bds[1][1]) and (bds[0][2] <= pts[2] <= bds[1][2])   

  t = 0
  
  while t < 10:
    for i in range(len(cloud)):
      if i != index and dist(mv_cloud,cloud[i]) > 15.0 and off_bounds(mv_cloud, bounds):
        og = cloud[index].copy
        cloud[i][0] = mv_cloud[0]
        cloud[i][1] = mv_cloud[1]
        cloud[i][2] = mv_cloud[2]
        return og

  return None

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
