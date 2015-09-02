# -*- coding: utf-8 -*-
"""
Принимаем сразу, что 1-я и 2-я вершины треугольника лежат в горизонтальной плоскости, 
а третья вершина может быть top или bottom. Это касается и серединного треугольника
"""
import turtle as t

#функция отрисовывает треугольник и возвращает словарь с координатами вершин и длиной сторон
#параметры: координаты 1-й вершины, длина сторон
def triangleDrawer(startx, starty, length, head='top'):	
	coordsList = []
	descrTriangle = {}
	if head == 'top':
		head = 120
		t.color("black","black")
	elif head == 'bottom':
		head = 240
		t.color("white","white")
	t.setheading(0)
	t.penup()
	t.begin_fill()
	t.setpos(startx, starty)
	t.pendown()
	coordsList.append(t.pos())
	t.forward(length)
	coordsList.append(t.pos())
	t.setheading(head)
	t.forward(length)
	coordsList.append(t.pos())
	if head == 120:
		t.left(120)
	else:
		t.right(120)	
	t.forward(length)
	t.end_fill()
	descrTriangle['length'] = length
	descrTriangle['coord'] = coordsList
	return descrTriangle

#расчет координат середины стороны треугольника
def subtrCoord(first, second):
	first = round (first,1)
	second = round (second,1)
	if first >= second:
		res = (first-second)/2
		res = first - res
		return res
	else:
		res = (second - first)/2
		res = second - res
		return res

#функция расчитывает координаты серединного треугольника
def calcNewCoord(coordList):
	newCoordList = []
#	newCoordList = coordList
	newCoordList.append([subtrCoord(coordList[0][0], coordList[2][0]), subtrCoord(coordList[0][1], coordList[2][1])])
	newCoordList.append([subtrCoord(coordList[1][0], coordList[0][0]), subtrCoord(coordList[1][1], coordList[0][1])])
	newCoordList.append([subtrCoord(coordList[2][0], coordList[1][0]), subtrCoord(coordList[2][1], coordList[1][1])])
	return newCoordList


#рекурсивная ф-я. Вырезает серединный треугольник и определяет три оставшихся	
def cutter(deep, startTriangle): 

	#координаты треугольника, который нужно вырезать. Вообще-то можно рассчитывать только первую вершину...
	cutTriangleCoord=calcNewCoord(startTriangle['coord'])	
	cutTriangle = triangleDrawer(cutTriangleCoord[0][0], cutTriangleCoord[0][1], startTriangle['length']/2, 'bottom') #(dict)

	RangTriangle = []
	RangTriangle.append([startTriangle['coord'][0], cutTriangle['coord'][2], cutTriangle['coord'][0]])
	RangTriangle.append([cutTriangle['coord'][0], cutTriangle['coord'][1], startTriangle['coord'][2]])
	RangTriangle.append([cutTriangle['coord'][2], startTriangle['coord'][1], cutTriangle['coord'][1]])


	for i in range(3):
		cutTriangleCoord = calcNewCoord(RangTriangle[i])
		descrTriangle = {}
		descrTriangle['length'] = cutTriangle['length']
		descrTriangle['coord'] = RangTriangle[i]
		if deep > 1:
			cutter((deep-1), descrTriangle)


#основная функция
#параметры: X, Y, длина стороны, количество разделений
def main(startX = 0, startY = 0, sideLength = 200, deep = 5):
	t.speed(10)
	startTriangle = triangleDrawer(startX, startY, sideLength)	#стартовый треугольник (dict)
	cutter(deep, startTriangle)

if __name__ == '__main__':
	main(-200, -100, 400, 5)