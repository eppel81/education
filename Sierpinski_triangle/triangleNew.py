# -*- coding: utf-8 -*-

import turtle as t


# Функция строит треугольник. Принимает в качестве параметров координаты 
# левой вершины (кортеж с координатами X Y), длину стороны и текущий уровень
# вложенности (уровень определяет цвет заливки треугольника)
#
# initAngle определяет угол левой вершины треульника.

def triangleDrawer(leftCornerCoord, sideSize, deep=5):
	initAngle = 60
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
	t.forward(sideSize)
	t.right(initAngle*2)
	t.forward(sideSize)
	t.right(initAngle*2)
	t.forward(sideSize)
	t.end_fill()


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


def main(coord=(-100,0), sideLength=300, deep=5):
	t.speed(10)
	triangleDrawer(coord, sideLength)
	serpTriangleDrawer(coord, sideLength/2, deep)


if __name__ == '__main__':
	main()