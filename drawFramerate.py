#!/usr/bin/python

import sfml as sf

framerate=0.0 ; iFramerate=int(0)
fpsText = sf.Text()
ttf='/usr/share/games/extremetuxracer/fonts/PaperCuts_outline.ttf'
#ttf='/usr/share/fonts/truetype/freefont/FreeMonoBoldOblique.ttf'
fpsText.font = sf.Font.from_file(ttf)
fpsText.position = (8,8)
fpsText.character_size = 36

def drawFramerate():
	framerate= .9*framerate+(1/tDelta*.1)
	i=int(framerate)
	if i!=iFramerate:
		iFramerate=i
		fpsText.string = str(i)

	view=g.window.view
	g.window.view = g.window.default_view
	g.window.push_GL_states() # protects poly shaders from text
	g.window.draw(fpsText)
	g.window.pop_GL_states()
	g.window.view=view
