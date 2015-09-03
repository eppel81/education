# -*- coding: utf-8 -*- 

import turtle as t

import random as r

# Функция строит треугольник. Принимает в качестве параметров координаты 
# левой вершины (кортеж с координатами X Y), длину стороны и текущий уровень
# вложенности (уровень определяет цвет заливки треугольника)
#
# Возвращает все координаты вершин правильного треугольника в списке. Это
# нужно для постоения фрактала методом хаоса.
#
# initAngle определяет угол левой вершины треульника.

def triangleDrawer(leftCornerCoord, sideSize, deep=5):
	cornersCoord = []
	initAngle = 60

	# если достигли дна, т.е. deep=0, то закрашиваем треугольник черным
	if deep > 1:
		color = 'white'
	else:
		color = 'black'

	t.color('black', color)
	t.begin_fill()
	t.penup()
	t.setpos(leftCornerCoord[0],leftCornerCoord[1])
	t.pendown()
	t.setheading(initAngle)
	cornersCoord.append(leftCornerCoord)
	
	t.forward(sideSize)
	t.right(initAngle*2)
	cornersCoord.append(t.pos())
	
	t.forward(sideSize)
	t.right(initAngle*2)
	cornersCoord.append(t.pos())
	
	t.forward(sideSize)
	t.end_fill()

	return cornersCoord


# Фцнкция передвигает указатель и не оставляет след (не рисует)

def movePointer(angle, sideSize):
	"""
	Передвигает указатель на нужное расстояние и под нужным углом
	
	"""
	t.setheading(angle)
	t.penup()
	t.forward(sideSize)
	t.pendown()	
	

# Функция строит три треульника с длиной стороны вдвое меньшей родительского.
# Расчет позиции левых вершин треугольников исходит из длины стороны и угла.
# Сначала строит треугольник №1 в левой вершине родительского треугольника. 
# Далее указатель переезжает на длину стороны в вершину треугольника №1 и 
# стоится треугольник №2. Далее указатель переводится на расстояние длины 
# треугольника с углом -60 градусов в точку вершины треульника №3.

def serpTriangleDrawer(leftCornerCoord, sideSize, deep=5):
	initAngle = 60
	triagDict = {}
	
	if deep > 0:
		triagDict['firstTriangleCoord'] = leftCornerCoord
		
		triangleDrawer(triagDict['firstTriangleCoord'], sideSize, deep)
		
		movePointer(initAngle,sideSize)
		triagDict['secTriangleCoord'] = t.pos()
		triangleDrawer(triagDict['secTriangleCoord'], sideSize, deep)
		
		movePointer(-initAngle,sideSize)
		triagDict['thirdTriangleCoord'] = t.pos()
		triangleDrawer(triagDict['thirdTriangleCoord'], sideSize, deep)

		for key in triagDict:
			serpTriangleDrawer(triagDict[key], sideSize/2, deep-1)


# Функция поиска середины отрезка по крайним координатам

def subtrCoord(coord1, coord2):
	res = (max(coord1, coord2) - min(coord1, coord2))/2
	return (max(coord1, coord2) - res)


# Функция отображает фрактал методом хаоса. 

def haosMode(coords=0, numIter=1000):
	
	startPoint = (100,75)
	t.dot(2)
	for i in range(numIter):
		randCorner = coords[r.randint(0, 2)]
		newPoint =    (subtrCoord(startPoint[0], randCorner[0]), 
						subtrCoord(startPoint[1], randCorner[1]))
		startPoint = newPoint
		t.penup()
		t.setpos(startPoint[0], startPoint[1])
		t.pendown()
		t.dot(2)
		


# Главная функция. Принимает параметры: 
#     алгоритм (по умолчанию итеративный);
#     координаты левого угла
#     длину стороны
#     глубина разделения в итеративном методе.

def main(alg='iter', coord=(-100,0), sideLength=300, deep=5):
	"""
	У функции обязательный параметр alg. Может быть 'iter' или 'haos'

	"""
	t.speed(10)

	# по умолчанию 3000 точек для нормального проявления
	countPoints = 3000

	if alg == 'iter':
		triangleDrawer(coord, sideLength)
		serpTriangleDrawer(coord, sideLength/2, deep)
	elif alg == 'haos':
		coords = triangleDrawer(coord, sideLength)
		haosMode(coords , countPoints)
	else:
		print 'Задан неправильный алгоритм построения'



if __name__ == '__main__':
	main('haos')