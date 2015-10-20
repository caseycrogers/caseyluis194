#!/usr/bin/python

from digifab import *
#from solution_lab5 import * #importing the SynthFourBar
import numpy
import solid

# EDITED - Luis #
# USEFULL THING #

def pts_to_vec (pt_a, pt_b):
  start = numpy.asarray(pt_a)
  end = numpy.asarray(pt_b)
  vec = end - start
  return vec

################
"""
# Importing a mechanism
gripper_r_arm = SynthFourBar(B = 35+18.52j, D = 84.15 + 52.93j, P= (100+237.1j, 76.95+244.45j, 53+250j, 28.6+253.3j, 4+254.73j)) #the solution is gripper_r_arm.children[0]
gripper_arm = gripper


robot_leg = SynthFourBar(B= 0+80j, D= 0+20j, P= pattern(0.5, 10+0j)) #the solution is robot_leg.children[1]
robot_leg = robot_leg.children[1]"""


# Test

# Selecting the ternary link #
# Making a filter function #
# Test: which body has 3 joints? #

def filter_three_joints (a_mechanism):
	for body in a_mechanism:
		if len(body.joints) == 3:
			ternary_link = body
		else:
			pass
	return ternary_link

"""
def joint_coord (mechanism):
	joints_coord=[]
	bb_coord=[]
	
	ternary_body = filter_three_joints(mechanism)
	ternary_joints = ternary_body.joints
	for i in range(len(ternary_joints)):
		joints_coord.append(ternary_joints[i].pose[0])
	
	BBox_points= mechanism.boundingBox().points
	width= numpy.linalg.norm(pts_to_vec(BBox_points[0],BBox_points[3]))
	height= numpy.linalg.norm(pts_to_vec(BBox_points[0],BBox_points[1]))
	
	if width == height:
		bb_coord.extend((BBox_points[0], BBox_points[2]))
	elif width > height:
		bb_square= Polyline(generator= solid.square(width)).simplified()
	else:
		pass

	#length= 

	return joints_coord, bb_coord
"""


# Applying the joint_coord function to robot_leg #

#bot_leg_joints= joint_coord(robot_leg)


def dumb_coordinates(cList, dim, bound0, bound1):
	ret = []
	dim = dim + 1
	for c in cList:
		gX = numpy.round( (c[0]-bound0[0])/(bound1[1]-bound0[0])*dim )
		gY = numpy.round( (c[1]-bound0[1])/(bound1[1]-bound0[1])*dim ) 
		print str(gX) + ", " + str(gY)
		ret.append((int) (dim*gX + (dim-gY)))
	return ret


if __name__ == '__main__':
	print dumb_coordinates([(6.0,6.0), (10.0,10.0)], 3, (0.0,0.0), (10.0,10.0))
	#p = PolyLine(filename='ternary_link_020.png')
	#p.show()
