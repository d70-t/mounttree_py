# Python package for coordinate conversions
This package allows to convert position and direction vectors between different coordinate frames.
These frames must be arranged in a so called "mounttree", a tree-like structure which defines their relative orientation.

# Usage
Load a mounttree in yaml format to get a CoordinateUniverse object
```python
import mounttree as mnt
universe=mnt.load_mounttree('test/testmounttree.yaml')
```
Each sub-coordinate frame in the tree needs a position and rotation relative to the parent.
Both can be three floating point numbers or three strings.
In the latter case, the strings must be associated to numbers with the "update()" method before they can be used for transformations.
Rotations are assumed to be Euler angles. Alternatively, a single string of a form similar to `Ry(-85deg)*Rz(-90deg)` can be provided at initialization, defining the rotation as a product of rotation matrices.
```python
universe.update(lat=0, lon=0, height=10,roll=0, pitch=0, yaw=0)
```

Now, we can get a transformation from 'HALO' to 'EARTH' coordinates
```python
transform=self.universe.get_transformation('HALO','EARTH')
```
Use the transformation to convert positional or direction vectors
```python
p1=transform.apply_point(0,0,0)
p2=transform.apply_direction(0,1,0)
```
We can also convert multiple points at once, if we provide numpy arrays of coordinates.
```python
import numpy as np
x=np.array([[0,0,0],[0,1,1]])
y=np.array([[0,1,1],[0,0,0]])
z=np.array([[0,0,0],[1,1,1]])
px, py, pz=transform.apply_point(x,y,z)
```