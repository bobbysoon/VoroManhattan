#!/usr/bin/python

def rayRayIntersectPoint(a1,a2,b1,b2):
	#print a1,a2,b1,b2
	x1_,y1_ = a1
	x2_,y2_ = a2
	x3_,y3_ = b1
	x4_,y4_ = b2

	# Make sure the lines aren't parallel
	if ((y2_ - y1_) / (x2_ - x1_) != (y4_ - y3_) / (x4_ - x3_)):
		d = (((x2_ - x1_) * (y4_ - y3_)) - (y2_ - y1_) * (x4_ - x3_))
		if (d != 0):
			r = (((y1_ - y3_) * (x4_ - x3_)) - (x1_ - x3_) * (y4_ - y3_)) / d
			s = (((y1_ - y3_) * (x2_ - x1_)) - (x1_ - x3_) * (y2_ - y1_)) / d
			if (r >= 0) and (s >= 0):
				return Vec2(x1_ + r * (x2_ - x1_), y1_ + r * (y2_ - y1_))

def intersect(r1,r2):
	a1,a2=r1
	b1,b2=r2
	return rayRayIntersectPoint(a1,a2,b1,b2)

from Vec2 import *


class Edge:
	def __init__(self, edge,other):
		self.p1,self.p2 = edge
		self.other = other


class Border:
	def __init__(self, line, other):
		self.line=line
		self.other=other
		self.prev,self.next = None,None
		self.flipped=False

	def __delitem__(self, key):				self.line.__delattr__(key)
	def __getitem__(self, key):				return self.line[key]
	def __setitem__(self, key, value):		self.line[key]= value

	def reverse(self):
		#if self.flipped: raise
		#self.flipped=not self.flipped
		self.line.reverse()



def collinear(p0, p1, p2, asBool=True):
	n= abs((p1.x-p0.x)*(p2.y-p0.y)-(p2.x-p0.x)*(p1.y-p0.y))
	return (n < 1e-8) if asBool else n


class Poly:
	def __init__(self, centroid):
		self.centroid= centroid
		self.borders=[]
		#self.verts=[]
		#self.lines=[]
		#self.others=[]
		#self.edges=[]

	def addLine(self, other, line):
		self.lines.append(line)
		self.others.append(other)

	#	manhattan distance of p to self.centroid
	def dist(self, p):
		dx,dy=p-self.centroid
		return abs(dx)+abs(dy)

	def bordersAreLooped(self):
		b2=self.borders[-1]
		for b1 in self.borders:
			if b2.line[-1]!=b1.line[0]:
				return False
			b2=b1
		return True

	def nearest(self, pa,oba,smallVal):
		dists=[]
		for b in oba:
			for i,j in [(0,0),(0,-1),(-1,0),(-1,-1)]:
				d=pa[i].dist(b[j]);dists.append(d)
				if d<smallVal:	return b,i,j,d
		return None,None,None,min(dists)

	def loopBorders(self, smallVal):
		borders=[self.borders.pop()]
		while self.borders:
			pa=[borders[0][0],borders[-1][-1]]
			b,i,j,d = self.nearest(pa,self.borders,smallVal)
			if not b:
				print 'motherfucker - '+str(d)
				break
				assert b, 'motherfucker - '+str(d)
			self.borders.pop(self.borders.index(b))
			if i==j: b.reverse()
			if i:	borders.append(b)
			else:	borders.insert(0,b)
			if i:	borders[-2].next , borders[-1].prev = borders[-1] , borders[-2]
			else:	borders[ 0].next , borders[ 1].prev = borders[ 1] , borders[ 0]

		if self.borders:
			print 'what the fuck'
			self.wtf=True
		else:
			self.wtf=False
			b0,b1=borders[0],borders[-1]
			p0,p1=b0[0],b1[-1]
			if p0.dist(p1)<smallVal:
				b0.prev,b1.next = b1,b0
		#assert not self.borders, 'what the fuck'

		b2= borders[-1]
		for b1 in borders:
			if b1.prev==b2 and b2.next==b1:
				r1=b1[1],b1[0]
				r2=b2[-2],b2[-1]
				ip=intersect(r1,r2)
				#assert ip, 'bloody hell'
				if ip:
					b1[0],b2[-1] = ip,ip
				else:
					print 'bloody hell:',borders.index(b2),borders.index(b1)
			b2=b1

		self.borders=borders # sorted, hopefully

		return self.bordersAreLooped()
