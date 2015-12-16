#!/usr/bin/python

from digifab import *
import numpy
import solid

# USEFULL STUFF #

origin = numpy.array([0,0,0])

def pts_to_vec (pt_a, pt_b):
  start = numpy.asarray(pt_a)
  end = numpy.asarray(pt_b)
  vec = end - start
  return vec

thick = 6
width = 15
border = 3
innerD = 3.5
bolt = 3.5
t = .2
outerD = 2*(2*border+thick+innerD/2+2)
biggest = 400

spacer = 3

"""
hJoint takes in two booleans right and out and a name and creates
a joint. The joint is saved as an .stl named "heliodon/joint<name>.stl".
If right is True, the join goes on the right side of an arc. If right is
False, the joint goes on left side (as seen from above an arc placed in the
first quadrant). If outside is true, the joint attaches to another joint on
the outer side of the arc. If outside is false, the joint attaches to another
joint on the inner side.
"""
def hJoint (right, out, name):
  female = out

  # Create the outer cylinder
  j = solid.rotate(a = [-90, 0, 0])\
    (solid.cylinder(r=outerD/2, h=width, segments = 20))
  j = solid.translate(v = [0, 0, outerD/2])(j)

  # Create the clamp
  j = j + solid.cube([outerD,width,border])
  j = j + solid.translate([0, 0, border+thick])\
    (solid.cube([outerD,width,border]))
  j = j - solid.translate(v = [0, 0, border])(solid.cube([outerD,width,thick+2*t]))

  # Create the center hole
  c = solid.rotate(a = [90, 0, 0])\
    (solid.cylinder(r=innerD/2,center=True, h=2*width, segments=20))
  if female:
    if (right and out) or (not right and not out):
      off = -(width-6)
    else:
      off = width-6
    c = solid.translate(v = [0, width/2+off, outerD/2])(c)
  else:
    c = solid.translate(v = [0, width/2, outerD/2])(c)
  j = solid.difference()(j, c)

  if not female:
    if (right and out) or (not right and not out):
      off = -border
    else:
      off = border
    c = solid.rotate(a = [90, 0, 0])\
      (solid.cylinder(r=(outerD)/2-border,center=True, h=width, segments = 20))
    c = solid.translate(v = [0, width/2+off, outerD/2])(c)
    cube = solid.cube([outerD, width, 2*border+thick])
    c = solid.difference()(c, \
      solid.translate(v = [-outerD/2.0, 0, 0])(cube))
    j = solid.difference()(j, c)

  # Create bolt holes
  j = solid.difference()(j, 
    solid.translate(v=[.65*outerD, width/2, 0])
      (solid.cylinder(r=bolt/2, h = outerD, segments = 20)))
  j = solid.difference()(j, 
    solid.translate(v=[.85*outerD, width/2, 0])
      (solid.cylinder(r=bolt/2, h = outerD, segments = 20)))

  # Support bar
  # j = j + solid.translate(v = [-thick,0,border])(solid.cube([thick, width, thick+2*t]))

  # Move and rotate
  j = solid.translate(v=[0, 0, -border])(j)
  if right:
    j = solid.translate(v=[width, 0, 0])(solid.rotate(a=[0, 0, 90])(j))
  j = PolyMesh(generator=j)
  j.save("heliodon/joint" + name + ".stl")
  return j

"""
Arc creates an arc with the given radius and saves that arc as
"heliodon/arc<radius>.dxf" for laser cutting. The arc function
uses the global variables width and thick to determin the arc's
width and thickness respectively. The function also cuts holes
in the arc for securing it to the joints and for securing to
laser cut arcs together to increase stiffness.
"""
def arc(radius):
  a = solid.difference()(
    solid.cylinder(r=radius, h=thick, segments=48), solid.cylinder(r=radius-width, h=thick, segments=48))
  a = solid.intersection()(a, solid.cube([radius, radius, thick]))

  a = solid.difference()(a, 
    solid.translate(v=[.75*outerD, radius-width/2, 0])
      (solid.cylinder(r=bolt/2, h=2*thick, segments=20, center=True)))
  a = solid.difference()(a, 
    solid.translate(v=[radius-width/2, .75*outerD, width/2.0])
      (solid.cylinder(r=bolt/2, h=2*thick, segments=20, center=True)))
  c = solid.translate(v=[radius-width/2, 0, 0])\
    (solid.cylinder(r=bolt/2, h=2*thick, segments=20, center=True))

  # Add bolt holes for fastening the two sheets of acryllic together
  for step in range(1,3):
    a = solid.difference()(a, solid.rotate(a = [0,0, step * 30])(c))

  PolyLine(generator = solid.projection()(a)).save("heliodon/a" + str(radius) + ".dxf")
  return PolyMesh(generator=a)

"""
fullArc creates an arc and two joints and then combines them together.
radius determines the radius, outL determines 
"""
def fullArc(radius, outL, outR):
  jR = hJoint(True, outR, str(radius) + "R")
  jL = hJoint(False, outL, str(radius) + "L")
  a = arc(radius)

  jR *= translation_matrix([radius-width,0,0])
  jL *= translation_matrix([0,radius-width,0])
  a |= jR
  a |= jL
  a *= translation_matrix([0,0,border-outerD/2.0])
  return a

def spacerMaker(radius, right, out, spacer, name):
  s = solid.rotate(a = [-90, 0, 0])\
    (solid.cylinder(r=outerD/2, h=spacer, segments = 20))


  s1 = solid.rotate(a = [90, 0, 0])\
    (solid.cylinder(r=innerD/2, h=3*spacer, segments = 20, center=True))
  s = solid.difference()(s, s1)

  """s1 = solid.rotate(a = [90, 0, 0])\
    (solid.cylinder(r=innerD/2, h=2*border, segments = 20))
  s1 = solid.translate(v = [0, spacer+2*border, 0])(s1)
  s = s + s1"""

  if not out:
    s = solid.translate(v = [0, -spacer, 0])(s)
    off = radius - width
  else:
    off = radius
  s = solid.translate(v = [0, off, 0])(s)

  if right:
    s = solid.rotate(a = [0, 0, -90])(s)
  s = PolyMesh(generator=s)
  s.save("heliodon/spacer" + name +".stl")
  return s


def heliodon(modelSize):
  heliodon = fullArc(modelSize + 4*(width+spacer) + width, True, True)
  heliodon |= spacerMaker(modelSize + 4*(width+spacer) + width, \
    False, False, spacer+3*(width+spacer), "0")

  a1 = fullArc(modelSize + 3*(width+spacer) + width, False, True)
  a1 |= spacerMaker(modelSize + 3*(width+spacer) + width, \
    False, True, spacer, "1")
  a1 *= rotation_matrix(-numpy.pi/2, [0,0,1])
  heliodon |= a1

  a2 =  fullArc(modelSize + 2*(width+spacer) + width, False, True)
  a2 |= spacerMaker(modelSize + 2*(width+spacer) + width, \
    False, True, spacer, "2")
  a2 *= rotation_matrix(numpy.pi, [0,0,1])
  a2 *= rotation_matrix(numpy.pi/2, [0,1,0])
  heliodon |= a2

  a3 =  fullArc(modelSize + 1*(width+spacer) + width, True, False)
  a3 |= spacerMaker(modelSize + 1*(width+spacer) + width, \
    True, True, spacer, "3")
  a3 *= rotation_matrix(numpy.pi/2, [0,0,1])
  a3 *= rotation_matrix(numpy.pi/2, [1,0,0])
  heliodon |= a3

  a4 = fullArc(modelSize + 0*(width+spacer) + width, False, False)
  a4 |= spacerMaker(modelSize + 0*(width+spacer) + width, \
    False, True, spacer, "4")
  a4 *= rotation_matrix(numpy.pi/2, [0,0,1])
  heliodon |= a4
  return heliodon

heliodon = heliodon(400)
heliodon.show()

#hJoint(True, True).show()
"""heliodon = fullArc(400 + 4*(width+spacer) + width, True, True)
space = spacerMaker(400 + 4*(width+spacer) + width, False, True, spacer)
heliodon |= space
space = spacerMaker(400 + 4*(width+spacer) + width, True, True, spacer)
heliodon |= space
heliodon.show()"""

#PolyLine(generator = solid.projection()(a100.get_generator())).save("a100.dxf")