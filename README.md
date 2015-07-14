# VoroManhattan
Manhattan Voronoi diagram by Takashi Ohyama, in Python
Conversion of java code found at http://www.nirarebakun.com/voro/eman.html
This is incomplete, and very messy as of yet.
Regions are Poly in this. The VoroMan function returns an array of class Poly.
Poly has verts arranged in ccw order
test.py creates an OpenGL triangle fan and a shader for each poly. 
The shader is given the poly corners, which are used to find each pixels distance from the poly's border.
