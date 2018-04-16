#!/usr/bin/evn python
# -*- coding: utf-8 -*-
"""Simple converter of lpy files to ply format."""

import os
import sys

from openalea.lpy import Lsystem
from openalea.plantgl.all import Tesselator

usage = """Convert lpy file to ply format
  usage: {} FILE"""
if len(sys.argv) != 2:
    print(usage.format(__name__))

lpy_file = sys.argv[1]
lsys = Lsystem(lpy_file)
ply_file = os.path.splitext(
    os.path.basename(os.path.expanduser(lpy_file)))[0]
ply_file = ply_file + '.ply'

n = lsys.derivationLength
tree = lsys.axiom
for i in range(n):
    # Apply rewritting rules on the tree -> One step of simulation
    tree = lsys.iterate(tree, 1)
    scene = lsys.sceneInterpretation(tree)

d = Tesselator()
nind = 0
nvert = 0
vert_part = ''
ind_part = ''
for shapes in scene.todict().values():
    for shape in shapes:
        d.process(shape)
        c = shape.appearance.ambient
        for p in d.result.pointList:
            vert_part += "%f %f %f %i %i %i\n" % \
                  (p.x, p.y, p.z, c.red, c.green, c.blue)
        for i3 in d.result.indexList:
            ind_part += "3 %i %i %i\n" % \
                  (i3[0] + nvert, i3[1] + nvert, i3[2] + nvert)
        nind += len(d.result.indexList)
        nvert += len(d.result.pointList)

header = """ply
format ascii 1.0
comment author Xarthisius
comment File Generated with PlantGL API
element vertex {nvert}
property float x
property float y
property float z
property uchar diffuse_red
property uchar diffuse_green
property uchar diffuse_blue
element face {nind}
property list uchar int vertex_indices
end_header
"""

with open(ply_file, 'w') as fp:
    fp.write(header.format(nvert=nvert, nind=nind))
    fp.write(vert_part)
    fp.write(ind_part)
print('Saved data to ' + ply_file)
