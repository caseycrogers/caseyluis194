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

def hJoint (thick, width, border, innerD, bolt, t, right):
  outerD = 2*(border+thick+innerD/2+2)
  j = solid.rotate(a = [90, 0, 0])\
    (solid.cylinder(r=outerD/2,center=True, h=width, segments = 20))
  j = solid.translate(v = [0, width/2, outerD/2])(j)
  j = j + solid.cube([outerD,width,border])
  j = j + solid.translate([0, 0, border+thick+2*t])\
    (solid.cube([outerD,width,border]))
  j = j - solid.translate(v = [0, 0, border])(solid.cube([outerD,width,thick+2*t]))

  c = solid.rotate(a = [90, 0, 0])\
    (solid.cylinder(r=innerD/2,center=True, h=width, segments = 20))
  c = solid.translate(v = [0, width/2, outerD/2])(c)
  j = solid.difference()(j, c)
  if right:
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
  return PolyMesh(generator=j)

def arc(thick, width, radius):
  a = solid.difference()(
    solid.cylinder(r=radius), solid.cylinder(r=radius-width))
  a = solid.intersection()(a, solid.cube([radius, radius, thick]))
  return PolyMesh(generator=a)

jR = hJoint(3, 10, 3, 3, 3.5, .2, True)
jL = hJoint(3, 10, 3, 3, 3.5, .2, False)
jR.save("rightjoint.stl")
jL.save("leftjoint.stl")
a100 = arc(3, 10, 100)
jR *= translation_matrix([90,0,0])
jL *= translation_matrix([0,90,0])
a100 |= jR
a100 |= jL
a100.show()