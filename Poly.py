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

	def interlink(self, otherBorders, smallVal):
		for b in otherBorders:
			dists= {self.line[i].dist(b.line[j]):(i,j) for i,j in [(0,0),(0,-1),(-1,0),(-1,-1)]}
			nearest= sorted(dists.keys())[0]
			if nearest and nearest<smallVal:
				i,j = dists[nearest]
				if i==j:
					j=-1-j ; b.reverse()
				if i:	ii,jj=-2,1
				else:	ii,jj=1,-2
				if nearest>0:
					ip= rayRayIntersectPoint(self.line[ii],self.line[i],b.line[jj],b.line[j])
					if ip:
						self.line[i],b.line[j] = ip,ip
				if i:	self.next,b.prev = b,self
				else:	self.prev,b.next = b,self
			else:
				print 'nearest=',nearest
	def debug(self, otherBorders):
		for b in otherBorders:
			dists= {self.line[i].dist(b.line[j]):(i,j) for i,j in [(0,0),(0,-1),(-1,0),(-1,-1)]}
			print sorted(dists.keys())[:3]
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
		self.verts=[]
		self.lines=[]
		self.others=[]
		self.edges=[]
		self.borders=[]

	def addLine(self, other, line):
		self.lines.append(line)
		self.others.append(other)

	def _addLine(self, other, line):
		for p in line:
			if not p in self.verts:
				self.verts.append(p)
		line=[self.verts.index(p) for p in line]
		self.lines.append(line)

	def sortedVertIndices(self):
		vc=sum(self.verts)/len(self.verts)
		va={(self.verts[vi]-vc).angle():vi for vi in range(len(self.verts))}
		via= [va[a] for a in sorted(va.keys())]
		return via

	def refineEdges(self, ignoreTrisectors=True):
		if not hasattr(self,'verts'): self.indexVerts()
		l=len(self.edges)
		dele=[]
		for ei1 in range(l-1):
			if not ei1 in dele:
				e1=self.edges[ei1]
				for ei2 in range(1,l):
					if not ei2 in dele:
						e2=self.edges[ei2]
						if ignoreTrisectors or e1.other==e2.other: # same poly on other side
							pa=list(set([e1.p1,e1.p2,e2.p1,e2.p2]))
							if len(pa)==3 and self.collinear(pa):
								if		e1.p1==e2.p1:
										e1.p1=e2.p2
										dele.append(ei2)
								elif	e1.p1==e2.p2:
										e1.p1=e2.p1
										dele.append(ei2)
								elif	e1.p2==e2.p1:
										e1.p2=e2.p2
										dele.append(ei2)
								elif	e1.p2==e2.p2:
										e1.p2=e2.p1
										dele.append(ei2)

		dele=list(set(dele))
		self.edges=[self.edges[i] for i in range(l) if not i in dele]

	def removeUnusedVerts(self):
		if not hasattr(self,'verts'): self.refineEdges()
		usedVerts= sorted(list(set([vi for edge in self.edges for vi in [edge.p1,edge.p2]])))
		for edge in self.edges:
			edge.p1= usedVerts.index(edge.p1)
			edge.p2= usedVerts.index(edge.p2)
		self.verts = [self.verts[vi] for vi in usedVerts]

	def initBoundingBox(self, openVerts):
		if not hasattr(self,'verts'): self.removeUnusedVerts()
		xa=[self.verts[vi].x for vi in openVerts]
		ya=[self.verts[vi].y for vi in openVerts]
		xMin,xMax = min(xa),max(xa) ; wd=xMax-xMin
		yMin,yMax = min(ya),max(ya) ; ht=yMax-yMin
		self.boundingBox = Vec2(xMin,yMin),Vec2(xMax,yMax)
		self.smallVal=sqrt(wd*wd+ht*ht)/(len(self.verts)**2)

	def vertEdgeOther(self, vi):
		for edge in self.edges:
			if edge.p1==vi:		return edge,edge.p2
			if edge.p2==vi:		return edge,edge.p1
		return None,None

	def rayRayIntersectPoint(self, oi,vi,oj,vj):
		oi=self.verts[oi]
		vi=self.verts[vi]
		oj=self.verts[oj]
		vj=self.verts[vj]
		return rayRayIntersectPoint(oi,vi,oj,vj)

	def weldOpenVerts(self):
		if not hasattr(self,'verts'): self.removeUnusedVerts()
		openVerts = [vi for vi in range(len(self.verts)) if len([e for e in self.edges if vi in [e.p1,e.p2]])==1]
		self.initBoundingBox(openVerts) # determine smallVal
		while len(openVerts)>1:
			vi=openVerts.pop()
			da={(self.verts[vi]-self.verts[vj]).length():vj for vj in openVerts}
			d=sorted(da.keys())[0]
			if d>self.smallVal: break
			vj=da[d] ; openVerts.remove(vj)
			ei,oi=self.vertEdgeOther(vi)
			ej,oj=self.vertEdgeOther(vj)
			ip= self.rayRayIntersectPoint(oi,vi,oj,vj)
			if ip:
				ip=self.addVert(ip)
				if ei.p1==vi:	ei.p1=ip
				else:			ei.p2=ip
				if ej.p1==vj:	ej.p1=ip
				else:			ej.p2=ip
				return True

	def cleanup(self):
		self.indexVerts()
		self.refineEdges()
		self.removeUnusedVerts()
		self.weldOpenVerts()
		self.removeUnusedVerts()



	def draw(self):
		g.setColor(PURPLE)
		g.drawLine( p1,self.centroid )
		g.drawLine( p2,self.centroid )
		g.setColor(BLUE)
		g.drawLine( p1,p2 )

	def otherEdgeWithVertIndex(self, vi, notEdge):
		edges=[]
		for edge in self.edges:
			if edge!=notEdge:
				if edge.p1==vi: return edge,edge.p2
				if edge.p2==vi: return edge,edge.p1
		return None,None

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
