from random import seed as random_seed,random as rand, randint as iRand
from math import *
from Vec2 import *
from FileIO import *
import pickle
from VoroMan import *
from sys import getrecursionlimit,setrecursionlimit
from SFMLGraphics import *
from SFPoly import *

seed=3519714916446274305
randomishness=0.875
grid=6
WindowSize = 512
TOOSMALL=16

def randomGrid_square(grid,scale=1.0,randomishness=1.0):
	step=scale/grid
	centroids=[]
	for i in range(grid):
		for j in range(grid):
			p=Vec2(i,j)*step + Vec2(rand(),rand())*step*randomishness
			centroids.append(p)
	return centroids

def initFrag(poly,pMin,pScale):
	fpFrag='./frag.glsl'
	points = poly.verts
	others = poly.others
	N=len(points)
	txt='#version 120\n'
	txt+='#define N %i\n'%N
	txt+='vec2 P[N] = vec2[](%s);\n'%( ', '.join(['vec2(%f,%f)'%(x,y) for x,y in points ]) )
	txt+='bool O[N] = bool[](%s);\n'%( ','.join(['true' if o else 'false' for o in others]) )
	txt+= fileRead('__frag__.glsl')
	fileWrite(fpFrag,txt)
	return fpFrag

def createVoroMan( boundingBox, grid, randomishness=1.0, seed=None ):
	pMin,pMax=boundingBox;size=Vec2(pMax)-Vec2(pMin)
	if seed: save=True
	else:
		seed = iRand(0, maxint )
		print 'seed:',seed
		save=False
	random_seed(seed)
	centroids=randomGrid_square(grid, WindowSize ,randomishness)
	tooSmall = size.x/grid/TOOSMALL
	print 'tooSmall:',tooSmall
	polies = VoroMan( centroids, boundingBox, tooSmall ) # bounding box not really implemented yet. Only size is used.
	fp= "%i_%i.pickle"%(grid,seed)
	if save: pickle.dump( polies, open( fp, "wb" ) )
	return polies

def loadVoroMan(grid,seed):
	fp= "%i_%i.pickle"%(grid,seed)
	if exists(fp):
		return pickle.load( open( fp, "rb" ) )

def CreatePolies():
	setrecursionlimit(10000)

	#shader = sf.Shader.from_file(None, '../data/db2.frag' )
	#states = sf.RenderStates(shader=shader)


	pMin=-WindowSize,-WindowSize
	pMax= WindowSize, WindowSize
	boundingBox=pMin,pMax
	polies= loadVoroMan(grid,seed) if seed else None
	if not polies:
		polies= createVoroMan(boundingBox, grid, randomishness, seed)

	pMin,pMax=Vec2(boundingBox[0]),Vec2(boundingBox[1]);pScale=pMax-pMin
	polies=[SFPoly(poly, pMin,pScale) for poly in polies]
	for p in polies: p.interlink(polies)

	return polies

