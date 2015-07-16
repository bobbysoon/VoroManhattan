#!/usr/bin/python

from random import seed as random_seed,random as rand, randint as iRand
from math import *
from Vec2 import *

from sys import getrecursionlimit,setrecursionlimit
setrecursionlimit(10000)

from SFMLGraphics import *

def randomGrid_square(grid,scale=1.0,randomishness=1.0):
	step=scale/grid
	centroids=[]
	for i in range(grid):
		for j in range(grid):
			p=Vec2(i,j)*step + Vec2(rand(),rand())*step
			centroids.append(p)
	return centroids


from FileIO import *
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


selectedPoly=None
def onLeftClick(p):
	global selectedPoly
	p=Vec2(tuple(p))
	da={poly.dist(p):poly for poly in polies}
	selectedPoly= da[sorted(da.keys())[0]]


import pickle
from VoroMan import *
def createVoroMan( boundingBox, grid, randomishness=1.0, seed=None ):
	if not seed:
		seed = iRand(0, maxint )
		print 'seed:',seed
	random_seed(seed)
	centroids=randomGrid_square(grid,WindowSize,randomishness)
	polies = VoroMan( centroids, boundingBox ) # bounding box not really implemented yet. Only size is used.
	fp= "%i_%i.pickle"%(grid,seed)
	pickle.dump( polies, open( fp, "wb" ) )
	return polies

def loadVoroMan(grid,seed):
	fp= "%i_%i.pickle"%(grid,seed)
	if exists(fp):
		return pickle.load( open( fp, "rb" ) )


#seed=4304736947893117592
seed=None
WindowSize = 512
pMin=-WindowSize,-WindowSize
pMax= WindowSize, WindowSize
boundingBox=pMin,pMax
randomishness=0.5
grid=7
polies= loadVoroMan(grid,seed) if seed else None
if not polies:
	polies= createVoroMan(boundingBox, grid, seed, randomishness)


class SFPoly(sf.Drawable,Poly):
	def __init__(self, poly, pMin,pScale):
		self.poly=poly
		poly.sfPoly=self
		self.initPolyGLFan(pMin,pScale)
	def interlink(self):
		global polies
		self.others=[b.other.sfPoly if b.other and hasattr(b.other,'sfPoly') else None for b in self.poly.borders]
		self.adjacentPolies=[b.other.sfPoly for b in self.poly.borders if b.other and hasattr(b.other,'sfPoly') and b.other.sfPoly in polies]
	def draw(self, target, states):
		#states.shader = self.shader
		target.draw(self.glFan, states)
	def initPolyGLFan(self,pMin,pScale):
		self.glFan=sf.VertexArray(sf.PrimitiveType.TRIANGLES_FAN, 2+len(self.poly.verts))
		self.glFan[0].position=self.poly.centroid
		self.glFan[0].tex_coords=self.poly.centroid
		self.glFan[0].color=BLACK
		for i in range(len(self.poly.verts)):
			self.glFan[1+i].position=self.poly.verts[i]
			self.glFan[1+i].tex_coords=self.poly.verts[i]
			self.glFan[1+i].color=WHITE
		self.glFan[1+len(self.poly.verts)].position=self.poly.verts[0]
		self.glFan[1+len(self.poly.verts)].tex_coords=self.poly.verts[0]
		self.glFan[1+len(self.poly.verts)].color=WHITE
		#self.shader = sf.Shader.from_file(None, initFrag(self.poly,pMin,pScale) )
		#self.states = sf.RenderStates(shader=)


pMin,pMax=Vec2(boundingBox[0]),Vec2(boundingBox[1]);pScale=pMax-pMin
polies=[SFPoly(poly, pMin,pScale) for poly in polies]
for p in polies: p.interlink()

shader = sf.Shader.from_file(None, '../data/db2.frag' )
states = sf.RenderStates(shader=shader)

g=Graphics(WindowSize=512, rate=30, debug=True)
g.onLeftClick=onLeftClick;
clock = sf.Clock() ; time=0.0
framerate=0.0 ; iFramerate=int(0)
fpsText = sf.Text()
ttf='/usr/share/games/extremetuxracer/fonts/PaperCuts_outline.ttf'
#ttf='/usr/share/fonts/truetype/freefont/FreeMonoBoldOblique.ttf'
fpsText.font = sf.Font.from_file(ttf)
fpsText.position = (8,8)
fpsText.character_size = 36

def drawFramerate():
	framerate= .9*framerate+(1/tDelta*.1)
	i=int(framerate)
	if i!=iFramerate:
		iFramerate=i
		fpsText.string = str(i)

	view=g.window.view
	g.window.view = g.window.default_view
	g.window.push_GL_states() # protects poly shaders from text
	g.window.draw(fpsText)
	g.window.pop_GL_states()
	g.window.view=view


def loopStep(polies):
	global tDelta,time
	tDelta= clock.restart().seconds ; time+= tDelta

	g.pollEvents()
	g.clear()

	for poly in polies:
		g.draw(poly)

	g.display()

#while g.window.is_open: loopStep(polies)


def PolyPath(cell,cells,others):
	global polies
	paths={}
	for n in others[cell]:			#	for each neighbor,
		if not [None for nn in others[n] if not nn in cells]:
			nCells= [c for c in cells if c!=cell]
			path = PolyPath(n,nCells,others)
			paths[len(path)]=path

	path = [cell]
	if paths: path.extend(paths[sorted(paths.keys())[-1]])

	pathPolies = [polies[i] for i in range(len(polies)) if i in path]

	if len(path)>3: loopStep( pathPolies )

	return path


others=[[polies.index(n) for n in p.adjacentPolies if n in polies] for p in polies]
cells= range(len(polies))
outerCells = [polies.index(p) for p in polies if None in p.others]
paths = [PolyPath(cell,cells,others) for cell in outerCells]
paths = { len(path):path for path in paths }
path = paths[sorted(paths.keys())[-1]]

polies= [polies[i] for i in path]

while g.window.is_open: loopStep(polies)
