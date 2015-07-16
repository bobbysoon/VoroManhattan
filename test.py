#!/usr/bin/python

from CreatePolies import *
from drawFramerate import *
from LongestPolyPath import *
from Player import *

clock = sf.Clock() ; time=0.0

def loopStep(drawPolies):
	global tDelta,time, polies
	tDelta= clock.restart().seconds ; time+= tDelta

	g.pollEvents()
	g.clear()
	for poly in drawPolies:		g.draw(poly)
	for poly in polies:			g.draw(poly.vertsArray)
	g.display()

def lirp(a,b,i):
	return a*(1-i)+b*i

def gameStep(window):
	window.view.center= player.position

	window.clear( sf.Color(0,0,0) )
	for poly in polies:		window.draw(poly)
	for poly in polies:		window.draw(poly.vertsArray)
	window.draw(player)
	window.display()
	window.view.rotation= player.rotation

	#window.view.move( dx, dy)


polies = CreatePolies()
polies=LongestPolyPath(polies,loopStep)
orientation = (polies[1].center-polies[0].center).angle()*360.0/6.283185
player=Player(polies[0].center,orientation)

while g.window.is_open:
	g.pollEvents()
	player.input()
	player.move()
	gameStep(g.window)


