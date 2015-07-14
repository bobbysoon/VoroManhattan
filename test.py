#!/usr/bin/python

from random import seed as random_seed,random as rand, randint as iRand
from math import *
from Vec2 import *

WindowSize = 512
from SFMLGraphics import *

N=32
seed=3157704460901888162
#seed = iRand(0, maxint );print 'seed:',seed
#random_seed(seed)
#centroids = [(Vec2(rand(),rand())*6./8.+1./8.)*WindowSize for i in range(N)]

import numpy as np
np.random.seed(seed)
centroids = [ Vec2(p[0],p[1]) for p in np.random.uniform(low=0.0, high=WindowSize, size=(N,2) ) ]

from VoroMan import *
pMin=-WindowSize,-WindowSize
pMax= WindowSize, WindowSize
boundingBox=pMin,pMax


from FileIO import *

def initFrag(P,pMin,pScale):
	fpFrag='./frag.glsl'
	points = P
	#points = [p*2.0/pScale for p in P]
	points = ', '.join(['vec2(%f,%f)'%(x,y) for x,y in points ])
	txt='#version 120\n#define N %i\nvec2 P[N] = vec2[](%s);\n'%( len(P) , points )
	txt+= fileRead('__frag__.glsl')
	fileWrite(fpFrag,txt)
	return fpFrag



selectedPoly=None
def onLeftClick(p):
	global selectedPoly
	p=Vec2(tuple(p))
	da={poly.dist(p):poly for poly in polies}
	selectedPoly= da[sorted(da.keys())[0]]

def initPolyGLFan(pol,pMin,pScale):
	pol.glFan=sf.VertexArray(sf.PrimitiveType.TRIANGLES_FAN, 2+len(pol.verts))
	pol.glFan[0].position=pol.centroid
	pol.glFan[0].tex_coords=pol.centroid
	pol.glFan[0].color=BLACK
	for i in range(len(pol.verts)):
		pol.glFan[1+i].position=pol.verts[i]
		pol.glFan[1+i].tex_coords=pol.verts[i]
		pol.glFan[1+i].color=WHITE
	pol.glFan[1+len(pol.verts)].position=pol.verts[0]
	pol.glFan[1+len(pol.verts)].tex_coords=pol.verts[0]
	pol.glFan[1+len(pol.verts)].color=WHITE
	pol.states = sf.RenderStates(shader=sf.Shader.from_file(None, initFrag(pol.verts,pMin,pScale) ))

polies = VoroMan( centroids, boundingBox ) # bounding box not really implemented yet. Only size is used.
pMin,pMax=Vec2(boundingBox[0]),Vec2(boundingBox[1])
pScale=pMax-pMin
for pol in polies: initPolyGLFan(pol,pMin,pScale)

shader = sf.Shader.from_file(None, '../data/db2.frag' )
states = sf.RenderStates(shader=shader)

g=Graphics(WindowSize=512, rate=30, debug=True)
g.onLeftClick=onLeftClick;
clock = sf.Clock() ; time=0.0
while g.window.is_open:
	tDelta = clock.restart().seconds
	time+= tDelta
	hueTime=time/4.0

	g.pollEvents()
	g.clear()

	for poly in polies:
		if poly!=selectedPoly and (poly.isClosed or not g.hideStuff):
			g.draw(poly.glFan,poly.states)

	if selectedPoly:
		g.draw(selectedPoly.glFan,selectedPoly.states)

	g.setColor(DGREY)
	for poly in polies:
		if poly!=selectedPoly and (poly.isClosed or not g.hideStuff):
			g.drawCircle(poly.centroid)
	if selectedPoly:
		g.setColor(WHITE)
		g.drawCircle(selectedPoly.centroid)

	g.display()

