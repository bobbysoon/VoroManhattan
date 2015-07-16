#!/usr/bin/python

__all__ = ['LongestPolyPath']

polies=None

def PolyPath(cell,cells,others):
	global polies
	paths={}
	for n in others[cell]:			#	for each neighbor,
		if not [None for nn in others[n] if not nn in cells]:
			nCells= [c for c in cells if c!=cell]
			path = PolyPath(n,nCells,others)
			paths[len(path)]=path

	path = [cell]
	if paths:
		longestPath= paths[sorted(paths.keys())[-1]]
		path.extend(longestPath)

	return path

def LongestPolyPath(__polies__,loopStep=None):
	global polies
	polies = __polies__
	others=[[polies.index(n) for n in p.adjacentPolies if n in polies] for p in polies]
	cells= range(len(polies))
	outerCells = [polies.index(p) for p in polies if None in p.others]
	paths = {}
	for cell in outerCells:
		path= PolyPath(cell,cells,others)
		if path:
			paths[len(path)]= path
			if loopStep:
				pathPolies = [polies[i] for i in range(len(polies)) if i in path]
				loopStep( pathPolies )

	path = paths[sorted(paths.keys())[-1]]

	return [polies[i] for i in path]


