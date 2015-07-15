#!/usr/bin/python

'''
  VoroManhattan.py
Manhattan Voronoi diagram by Takashi Ohyama, in Python.
Generates specified number of random centroids, and draws
the boundary lines between the centroids, using the 'manhattan' distance metric.
Takashi Ohyama's website: http://www.nirarebakun.com/

python ported version resides at https://github.com/bobbysoon/VoroManhattan/edit/master/man.py

'''
from Poly import *

#	jitter range?
CONST1 = 1000.0
CONST2 = 800.0


#	x-coordinate of intersection of two lines y=as x+bs and y= ask x+bsk
def koutenx(_as,_bs,ask,bsk):
	return (bsk-_bs)/(_as-ask)

#	y-coordinate of intersection of two lines y=as x+bs and y= ask x+bsk
def kouteny(as2,bs2,ask2,bsk2):
    return (bs2/as2-bsk2/ask2)/(1.0/as2-1.0/ask2)

#	subroutine of sort
#	 reorder te1[],te2[] such that te1[0]<te1[1]<...<te1[NN-1]
'''
from operator import itemgetter
def _heapv(te1,te2, NN):
	pa=zip(te1,te2)
	pa.sort(key=itemgetter(0))
	for i in range(NN):
		te1[i],te2[i] = pa[i]
'''
def heapv(te1,te2, NN):
	kks=int(NN/2)
	for kk in range(kks,0,-1):
		ii=kk
		b1=te1[ii-1]
		b2=te2[ii-1]
		while 2*ii<=NN:
			jj=2*ii
			if jj+1<=NN:
				if te1[jj-1]<te1[jj]:
					jj+=1

			if te1[jj-1]<=b1:
				break

			te1[ii-1]=te1[jj-1]
			te2[ii-1]=te2[jj-1]
			ii=jj

		te1[ii-1]=b1
		te2[ii-1]=b2

	mm=NN-1
	while mm>=1:
		c1=te1[mm];c2=te2[mm]
		te1[mm]=te1[0]
		te2[mm]=te2[0]
		ii=1
		while 2*ii<=mm:
			kk=2*ii
			if kk+1<=mm:
				if te1[kk-1]<=te1[kk]:
					kk+=1

			if te1[kk-1]<=c1:
				break

			te1[ii-1]=te1[kk-1]
			te2[ii-1]=te2[kk-1]
			ii=kk

		te1[ii-1]=c1
		te2[ii-1]=c2

		mm-=1


def maybeAddPoint(l,kx,ky,a,b,ak,bk,_min,_max):
	koutenx_a_b_ak_bk = koutenx(a,b,ak,bk)
	if (koutenx_a_b_ak_bk>_min and koutenx_a_b_ak_bk<_max):
		kx[l+1]=koutenx_a_b_ak_bk
		ky[l+1]=kouteny(a,b,ak,bk)
		return True

def simplifyLine(line):
	i=1
	while i+1<len(line):
		if collinear(line[i-1],line[i],line[i+1]): line.pop(i)
		else: i+=1

def isClockwise(poly,line,centroid):
	pa=[poly.verts[vi] for vi in line]
	xa=[p.x for p in pa]
	ya=[p.y for p in pa]
	pMin=Vec2(min(xa),min(ya))
	pMax=Vec2(max(xa),max(ya))
	c=(pMin+pMax)/2.0
	c=centroid
	a= (pa[0]-c).angle() - (pa[1]-c).angle()
	if a<-pi: a+=pi*2
	if a>pi: a-=pi*2
	return a>0

def intersectRays(ray1,ray2):
	a1,a2=ray1
	b1,b2=ray2
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

from random import random as rand
def Manhattan( P, boundingBox ):
	pMin,pMax = boundingBox
	pMin,pMax = Vec2(pMin),Vec2(pMax)
	width,height = pMax-pMin
	xMin,yMin = pMin
	xMax,yMax = pMax

	N=len(P)
	PLENTY=N*N	#	for line segments
	lMax=0

	smallVal = width/CONST1
	print 'smallVal:',smallVal

	#	centroids
	px=	[p.x for p in P]
	py=	[p.y for p in P]

	poly= [Poly(Vec2(px[k],py[k])) for k in range(N)]

	kx=	range(PLENTY)
	ky=	range(PLENTY)

	#	bisectors
	for i in range(N-1):
		print i
		for j in range(i+1,N):
			swapEm = abs(px[i]-px[j]) >= abs(py[i]-py[j])
			if swapEm:	px,py = py,px

			x1min=min([px[i],px[j]])
			x1max=max([px[i],px[j]])
			y1min=min([py[i],py[j]])
			y1max=max([py[i],py[j]])

			cp2=(py[i]+py[j])/2
			cpx=(px[i]+px[j])/2

			tacoSalad = (px[i]-px[j])*(py[i]-py[j])>0
			di=(-1.0 if tacoSalad else 1.0)+rand()/CONST1

			yst=di*(x1min-cpx)+cp2
			yen=di*(x1max-cpx)+cp2
			l=0
			kx[l]=x1min
			ky[l]=di*(kx[l]-cpx)+cp2
			l+=1
			kx[l]=x1max
			ky[l]=di*(kx[l]-cpx)+cp2
			a=di
			b=-di*cpx+cp2
			if tacoSalad:
				for k in range(N):
					if k!=i and k!=j:
						cp2k=(py[i]+py[k])/2.0
						cpxk=(px[i]+px[k])/2.0

						factoid = (px[i]-px[k])*(py[i]-py[k])>0
						ff=	-1.0 if factoid else 1.0

						if (abs(px[i]-px[k]) < abs(py[i]-py[k])):
							dik=	ff+rand()/CONST1
							di2k=	ff*rand()/CONST2
							di3k=	ff*rand()/CONST2
							x1mink=	min([px[i],px[k]])
							x1maxk=	max([px[i],px[k]])
							ystk=	dik*(x1mink-cpxk)+cp2k
							yenk=	dik*(x1maxk-cpxk)+cp2k
							if not factoid:
								if maybeAddPoint(l,kx,ky,a,b,dik,-dik*cpxk+cp2k, x1min,x1max ): l+=1
							if maybeAddPoint(l,kx,ky,a,b,di2k,-di2k*x1mink+ystk, x1min,x1max ): l+=1
							if maybeAddPoint(l,kx,ky,a,b,di3k,-di3k*x1maxk+yenk, x1min,x1max ): l+=1
						else:
							dik=	ff+rand()/(CONST2 if factoid else CONST1)
							di2k=	ff*CONST2+rand()/CONST2
							di3k=	ff*CONST2+rand()/CONST2
							y1mink=	min([py[i],py[k]])
							y1maxk=	max([py[i],py[k]])
							xstk=	(y1mink-cp2k)/dik+cpxk
							xenk=	(y1maxk-cp2k)/dik+cpxk
							if not factoid:
								if maybeAddPoint(l,kx,ky,a,b,dik,-dik*cpxk+cp2k, x1min,x1max ): l+=1
							if maybeAddPoint(l,kx,ky,a,b,di2k,-di2k*xstk+y1mink, x1min,x1max ): l+=1
							if maybeAddPoint(l,kx,ky,a,b,di3k,-di3k*xenk+y1maxk, x1min,x1max ): l+=1

				di2=-rand()/CONST2
				l+=1
				kx[l]=xMin
				ky[l]=di2*(kx[l]-x1min)+yst
				a=di2
				b=-di2*x1min+yst
				for k in range(N):
					if k!=i and k!=j:
						cp2k=(py[i]+py[k])/2.0
						cpxk=(px[i]+px[k])/2.0

						factoid = (px[i]-px[k])*(py[i]-py[k])>0
						ff=	-1.0 if factoid else 1.0

						dik=ff+rand()/CONST1
						if (abs(px[i]-px[k])<abs(py[i]-py[k])):
							if maybeAddPoint(l,kx,ky,a,b,dik,-dik*cpxk+cp2k, xMin,x1min ): l+=1
						else:
							di2k=	ff*CONST2+rand()/CONST2
							di3k=	ff*CONST2+rand()/CONST2
							y1mink=	min([py[i],py[k]])
							y1maxk=	max([py[i],py[k]])
							xstk=	(y1mink-cp2k)/dik+cpxk
							xenk=	(y1maxk-cp2k)/dik+cpxk
							if maybeAddPoint(l,kx,ky,a,b,dik,-dik*cpxk+cp2k, xMin,x1min ): l+=1
							if maybeAddPoint(l,kx,ky,a,b,di2k,-di2k*xstk+y1mink, xMin,x1min ): l+=1
							if maybeAddPoint(l,kx,ky,a,b,di3k,-di3k*xenk+y1maxk, xMin,x1min ): l+=1


				di3=-rand()/CONST2
				l+=1
				kx[l]=xMax
				ky[l]=di3*(kx[l]-x1max)+yen
				a=di3
				b=-di3*x1max+yen
				for k in range(N):
					if (k!=i and k!=j):
						cp2k=(py[i]+py[k])/2.0
						cpxk=(px[i]+px[k])/2.0

						factoid = (px[i]-px[k])*(py[i]-py[k])>0
						ff=	-1.0 if factoid else 1.0

						dik=	ff+rand()/CONST1
						if maybeAddPoint(l,kx,ky,a,b,dik,-dik*cpxk+cp2k, x1max,xMax ): l+=1
						if not (abs(px[i]-px[k])<abs(py[i]-py[k])):
							di2k=	ff*CONST2+rand()/CONST2
							di3k=	ff*CONST2+rand()/CONST2
							y1mink=	min([py[i],py[k]])
							y1maxk=	max([py[i],py[k]])
							xstk=	(y1mink-cp2k)/dik+cpxk
							xenk=	(y1maxk-cp2k)/dik+cpxk
							if maybeAddPoint(l,kx,ky,a,b,di2k,-di2k*xstk+y1mink, x1max,xMax ): l+=1
							if maybeAddPoint(l,kx,ky,a,b,di3k,-di3k*xenk+y1maxk, x1max,xMax ): l+=1

			else: # not tacoSalad
				for k in range(N):
					if (k!=i and k!=j):
						cp2k=(py[i]+py[k])/2.0
						cpxk=(px[i]+px[k])/2.0

						factoid = (px[i]-px[k])*(py[i]-py[k])>0
						ff=	-1.0 if factoid else 1.0

						dik=ff+rand()/CONST1
						if (abs(px[i]-px[k])<abs(py[i]-py[k])):
							di2k=	ff*rand()/CONST2
							di3k=	ff*rand()/CONST2
							x1mink=	min([px[i],px[k]])
							x1maxk=	max([px[i],px[k]])
							ystk=	dik*(x1mink-cpxk)+cp2k
							yenk=	dik*(x1maxk-cpxk)+cp2k
							if factoid:
								if maybeAddPoint(l,kx,ky,a,b,dik,-dik*cpxk+cp2k, x1min,x1max ): l+=1
							if maybeAddPoint(l,kx,ky,a,b,di2k,-di2k*x1mink+ystk, x1min,x1max ): l+=1
							if maybeAddPoint(l,kx,ky,a,b,di3k,-di3k*x1maxk+yenk, x1min,x1max ): l+=1
						else:
							di2k=	ff*CONST2+rand()/CONST2
							di3k=	ff*CONST2+rand()/CONST2
							y1mink=	min([py[i],py[k]])
							y1maxk=	max([py[i],py[k]])
							xstk=	(y1mink-cp2k)/dik+cpxk
							xenk=	(y1maxk-cp2k)/dik+cpxk
							if factoid:
								if maybeAddPoint(l,kx,ky,a,b,dik,-dik*cpxk+cp2k, x1min,x1max ): l+=1
							if maybeAddPoint(l,kx,ky,a,b,di2k,-di2k*xstk+y1mink, x1min,x1max ): l+=1
							if maybeAddPoint(l,kx,ky,a,b,di3k,-di3k*xenk+y1maxk, x1min,x1max ): l+=1

				di2=rand()/CONST2
				l+=1
				kx[l]=yMin
				ky[l]=di2*(kx[l]-x1min)+yst
				a=di2
				b=-di2*x1min+yst
				for k in range(N):
					if (k!=i and k!=j):
						cp2k=(py[i]+py[k])/2.0
						cpxk=(px[i]+px[k])/2.0

						factoid = (px[i]-px[k])*(py[i]-py[k])>0
						ff=	-1.0 if factoid else 1.0

						dik=ff+rand()/CONST1
						if (abs(px[i]-px[k])<abs(py[i]-py[k])):
							if maybeAddPoint(l,kx,ky,a,b,dik,-dik*cpxk+cp2k, yMin,x1min ): l+=1
						else:
							di2k=	ff*CONST2+rand()/CONST2
							di3k=	ff*CONST2+rand()/CONST2
							y1mink=	min([py[i],py[k]])
							y1maxk=	max([py[i],py[k]])
							xstk=	(y1mink-cp2k)/dik+cpxk
							xenk=	(y1maxk-cp2k)/dik+cpxk
							if maybeAddPoint(l,kx,ky,a,b,dik,-dik*cpxk+cp2k, yMin,x1min ): l+=1
							if maybeAddPoint(l,kx,ky,a,b,di2k,-di2k*xstk+y1mink, yMin,x1min ): l+=1
							if maybeAddPoint(l,kx,ky,a,b,di3k,-di3k*xenk+y1maxk, yMin,x1min ): l+=1

				di3=rand()/CONST2
				l+=1
				kx[l]=yMax # may be wrong
				ky[l]=di3*(kx[l]-x1max)+yen
				a=di3
				b=-di3*x1max+yen
				for k in range(N):
					if (k!=i and k!=j):
						cp2k=(py[i]+py[k])/2.0
						cpxk=(px[i]+px[k])/2.0

						factoid = (px[i]-px[k])*(py[i]-py[k])>0
						ff=	-1.0 if factoid else 1.0

						dik=ff+rand()/CONST1
						if (abs(px[i]-px[k])<abs(py[i]-py[k])):
							if maybeAddPoint(l,kx,ky,a,b,dik,-dik*cpxk+cp2k, x1max,yMax ): l+=1
						else:
							di2k=	ff*CONST2+rand()/CONST2
							di3k=	ff*CONST2+rand()/CONST2
							y1mink=	min([py[i],py[k]])
							y1maxk=	max([py[i],py[k]])
							xstk=	(y1mink-cp2k)/dik+cpxk
							xenk=	(y1maxk-cp2k)/dik+cpxk
							if maybeAddPoint(l,kx,ky,a,b,dik,-dik*cpxk+cp2k, x1max,yMax ): l+=1
							if maybeAddPoint(l,kx,ky,a,b,di2k,-di2k*xstk+y1mink, x1max,yMax ): l+=1
							if maybeAddPoint(l,kx,ky,a,b,di3k,-di3k*xenk+y1maxk, x1max,yMax ): l+=1





			if swapEm:
				# un-swap axes
				px,py=py,px
				kx,ky=ky,kx


			heapv(kx,ky, l+1 )

			lMax=max([lMax,l])
			line = []
			for k in range(l):
				k2=k+1
				xx=(kx[k]+kx[k2])/2.0
				yy=(ky[k]+ky[k2])/2.0
				ds=abs(xx-px[i])+abs(yy-py[i])
				br2=True
				for u in range(N):
					if (u!=i and u!=j):
						us=abs(xx-px[u])+abs(yy-py[u])
						if (us<ds):
							br2=False
							break

				if br2:
					if not line: line.append( Vec2(kx[k],ky[k]) )
					line.append( Vec2(kx[k2],ky[k2]) )

			if line:
				simplifyLine(line) # remove collinear verts
				poly[i].borders.append(Border(line[:],poly[j]))
				poly[j].borders.append(Border(line[:],poly[i]))

	for pol in poly: pol.isClosed=pol.loopBorders(smallVal=smallVal)
	return [pol for pol in poly if pol.isClosed]

def VoroMan(centroids, boundingBox):
	polies = Manhattan( centroids, boundingBox ) # bounding box not really implemented yet. Only size is used.
	for pol in polies:
		pol.verts=[]
		pol.others=[]
		for b in pol.borders:
			verts=b.line[:-1]
			pol.verts.extend(verts)
			pol.others.extend([b.other and b.other.isClosed]*len(verts))
			b.nVerts=len(b.line)
			delattr(b,'line')

		s=0 # CCW winding order
		for i in range(len(pol.verts)):
			x1,y1=pol.verts[i-1]
			x2,y2=pol.verts[i]
			s+=(x1-x2)*(y1-y2)
		pol.reversed=s<0
		if False and pol.reversed:
			pol.verts.reverse()
			pol.others.reverse()

	return polies

