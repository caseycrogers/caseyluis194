#!/usr/bin/python

from digifab import *
from solution_lab5 import * #importing the SynthFourBar

# EDITED - Luis #
# Importing a mechanism
gripper_r_arm = SynthFourBar(B = 35+18.52j, D = 84.15 + 52.93j, P= (100+237.1j, 76.95+244.45j, 53+250j, 28.6+253.3j, 4+254.73j)) #the solution is gripper_r_arm.children[0]
robot_leg = SynthFourBar(B= 0+80j, D= 0+20j, P= pattern(0.5, 10+0j)) #the solution is robot_leg.children[1]
robot_leg = robot_leg.children[1]
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

def joint_coord (mechanism):
	joints_coord=[]
	ternary_body = filter_three_joints(mechanism)
	ternary_joints = ternary_body.joints
	for i in range(len(ternary_joints)):
		joints_coord.append(ternary_joints[i].pose[0])
	return joints_coord



if __name__ == '__main__':
  p = PolyLine(filename='ternary_link_020.png')
  p.show()
