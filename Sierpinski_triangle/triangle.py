"""Sierpinsky triangle drawer"""

import turtle as t

coordsList=[]

def triangleDrawer(startx=0, starty=0):
	t.penup()
	t.setpos(startx, starty)
	t.pendown()
	coordsList.append(t.position)
	t.right(60)
	t.forward(200)
	coordsList.append(t.position)
	t.right(120)
	t.forward(200)
	coordsList.append(t.position)
	t.right(120)
	t.forward(200)
	print coordsList

		
		