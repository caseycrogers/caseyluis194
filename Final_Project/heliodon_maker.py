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
  j = j + solid.translate([0, 0, border+thick])\
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
  if right:
    j = solid.translate(v=[width, 0, 0])(solid.rotate(a=[0, 0, 90])(j))
  return (PolyMesh(generator=j), outerD)

def arc(thick, width, radius, outerD, bolt):
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

jR, outerD = hJoint(3, 10, 3, 3, 3.5, .2, True)
jL, outerD = hJoint(3, 10, 3, 3, 3.5, .2, False)
jR.save("rightjoint.stl")
jL.save("leftjoint.stl")
a100 = arc(3, 10, 100, outerD, 3.5)

PolyLine(generator = solid.projection()(a100.get_generator())).save("a100.dxf")

jR *= translation_matrix([90,0,0])
jL *= translation_matrix([0,90,0])
a100 |= jR
a100 |= jL
a100.show()