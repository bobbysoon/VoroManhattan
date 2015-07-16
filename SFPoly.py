#!/usr/bin/python

from SFMLGraphics import *
from Poly import *

class SFPoly(sf.Drawable,Poly):
	def __init__(self, poly, pMin,pScale):
		self.poly=poly
		poly.sfPoly=self
		self.initPolyGLFan(pMin,pScale)
		self.vertsArray = sf.VertexArray(sf.PrimitiveType.LINES_STRIP,len(self.poly.verts))
		for i in range(len(self.poly.verts)):
			self.vertsArray[i] = sf.Vertex(self.poly.verts[i],WHITE)
		self.center = sum(self.poly.verts)/len(self.poly.verts)
	def interlink(self, polies):
		self.others=[b.other.sfPoly if b.other and hasattr(b.other,'sfPoly') else None for b in self.poly.borders]
		self.adjacentPolies=[b.other.sfPoly for b in self.poly.borders if b.other and hasattr(b.other,'sfPoly') and b.other.sfPoly in polies]
	def draw(self, target, states):
		#states.shader = self.shader
		target.draw(self.glFan, states)
	def initPolyGLFan(self,pMin,pScale):
		self.glFan=sf.VertexArray(sf.PrimitiveType.TRIANGLES_FAN, 2+len(self.poly.verts))
		self.glFan[0].position=self.poly.centroid
		self.glFan[0].tex_coords=self.poly.centroid
		self.glFan[0].color=GREY
		for i in range(len(self.poly.verts)):
			self.glFan[1+i].position=self.poly.verts[i]
			self.glFan[1+i].tex_coords=self.poly.verts[i]
			self.glFan[1+i].color=GREY
		self.glFan[1+len(self.poly.verts)].position=self.poly.verts[0]
		self.glFan[1+len(self.poly.verts)].tex_coords=self.poly.verts[0]
		self.glFan[1+len(self.poly.verts)].color=GREY
		#self.shader = sf.Shader.from_file(None, initFrag(self.poly,pMin,pScale) )
		#self.states = sf.RenderStates(shader=)

