# VoroManhattan
Manhattan Voronoi diagram by Takashi Ohyama, in Python
Conversion of java code found at http://www.nirarebakun.com/voro/eman.html
This is incomplete, and very messy as of yet.
Regions are Poly in this. The VoroMan function returns an array of class Poly.
Poly has verts arranged in ccw order.
Something quirky going on with poly.border vertsSlice, after reversing. Per-edge neighbor poly determination seems buggered. Indexing verts and finding who shares what verts would be a borkround.
test.py creates an OpenGL triangle fan and a shader for each poly.
The shader is given the poly corners, which are used to find each pixels distance from the poly's border.

vertsSlice:
	index range of poly.verts which defines the border. Adjacent borders share end verts.
	example values of a poly's border.vertsSlices:
		(-1, 2) (1, 4) (3, 6) (5, 9) (8, 10) (9, 12) (11, 15)
