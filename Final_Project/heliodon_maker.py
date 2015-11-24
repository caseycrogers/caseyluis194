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

thick = 3
width = 15
border = 3
innerD = 3.5
bolt = 3.5
t = .2
outerD = 2*(border+thick+innerD/2+2)
biggest = 400

spacer = 10

def hJoint (right, out):

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
    (solid.cylinder(r=innerD/2,center=True, h=width, segments = 20))
  c = solid.translate(v = [0, width/2, outerD/2])(c)
  j = solid.difference()(j, c)

  if (right and out) or (not right and not out):
    off = -border
  else:
    off = border
  c = solid.rotate(a = [90, 0, 0])\
    (solid.cylinder(r=(outerD)/2-border,center=True, h=width, segments = 20))
  c = solid.translate(v = [0, width/2+off, outerD/2])(c)
  j = solid.difference()(j, c)

  j = solid.difference()(j, 
    solid.translate(v=[.75*outerD, width/2, 0])
      (solid.cylinder(r=bolt/2, h = outerD, segments = 20)))

  j = solid.translate(v=[0, 0, -border])(j)
  if right:
    j = solid.translate(v=[width, 0, 0])(solid.rotate(a=[0, 0, 90])(j))
  return PolyMesh(generator=j)

def arc(radius):
  a = solid.difference()(
    solid.cylinder(r=radius, h=thick), solid.cylinder(r=radius-width, h=thick))
  a = solid.intersection()(a, solid.cube([radius, radius, thick]))

  a = solid.difference()(a, 
    solid.translate(v=[.75*outerD, 90+width/2, 0])
      (solid.cylinder(r=bolt/2, h = outerD, segments = 20)))
  a = solid.difference()(a, 
    solid.translate(v=[90+width/2, .75*outerD, 0])
      (solid.cylinder(r=bolt/2, h = outerD, segments = 20)))

  return PolyMesh(generator=a)

def fullArc(radius, outL, outR):
  jR = hJoint(True, outR)
  jL = hJoint(False, outL)
  a = arc(radius)

  jR *= translation_matrix([radius-width,0,0])
  jL *= translation_matrix([0,radius-width,0])
  a |= jR
  a |= jL
  a *= translation_matrix([0,0,border-outerD/2.0])
  return a

def spacerMaker(radius, right, out, spacer):
  s = solid.rotate(a = [-90, 0, 0])\
    (solid.cylinder(r=outerD/2, h=spacer, segments = 20))


  s1 = solid.rotate(a = [90, 0, 0])\
    (solid.cylinder(r=innerD/2, h=2*border, segments = 20))
  s = s + s1

  s1 = solid.rotate(a = [90, 0, 0])\
    (solid.cylinder(r=innerD/2, h=2*border, segments = 20))
  s1 = solid.translate(v = [0, spacer+2*border, 0])(s1)
  s = s + s1

  if not out:
    s = solid.translate(v = [0, -spacer, 0])(s)
    off = radius - width
  else:
    off = radius
  s = solid.translate(v = [0, off, 0])(s)

  if right:
    s = solid.rotate(a = [0, 0, -90])(s)
  return PolyMesh(generator=s)


def heliodon(modelSize):
  heliodon = fullArc(modelSize + 4*(width+spacer) + width, True, True)
  heliodon |= spacerMaker(modelSize + 4*(width+spacer) + width, \
    False, False, spacer+3*(width+spacer))

  a1 = fullArc(modelSize + 3*(width+spacer) + width, False, True)
  a1 |= spacerMaker(modelSize + 3*(width+spacer) + width, \
    False, True, spacer)
  a1 *= rotation_matrix(-numpy.pi/2, [0,0,1])
  heliodon |= a1

  a2 =  fullArc(modelSize + 2*(width+spacer) + width, False, True)
  a2 |= spacerMaker(modelSize + 2*(width+spacer) + width, \
    False, True, spacer)
  a2 *= rotation_matrix(numpy.pi, [0,0,1])
  a2 *= rotation_matrix(numpy.pi/2, [0,1,0])
  heliodon |= a2

  a3 =  fullArc(modelSize + 1*(width+spacer) + width, True, False)
  a3 |= spacerMaker(modelSize + 1*(width+spacer) + width, \
    True, True, spacer)
  a3 *= rotation_matrix(numpy.pi/2, [0,0,1])
  a3 *= rotation_matrix(numpy.pi/2, [1,0,0])
  heliodon |= a3

  a4 = fullArc(modelSize + 0*(width+spacer) + width, False, False)
  a4 |= spacerMaker(modelSize + 0*(width+spacer) + width, \
    False, True, spacer)
  a4 *= rotation_matrix(numpy.pi/2, [0,0,1])
  heliodon |= a4
  return heliodon

heliodon = heliodon(400)
heliodon.show()
"""heliodon = fullArc(400 + 4*(width+spacer) + width, True, True)
space = spacerMaker(400 + 4*(width+spacer) + width, False, True, spacer)
heliodon |= space
space = spacerMaker(400 + 4*(width+spacer) + width, True, True, spacer)
heliodon |= space
heliodon.show()"""

#PolyLine(generator = solid.projection()(a100.get_generator())).save("a100.dxf")