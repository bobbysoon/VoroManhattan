#!/usr/bin/python

from SF import *
from math import *
from FileIO import *

def initFrag(P):
	fpFrag='./frag.glsl'
	#return fpFrag
	points = ', '.join(['vec2(%f,%f)'%(x,y) for x,y in P])
	txt='#version 120\n#define N %i\nvec2 P[N] = vec2[](%s);\n'%( len(P) , points )
	txt+= fileRead('__frag__.glsl')
	fileWrite(fpFrag,txt)
	return fpFrag

class Quad(sf.VertexArray):
	def __init__(self):
		sf.VertexArray.__init__(self, sf.PrimitiveType.QUADS,4)
		for i in [0,1,2,3]: self[i].color=sf.Color.BLUE

	def align(self, target):
		sw,sh= target.size
		pa = [(0,0),(sw,0),(sw,sh),(0,sh)]
	#	pa = [(0,sh/2),(sw/2,0),(sw,sh/2),(sw/2,sh)]
		for i in [0,1,2,3]:
			p=	target.map_pixel_to_coords(pa[i])
			self[i].position= p
			self[i].tex_coords= p

from random import randint,random
def rnd(): return randint(0,255)
def createNoisemap(size):
	image = sf.Image.create(size,size)
	for i in range(size):
		for j in range(size):
			image[i,j]=sf.Color(rnd(),rnd(),rnd(),255)
	texture= sf.Texture.from_image(image)
	texture.repeated=True
	texture.smooth=True
	return texture

window = sf.RenderWindow(sf.VideoMode(800,600), "pysfml")
window.view.center=0,0 ; ww,wh=window.size ; scale=1000
window.view.size= scale,scale*wh/ww

def RP(): return random(),random()
N=16
points=[RP() for n in range(N)]
quad=Quad()
shader = sf.Shader.from_file(None, initFrag(points) )
#texture=createNoisemap(256)
#shader.set_parameter('texture', texture )
states = sf.RenderStates(shader=shader)
panFrom=None
def handleEvents():
	global scale,panFrom
	for event in window.events:
		if type(event) is sf.CloseEvent: window.close()
		if type(event) is sf.KeyEvent and event.pressed:
			if event.code == sf.Keyboard.ESCAPE:	window.close()
		if type(event) is sf.MouseWheelEvent:
			if event.delta>0:	window.view.zoom( 7./8. )
			else:				window.view.zoom( 8./7. )
			scale= window.view.size.x
			print 'scale=',scale
		if type(event) is sf.MouseButtonEvent:
			if event.button == sf.Mouse.MIDDLE:
				panFrom= window.map_pixel_to_coords(event.position) if event.pressed else None
		if panFrom and type(event) is sf.MouseMoveEvent:
			pos=window.map_pixel_to_coords(event.position)
			dx,dy = panFrom-pos
			panFrom= pos
			window.view.move(dx,dy)



def getWASD():
	dx,dy=0,0
	if sf.Keyboard.is_key_pressed(sf.Keyboard.A):		dx=-1
	elif sf.Keyboard.is_key_pressed(sf.Keyboard.D):		dx= 1

	if sf.Keyboard.is_key_pressed(sf.Keyboard.W):		dy=-1
	elif sf.Keyboard.is_key_pressed(sf.Keyboard.S):		dy= 1
	return dx,dy

clock = sf.Clock()
speed=.5
deg2rad = 6.283185/360

framerate=0.0 ; iFramerate=int(0)
fpsText = sf.Text()
fpsText.font = sf.Font.from_file('/usr/share/fonts/truetype/freefont/FreeMonoBoldOblique.ttf')
fpsText.position = (8,8)
fpsText.character_size = 36

aVel=0 ; tVel=0
def navView():
	global scale,clock,deg2rad,speed,framerate,tDelta, aVel,tVel
	dx,dy = getWASD()
	tDelta = clock.restart().seconds
	framerate= .9*framerate+(1/tDelta*.1)

	if dx:	aVel = min([60,max([-60,aVel+120*dx*tDelta])])
	else: aVel*= 1-8*tDelta
	window.view.rotate(aVel*tDelta)

	dx= window.view.rotation * deg2rad

	if dy:	tVel = min([speed,max([-speed,tVel+speed*dy*tDelta])])
	else: tVel*= 1-8*tDelta
	dx,dy = sf.Vector2(-sin(dx),cos(dx))*tDelta*tVel*scale
	window.view.move(dx,dy)

iGlobalTime=0
while window.is_open:
	handleEvents()
	navView()

	x, y = sf.Mouse.get_position(window) / window.size
	#shader.set_parameter("iMouse", x,y, int(sf.Mouse.is_button_pressed(sf.Mouse.LEFT)) )

	window.clear(sf.Color(0, 128, 0))
	quad.align(window)
	i=int(framerate)
	if i!=iFramerate:
		iFramerate=i
		fpsText.string = str(i)
	iGlobalTime+=tDelta/8
	#shader.set_parameter('iGlobalTime', iGlobalTime )

	window.draw(quad,states)

	view=window.view
	window.view = window.default_view
	window.draw(fpsText)
	window.view=view

	window.display()









