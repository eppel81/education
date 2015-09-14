# -*- coding: utf-8 -*- 

import turtle

import random


# Функция строит треугольник. Принимает в качестве параметров координаты
# левой вершины (кортеж с координатами X Y), длину стороны и текущий уровень
# вложенности (уровень определяет цвет заливки треугольника)
#
# Возвращает все координаты вершин правильного треугольника в списке.  Это
# нужно для постоения фрактала методом хаоса.  
#
# initAngle определяет угол левой вершины треульника.  
def triangle_drawer(leftCornerCoord, sideSize, deep=5):
    cornersCoord = []
    initAngle = 60

    # если достигли дна, т.е. deep=0, то закрашиваем треугольник черным
    if deep > 1:
        color = 'white'
    else:
        color = 'black'

    turtle.color('black', color)
    turtle.begin_fill()
    turtle.penup()
    turtle.setpos(leftCornerCoord[0], leftCornerCoord[1])
    turtle.pendown()
    turtle.setheading(initAngle)
    cornersCoord.append(leftCornerCoord)

    turtle.forward(sideSize)
    turtle.right(initAngle * 2)
    cornersCoord.append(turtle.pos())

    turtle.forward(sideSize)
    turtle.right(initAngle * 2)
    cornersCoord.append(turtle.pos())

    turtle.forward(sideSize)
    turtle.end_fill()

    return cornersCoord


# Фцнкция передвигает указатель и не оставляет след (не рисует).
def move_pointer(angle, sideSize):
    """
    Передвигает указатель на нужное расстояние и под нужным углом

    """
    turtle.setheading(angle)
    turtle.penup()
    turtle.forward(sideSize)
    turtle.pendown()


# Функция строит три треульника с длиной стороны вдвое меньшей родительского.  
# Расчет позиции левых вершин треугольников исходит из длины стороны и угла.  
# Сначала строит треугольник №1 в левой вершине родительского треугольника.  
# Далее указатель переезжает на длину стороны в вершину треугольника №1 и 
# стоится треугольник №2.  Далее указатель переводится на расстояние длины 
# треугольника с углом -60 градусов в точку вершины треульника №3.  
def serp_triangle_drawer(leftCornerCoord, sideSize, deep=5):
    initAngle = 60
    triagDict = {}

    if deep > 0:
        triagDict['firstTriangleCoord'] = leftCornerCoord

        triangle_drawer(triagDict['firstTriangleCoord'], sideSize, deep)

        move_pointer(initAngle, sideSize)
        triagDict['secTriangleCoord'] = turtle.pos()
        triangle_drawer(triagDict['secTriangleCoord'], sideSize, deep)

        move_pointer(-initAngle, sideSize)
        triagDict['thirdTriangleCoord'] = turtle.pos()
        triangle_drawer(triagDict['thirdTriangleCoord'], sideSize, deep)

        for key in triagDict:
            serp_triangle_drawer(triagDict[key], sideSize / 2, deep - 1)


# Функция поиска середины отрезка по крайним координатам
def subtr_coord(coord1, coord2):
    res = (max(coord1, coord2) - min(coord1, coord2)) / 2
    return (max(coord1, coord2) - res)


# Функция отображает фрактал методом хаоса.
def haos_mode(coords=0, numIter=1000):
    startPoint = (100, 75)
    turtle.dot(2)
    for i in range(numIter):
        randCorner = coords[random.randint(0, 2)]
        newPoint = (subtr_coord(startPoint[0], randCorner[0]),
                    subtr_coord(startPoint[1], randCorner[1]))
        startPoint = newPoint
        turtle.penup()
        turtle.setpos(startPoint[0], startPoint[1])
        turtle.pendown()
        turtle.dot(2)


# Главная функция. Принимает параметры: 
#     алгоритм (по умолчанию итеративный);
#     координаты левого угла
#     длину стороны
#     глубина разделения в итеративном методе.
def main(alg='iter', coord=(-100, 0), sideLength=300, deep=5):
    """
    У функции обязательный параметр alg. Может быть 'iter' или 'haos'

    """
    turtle.speed(10)

    # по умолчанию 3000 точек для нормального проявления
    countPoints = 3000

    if alg == 'iter':
        triangle_drawer(coord, sideLength)
        serp_triangle_drawer(coord, sideLength / 2, deep)
    elif alg == 'haos':
        coords = triangle_drawer(coord, sideLength)
        haos_mode(coords, countPoints)
    else:
        print 'Задан неправильный алгоритм построения'


if __name__ == '__main__':
    main('haos')
