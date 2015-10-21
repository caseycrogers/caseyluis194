#!/usr/bin/python

from digifab import *
from solution_lab5 import * #importing the SynthFourBar class
import numpy
import solid

# EDITED - Luis #

# USEFULL THING #

def pts_to_vec (pt_a, pt_b):
  start = numpy.asarray(pt_a)
  end = numpy.asarray(pt_b)
  vec = end - start
  return vec

###################################

# IMPORTING MECHANISMS #
gripper_r_arm = SynthFourBar(B = 35+18.52j, D = 84.15 + 52.93j, P= (100+237.1j, 76.95+244.45j, 53+250j, 28.6+253.3j, 4+254.73j)) #the solution is gripper_r_arm.children[0]
gripper_arm = gripper_r_arm.children[0]

robot_leg = SynthFourBar(B= 0+80j, D= 0+20j, P= pattern(0.5, 10+0j)) #the solution is robot_leg.children[1]
robot_leg = robot_leg.children[1]

###################################


# AUXILIAR FUNCTION #
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

###################################


# GETTING JOINT COORDINATES AND MODIFIED BOUNDING BOX (always a square for simplification issues) CORNER COORDINATES #
def joints_bb_coord (mechanism):
	joints_coord=[]
	bb_coord=[]
	origin = numpy.array([0,0,0])
	
	ternary_body = filter_three_joints(mechanism)
	ternary_joints = ternary_body.joints
	for i in range(len(ternary_joints)):
		joints_coord.append(ternary_joints[i].pose[0])
	
	BBox = ternary_body.bounding_box()
	BBox_points= BBox.points
	BBox_point0 = numpy.append(BBox_points[0], [0]) #numpy append to add a z coord

	width = numpy.linalg.norm(pts_to_vec(BBox_points[0],BBox_points[2]))
	height = numpy.linalg.norm(pts_to_vec(BBox_points[0],BBox_points[1]))
	
	if width == height:
		bb_square = BBox
	elif width > height:
		bb_square = PolyLine(generator = solid.square(width)).simplified()
		tr_vec = translation_matrix(pts_to_vec(origin, BBox_point0))
		bb_square *= tr_vec
	else:
		bb_square = PolyLine(generator = solid.square(height)).simplified()
		tr_vec = translation_matrix(pts_to_vec(origin, BBox_point0))
		bb_square *= tr_vec

	bb_square_points = [numpy.append(bb_square.points[0], [0]), numpy.append(bb_square.points[2], [0])] #numpy append to add a z coord - consistency

	# For the sake of clarity transforming the arrays of bb_square_points to tuplles #
	# In this way the output of the function would be two lists of tupples #

	bb_pts_tpl = (map (tuple, bb_square_points))

	return joints_coord, bb_pts_tpl

###################################

# APPLYING THE JOINT COORD TO MECHANISMS#

bot_leg_joints_bb = joints_bb_coord(robot_leg)
gripper_joints_bb = joints_bb_coord(gripper_arm) 

###################################

# EDITED - Luis ###################


# EDITED - Casey #

# Transforming the coordinate system #

def dumb_coordinates(cList, dim, bound0, bound1):
 	ret = []
 	dim = dim + 1
 	for c in cList:
 		gX = numpy.floor( [(c[0]-bound0[0])/(bound1[1]-bound0[0])*dim] )[0]
 		gY = numpy.floor( [(c[1]-bound0[1])/(bound1[1]-bound0[1])*dim] )[0]
 		ret.append(dim*(gx + 1) + (dim-gY))
 	return ret

# EDITED - Casey ##################


if __name__ == '__main__':
  p = PolyLine(filename='ternary_link_020.png')
  p.show()
