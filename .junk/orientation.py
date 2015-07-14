def orientation(poly,line,centroid):
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
	return a

