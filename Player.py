import sfml as sf
from Vec2 import *

SPEED=1
STRAIF=.75
SPIN=2.5
ORANGE= sf.Color(255,128,0,255)
GREY= sf.Color(0,0,0,128)

class Player(sf.Drawable):
	def __init__(self, pos, rot):
		self.position=pos
		self.rotation=rot
		radius=2
		self.drawable = sf.CircleShape(radius=radius)
		self.drawable.fill_color= ORANGE
		self.drawable.outline_color= GREY
		self.drawable.outline_thickness=1
		self.drawable.origin = radius,radius

	def input(self):
		if sf.Keyboard.is_key_pressed(sf.Keyboard.A):	self.turn=-1
		elif sf.Keyboard.is_key_pressed(sf.Keyboard.D):	self.turn= 1
		else: self.turn=0

		if sf.Keyboard.is_key_pressed(sf.Keyboard.W):	self.accel= 1
		elif sf.Keyboard.is_key_pressed(sf.Keyboard.S):	self.accel=-1
		else: self.accel=0

		if sf.Keyboard.is_key_pressed(sf.Keyboard.Q):	self.straif=-1
		elif sf.Keyboard.is_key_pressed(sf.Keyboard.E):	self.straif= 1
		else: self.straif=0
		if self.straif: self.accel,self.turn=0,0

	def move(self):
		rad= self.rotation * 6.283185/360
		dx,dy = sin(rad),cos(rad)
		self.forward = Vec2(dx,-dy)
		self.right = Vec2(dy,dx)
		self.position+= self.forward*self.accel*SPEED + self.right*self.straif*STRAIF
		self.rotation+= self.turn*SPIN
		self.drawable.position = self.position
		self.drawable.rotation = self.rotation

	def draw(self, target, states):
		target.draw(self.drawable, states)

