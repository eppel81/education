# -*- coding: utf-8 -*-

import turtle

import random

import math


XMIN = -1.777
XMAX = 1.777
YMIN = -1
YMAX = 1

KOEF_RANGE_MIN = -1
KOEF_RANGE_MAX = 1

# Функция генерирует случайное число в дипазоне
def rand_num(lo=-1, hi=-1):
	return (lo + (hi - lo)*random.random())

# Функция рассчитывает коээфициенты афинных преобразований
def calc_afin_koeff(KolAfinPreobr):
	AfinPreobrList = []
	i = 0
	while(i < KolAfinPreobr):
		TmpDict = {}
		a = 2
		b = 2
		c = 2
		d = 2
		e = 2
		f = 2

		while((a*a + d*d) > 1):
			a = random.random()
			d = rand_num(a*a, KOEF_RANGE_MAX)
			# выбираем диапазон от -2 до 1, чтобы было равное количество 
			# отриц. и положит. чисел, т.е. равноверноятное появление
			if (random.randint(-2,1) < 0):
				d = -d
		
		while((b*b + e*e) > 1):
			b = random.random()
			e = rand_num(b*b, KOEF_RANGE_MAX)
			if (random.randint(-2,1) < 0):
				e = -e


		if ((a*a + b*b + d*d + e*e) < (1 + (a*e - b*d)*(a*e - b*d))):
			# формируем словарь с коэффициентами и добавляем в список
			i += 1

			TmpDict['a'] = a
			TmpDict['b'] = b
			TmpDict['c'] = rand_num(-1, 1)
			if (random.randint(-2,1) < 0):
				c = -c
			TmpDict['d'] = d
			TmpDict['e'] = e
			TmpDict['f'] =  rand_num(-1, 1)
			if (random.randint(-2,1) < 0):
				f = -f

			# Выбираем случайным образом цвет стартового пикселя
			TmpDict['red'] = random.randint(1, 255)
			TmpDict['green'] = random.randint(1, 255)
			TmpDict['blue'] = random.randint(1, 255)

			AfinPreobrList.append(TmpDict)
	
	return AfinPreobrList

# Функция рисует точку в нужном месте и нужным цветом
def draw_point(x, y, r, g, b):
	turtle.penup()
	turtle.setpos(x, y)
	turtle.pendown()
	turtle.color(r,g,b)
	turtle.dot()

# Функция отрисовки изображения
def render(CountPoint=10000, KolAfinPreobr=16, Iter=1000, xRes=1920, yRes=1080):
	
	AfinsPreobrList = calc_afin_koeff(KolAfinPreobr)

	# Задаем словарь данных для свойств пикселя
	PixelProp = {'r' : 0, 'g' : 0, 'b' : 0, 'counter' : 0}

	# Формируем матрицу пикселей
	xRow = [PixelProp for i in range(xRes)]
	PixelList = [xRow for i in range(yRes)]

	for num in range(CountPoint):
	 	NewX = rand_num(XMIN, XMAX)
	 	NewY = rand_num(YMIN, YMAX)
	 	
	 	for step in range(-20, Iter):
	 		i = random.randint(0, KolAfinPreobr-1)
	 		
	 		x = (AfinsPreobrList[i]['a']*NewX + 
	 			AfinsPreobrList[i]['b']*NewY + AfinsPreobrList[i]['c'])
	 		y = (AfinsPreobrList[i]['d']*NewX + 
	 			AfinsPreobrList[i]['e']*NewY + AfinsPreobrList[i]['f'])

	 		# применяем линейное преобразование
	 		NewX = x
	 		NewY = y
		
	 		if step > 0:
	 			theta2 = 0
				symmetry = 2

				for sym in range(1, symmetry):
					
					#theta2 += (2*math.pi)/sym

					x_rot = NewX*math.cos(theta2) - NewY*math.sin(theta2)
					y_rot = NewX*math.sin(theta2) + NewY*math.cos(theta2)
		
					if (x_rot >= XMIN and x_rot <= XMAX 
							and	y_rot >= YMIN and y_rot <= YMAX):
					
						x1 = xRes - int(((XMAX - x_rot)/(XMAX - XMIN))*xRes)
						y1 = yRes - int(((YMAX - y_rot)/(YMAX - YMIN))*yRes)

						#print '[%f, %f]' % (x1, y1)
											

						if (x1 < xRes and y1 < yRes):

							# проверяем первый раз попали в точку или нет
							if PixelList[x1][y1]['counter'] == 0:
								PixelList[x1][y1]['r'] = AfinsPreobrList[i]['red']
								PixelList[x1][y1]['g'] = AfinsPreobrList[i]['green']
								PixelList[x1][y1]['b'] = AfinsPreobrList[i]['blue']
							else:
								PixelList[x1][y1]['r'] = ((PixelList[x1][y1]['r'] + 
													  AfinsPreobrList[i]['red'])/2)
								PixelList[x1][y1]['g'] = ((PixelList[x1][y1]['g'] + 
													  AfinsPreobrList[i]['green'])/2)
								PixelList[x1][y1]['b'] = ((PixelList[x1][y1]['b'] + 
													  AfinsPreobrList[i]['blue'])/2)

							# отрисовываем точку на экране
							draw_point(x1, y1, PixelList[x1][y1]['r'], 
									   PixelList[x1][y1]['g'], PixelList[x1][y1]['b'])
							
							PixelList[x1][y1]['counter'] += 1


def main():
	lst = calc_afin_koeff(16)
	print lst


if __name__ == '__main__':
	main()