#!/usr/bin/python

import sfml as sf
from sys import maxint

def Window(wd=800,ht=600): # on_resize	class Window(sf.Window):
	vm=sf.VideoMode(wd,ht)
	window = sf.RenderWindow( vm, "Press Esc to close" )
	window.position= 400,50
	window.vertical_synchronization = True
	window.view.center = (0,0)
	#window.view.size = window.size/8
	return window


BLACK=	sf.Color.BLACK
DGREY=	sf.Color(64,64,64,255)
GREY=	sf.Color(128,128,128,255)
WHITE=	sf.Color.WHITE
GREEN=	sf.Color.GREEN
RED=	sf.Color.RED
BLUE=	sf.Color.BLUE
YELLOW=	sf.Color.YELLOW
GREEN=	sf.Color.GREEN
PURPLE=	sf.Color(255,0,255,255)
ORANGE=	sf.Color(255,128,0,255)


def hue(h, s=1.0, v=1.0):
	if s == 0.0: v*=255; return sf.Color(v, v, v)
	i = int(h*6.) # XXX assume int() truncates!
	f = (h*6.)-i
	p = int(255*(v*(1.-s)))
	q = int(255*(v*(1.-s*f)))
	t = int(255*(v*(1.-s*(1.-f))))
	v*=255
	i%=6
	if i == 0: return sf.Color(v, t, p)
	if i == 1: return sf.Color(q, v, p)
	if i == 2: return sf.Color(p, v, t)
	if i == 3: return sf.Color(p, q, v)
	if i == 4: return sf.Color(t, p, v)
	if i == 5: return sf.Color(v, p, q)

ZOOMSTEP=16.0
panSpeed=8.
from math import *
class Graphics:
	def __init__(self, WindowSize, rate=15, debug=False ):
		self.debug=debug
		self.window=Window(WindowSize,WindowSize)
		self.line = sf.VertexArray(sf.PrimitiveType.LINES_STRIP, 2)
		self.circle = sf.CircleShape()
		self.circle.fill_color=sf.Color.TRANSPARENT
		self.circle.radius=2
		self.window.view.reset((0,0,WindowSize,WindowSize))
		self.clear=self.window.clear
		self.draw=self.window.draw
		self.display=self.window.display
		self.window.framerate_limit = rate # draw speed limiter
		self.scale= self.window.view.size.x/self.window.size.x
		self.pointClicked= sf.Vector2(0,0)
		self.hideStuff=True
		self.panFrom=None

	def setColor(self,c):
		self.circle.outline_color=c
		self.line[0].color=c
		self.line[1].color=c

	def drawCircle(self, pos ):
		vx,vy=self.window.view.size
		wx,wy=self.window.size
		dx=float(vx)/wx
		dy=float(vy)/wy
		s=sqrt(dx*dx+dy*dy)
		self.circle.outline_thickness= s
		self.circle.radius=s*3
		self.circle.position= pos-self.circle.radius
		self.window.draw(self.circle)

	def drawLine(self, p1,p2 ):
		self.line[0].position = p1
		self.line[1].position = p2
		self.window.draw(self.line)

	def pollEvents(self):
		dx,dy=0,0

		for event in self.window.events:
			if type(event) is sf.CloseEvent: self.window.close()
			if type(event) is sf.KeyEvent and event.pressed:
				if event.code == sf.Keyboard.ESCAPE:	self.window.close()
				if event.code == sf.Keyboard.H:			self.hideStuff= not self.hideStuff

			if type(event) is sf.MouseWheelEvent:
				if event.delta>0:	self.window.view.zoom( ZOOMSTEP/(ZOOMSTEP+1) )
				else:				self.window.view.zoom( (ZOOMSTEP+1)/ZOOMSTEP )
				self.scale= self.window.view.size.x/self.window.size.x

			if type(event) is sf.MouseButtonEvent:
				if event.button==sf.Mouse.LEFT and event.pressed:
					self.onLeftClick( self.window.map_pixel_to_coords(event.position) )
				if event.button == sf.Mouse.MIDDLE:
					self.panFrom= (event.position) if event.pressed else None

			if type(event) is sf.MouseMoveEvent:
				pos=(event.position)
				self.window.title=str(self.window.map_pixel_to_coords(pos))
				if self.panFrom:
					dx,dy = self.panFrom-pos
					self.panFrom= pos
					self.window.view.move(dx*self.scale,dy*self.scale)

		if sf.Keyboard.is_key_pressed(sf.Keyboard.A):
			self.window.view.zoom(ZOOMSTEP/(ZOOMSTEP+1))
			#print self.window.view.size
			self.scale= self.window.view.size.x/self.window.size.x
		elif sf.Keyboard.is_key_pressed(sf.Keyboard.Z):
			self.window.view.zoom((ZOOMSTEP+1)/ZOOMSTEP)
			#print self.window.view.size
			self.scale= self.window.view.size.x/self.window.size.x

		if sf.Keyboard.is_key_pressed(sf.Keyboard.LEFT):	dx=-1
		elif sf.Keyboard.is_key_pressed(sf.Keyboard.RIGHT):	dx= 1
		if sf.Keyboard.is_key_pressed(sf.Keyboard.UP):		dy=-1
		elif sf.Keyboard.is_key_pressed(sf.Keyboard.DOWN):	dy= 1

		self.window.view.move(dx*self.scale*panSpeed,dy*self.scale*panSpeed)


