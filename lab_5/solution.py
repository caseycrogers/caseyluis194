#!/usr/bin/python

from digifab import *
#from examples import disk_planar_body
import numpy

"""
Original Points:

B = -9.65+96.6j, D = -73.5-91.3j,
P = (-100+44j, -110+21j, -114-1.5j, -113-23j, -110-41j)

CALL:

### THIS IS COOL - number 1
def pattern(s, off):
  tpl=[(-50 - 0j) * s, (-5 - 0j)*s, (-12 + 10j)*s, (-25+15j)*s, (-40+10j)*s]
  for i in range(len(tpl)):
    tpl[i] += off
  return tpl

sfb = SynthFourBar(B= 0+80j, D= 0+20j, P= pattern(0.5, 10+0j))
sfb.show()
###

### THIS IS NOT COOL YET - number 2
def pattern(s, off):
  tpl=[(-75 - 0j) * s, (-5 - 0j)*s, (-15 + 10j)*s, (-45+20j)*s, (-60+10j)*s]
  for i in range(len(tpl)):
    tpl[i] += off
  return tpl

sfb = SynthFourBar(B= 0+80j, D= 0+40j, P= pattern(0.5, 10+0j))
sfb.show()
###

### USEFUL STUFF -  getting the origin to subtract the holes ###
### Luis will do this

sfb.children[1][i].joints[j].pose[j]

"""
"""
def pattern(s, off):
  tpl=[(-100 - 0j) * s, (0 - 0j)*s, (-25 + 10j)*s, (-50+15j)*s, (-80+10j)*s ]
  for i in range(len(tpl)):
    tpl[i] += off
  return tpl
"""

class SynthFourBar(Mechanism):
  def __init__(self, B = -9.65+96.6j, D = -73.5-91.3j,
    P = (-100+44j, -110+21j, -114-1.5j, -113-23j, -110-41j), signs=(1,1,1,1,1),
    origins=None, **kwargs):
    
    """Show all solutions of a synthesis problem showing output points.
    
    Args:
      B,D,P : synthesis arguments, see fourbar_synthesis.py
      origins: list of positions to put generated mechanisms at. By default
        will be spaced apart to not overlap
    """

    if 'name' not in kwargs.keys():
      kwargs['name'] = 'synth_four_bar'


    if 'children' not in kwargs.keys():
      # Get synthesis solutions, and remove those that don't have A/Ac and C/Cc
      # as complex conjugates
      solns = filter(is_consistent, synthesis(B, D, P, signs))
      
      # Remove 2R solutions
      solns = [s for s in solns if abs(s[0]-B) > 0.01]

      if not len(solns):
        raise Exception('No consistent solution found for synthesis')
      
      children = []
      constraints = []
      child_offset = 0.0
      soln_count = 0
      origins = []

      for A,_,C,_ in solns:
        # Create an elbow up and elbow down mechanism for each synthesis solution
        vectors = [B-A,D-B,(C-D,P[0]-D),A-C]
        
        up_child = FourBar(
          vectors=vectors, elbow=0, name='soln_%d_up' % soln_count,
        )

        down_child = up_child.clone(
          elbow=1, name='soln_%d_down' % soln_count,
        )
        
        # space children out by twice the maximum link length to guarantee no
        # overlapping
        offset = 2 * max(up_child.lengths)
        up_pos = (child_offset + A.real, A.imag, 0.0)
        down_pos = (child_offset + A.real, offset + A.imag, 0.0)

        up_child.constraints = [('body',(0,0,0),(up_pos, ORIGIN_POSE[1]))]
        down_child.constraints = [('body',(0,0,0),(down_pos, ORIGIN_POSE[1]))]

        origins.extend([(child_offset, 0.0),(child_offset,offset)])

        children.extend([up_child,down_child])
        
        constraints.extend([
          ('body', (up_child.name,0,0), (up_pos,ORIGIN_POSE[1])),
          ('body', (down_child.name,0,0), (down_pos,ORIGIN_POSE[1]))
        ])
        
        soln_count += 1
        child_offset += offset
      
      kwargs['children'] = children
      kwargs['constraints'] = constraints
    
    if type(B) is complex:
      self.B = (B.real, B.imag)
    else:
      self.B = B

    if type(D) is complex:
      self.D = (D.real, D.imag)
    else:
      self.D = D

    if type(P[0]) is complex:
      self.P = [(p.real,p.imag) for p in P]
    else:
      self.P = P
    
    self.origins = origins
    self.signs = signs

    super(SynthFourBar, self).__init__(**kwargs)
    
  def plot(self, plotter, **kwargs):
    x,y = zip(*self.P)
    x,y = numpy.array(x), numpy.array(y)
    for x_o, y_o in self.origins:
      plotter.ax.plot(x+x_o,y+y_o,'k*')

    super(SynthFourBar, self).plot(plotter, **kwargs)

  def synth_angle(self, synth_idx, child_idx):
    """Given a synthesis point index, return the angle that should be between
      body 0 and body 1

    Args:
      synth_idx (int): index into P from synthesis problem
      child_idx (int): which of self.children to get angle for
    """
    
    P = [complex(*pi) for pi in self.P]
    S,T = inv_kin_2R(complex(*self.B), complex(*self.D), P[0], P[synth_idx])[self.signs[synth_idx]]
    return self.children[child_idx].init_angle + numpy.angle(S)

  def show(self, state=None, **kwargs):
    """Show collection of synthesized mechanisms
    
    Args:
      state (int|float): if int, use synth_angle to assign mechanism to pose
        that reaches output point P[state]. If float, assign all children
        mechanism 
    """

    if type(state) is int:
      for i in range(len(self.children)):
        self.children[i].state[0] = self.synth_angle(state,i)

    elif type(state) is float:
      for child in self.children:
        child.state[0] = state
    
    super(SynthFourBar, self).show(**kwargs)

"""
#ThIS IS UP AT THE BEGINNING#
def pattern(s, off):
  tpl=[(-50 - 0j) * s, (-5 - 0j)*s, (-12 + 10j)*s, (-25+15j)*s, (-40+10j)*s]
  for i in range(len(tpl)):
    tpl[i] += off
  return tpl

#THIS IS THE CLASS CALL#
sfb = SynthFourBar(B= 0+80j, D= 0+20j, P= pattern(0.5, 10+0j))
#sfb.show()
"""


"""
def gen_laser_cuts(mechanism):
  vec_list = [] # creating a list of vectors for translating a cylinder placed in the origin
  poly_meshes = [] # a list for the polymeshes with the holes
  pls_laser_cut = [] # a list for the polylines

  #1st iteration on mechanism - build translation vectors from joints
  for body in mechanism.elts:
    vec_body=[] #per body builds a list
    for i in range(len(body.joints)):
      pose_origin = body.joints[i].pose[0] # getting the origin of each joint
      vec_body.append(pts_to_vec([0,0,0], pose_origin))# calculating the vector between the origin and each joint, store in vec_body
    vec_list.append(vec_body) #append each vec_body in vec_list

  #2nd iteration on mechanism - subtracting for joints
  for i in range(len(vec_list)):
    for j in range(len(vec_list[i])):
      tf_sub_cyl = sub_cyl.clone()
      tf_sub_cyl *= translation_matrix(vec_list[i][j])
      mechanism.elts[i][0][0] = mechanism.elts[i][0][0] - tf_sub_cyl
    poly_meshes.append(mechanism.elts[i][0][0])

  """
  """
  Previous version - save a dxf per arm
  i = 0
  for pm in poly_meshes:
    pl= PolyLine(generator = solid.projection()(pm.get_generator()))
    name= '%d.dxf'%(i)
    pl.save(name)
    i += 1
  """
  """

  for pm in poly_meshes:
    pls_laser_cut.append(PolyLine(generator = solid.projection()(pm.get_generator())))
  

  a_block = Block([Layer(name = 'A_arm', color = 'red')])
  b_block = Block([Layer(name = 'B_arm', color = 'red')])
  c_block = Block([Layer(name = 'C_arm', color = 'red')])
  d_block = Block([Layer(name = 'D_arm', color = 'red')])

  a_block['A_arm'] += pls_laser_cut[0]
  b_block['B_arm'] += pls_laser_cut[1]
  c_block['C_arm'] += pls_laser_cut[2]
  d_block['D_arm'] += pls_laser_cut[3]

  a_layout = Layout([a_block, b_block, c_block, d_block], size= (600,600)) 

  #return poly_meshes #previous version save a dxf per arm
  return a_layout.solved()

gen_laser_cuts(p)[0].save('laser_cut.dxf')
"""

