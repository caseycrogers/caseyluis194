from digifab import *

class DiskPlanarBody(Body):
  def __init__(self, length=None, joint_points = None, vectors=None,
    disk_r = 5.5, disk_h = 2.0, disk_h_r = 7.0/2.0, **kwargs): #The previous radius was 5.0

    if 'elts' not in kwargs.keys():
      if joint_points is None:
        joint_points = []

      if length is not None:
        joint_points = [(0.0,0.0),(length,0.0)] + joint_points

      if vectors is not None:
        joint_points = [(0.0,0.0)] + [(v.real,v.imag) for v in vectors]

      if len(joint_points) > 1:
        j0,j1 = joint_points[:2]
        joint_angle = numpy.arctan2(j1[1]-j0[1],j1[0]-j0[1])
      else:
        joint_angle = 0.0

      joint_poses = [jpt + (joint_angle,) for jpt in joint_points]

      kwargs['joints'] = [
        Joint(pose = matrix_pose(pose_matrix(jp))) for jp in joint_poses
      ]

      '''
      disk = PolyLine(generator=solid.circle(disk_r))
      hole = PolyLine(generator=solid.circle(disk_r/5))

      holes = sum([jp * hole for jp in joint_poses],PolyLine())
      disks = sum([jp * disk for jp in joint_poses],PolyLine())
      outline = disks.hull()
      '''

      disk_gen = solid.circle(disk_r)
      #hole_gen = solid.circle(disk_r/5)
      hole_gen = solid.circle(disk_h_r, segments= 32)

      holes = solid.union()([solid.translate(jpt)(hole_gen) for jpt in joint_points])
      outline = solid.hull()([solid.translate(jpt)(disk_gen) for jpt in joint_poses])

      cut_layer = Layer(
        PolyLine(generator=outline) + PolyLine(generator=holes),
        name='cut', color='red'
      )

      '''
      extruded_outline = solid.linear_extrude(disk_h)(outline.get_generator())
      extruded_holes = [
        solid.translate([0.0,0.0,-1.0])(
          solid.linear_extrude(disk_h+2.0)(h.get_generator())
        ) for h in holes
      ]
      solid_gen = extruded_outline + solid.hole()(extruded_holes)

      print_layer = Layer(
        PolyMesh(generator=solid_gen), 
        name='print', color='white'
      )
      '''

      centroid = tuple(numpy.array(joint_points).mean(axis=0))
      label_layer = Layer(
        (centroid + (joint_angle,)) * PolyLine(generator=solid.text(kwargs['name'],disk_r)),
        name = 'label', color='black'
      )
        
      kwargs['elts'] = [cut_layer, label_layer]#, print_layer]

    super(DiskPlanarBody, self).__init__(**kwargs)
  
  def show(self, is_2d=True):
    if is_2d:
      self['cut'].show()
    else:
      self['print'].show(False)

