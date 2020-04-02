from debug import debug
import yaml
import numpy as np
import mounttree as mnt
import re as reg

# data=yaml.load(open('/project/meteo/work/Paul.Ockenfuss/Software/runmacs/test/test_geometry/testmounttree.yaml'))
# tree=data['mounttree']
coordinate_lib={'WGS-84':lambda variables: mnt.OblateEllipsoidFrame(6378137.0, 6356752.314245,variables), 'GRS-80':lambda variables: mnt.OblateEllipsoidFrame(6378137.0,  6356752.314140,variables)}
variables={'lat':1, 'lon':1, 'height':2, 'yaw':0, 'pitch':0, 'roll':90}
def load_mounttree(filename):
    tree=yaml.load(open(filename))
    name=tree['description']['name']
    tree=tree['mounttree']
    root_frame=create_from_yaml(tree, variables)
    universe=mnt.CoordinateUniverse(name, root_frame, variables)
    mytransform=universe.get_transformation('VNIR', 'SWIR')
    print(mytransform)

def create_from_yaml(mounttree, variables):
    try:
        rhs=coordinate_lib[mounttree['framespec']](variables)
    except KeyError:
        rhs=mnt.CartesianCoordinateFrame(variables)
    rhs.name=mounttree['framename']
    if 'position' in mounttree:
        rhs.pos=mounttree['position']
    if 'rotation' in mounttree:
        rot_input=mounttree['rotation']
        if isinstance(rot_input, list):
            assert(len(rot_input)==3)
            rhs.euler=rot_input
        if isinstance(rot_input, str):
            rhs.rotation=convert_rot_string(rot_input)
    if 'subframes' in mounttree:
        for subframe in mounttree['subframes']:
            rhs.add_child(create_from_yaml(subframe, variables))
    return rhs

def convert_rot_string(rot_string):
    reRotPrimitive = reg.compile('^R([xyz])\\((-?[0-9]+(?:\\.[0-9]*)?)((?:deg|rad)?)\\)$')
    rsplit=rot_string.split("*")
    rot=mnt.Rotation.Identity()
    for s in rsplit:
        m=reRotPrimitive.match(s)
        assert(m is not None)
        axis, angle, unit=m.groups()
        angle=float(angle)
        if unit=='deg':
            angle=mnt.deg2rad(angle)
        rot=mnt.Rotation.fromAngle(angle, axis)*rot
    return rot
     

    

# load_mounttree('/project/meteo/work/Paul.Ockenfuss/Software/runmacs/test/test_geometry/testmounttree.yaml')
load_mounttree('/project/meteo/work/Paul.Ockenfuss/Software/mounttree_py/eurec4a_pretest_mounttree.yaml')
