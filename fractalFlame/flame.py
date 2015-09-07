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
def rand_num(lo=-1, hi=1):
    return lo + (hi - lo) * random.random()


# Функция рассчитывает коээфициенты афинных преобразований
def calc_afin_koeff(kol_afin_preobr):
    afin_preobr_list = []
    i = 0
    while i < kol_afin_preobr:
        tmp_dict = {}

        # Инициализируем коэффициенты заведомо неправильными значениями
        a = 2
        b = 2
        d = 2
        e = 2

        while (a*a + d*d) > 1:
            a = random.random()
            d = rand_num(a * a, KOEF_RANGE_MAX)
            # выбираем диапазон от -2 до 1, чтобы было равное количество
            # отриц. и положит. чисел, т.е. равноверноятное появление
            if random.randint(-2, 1) < 0:
                d = -d

        while (b*b + e*e) > 1:
            b = random.random()
            e = rand_num(b * b, KOEF_RANGE_MAX)
            if random.randint(-2, 1) < 0:
                e = -e

        if (a*a + b*b + d*d + e*e) < (1 + (a*e - b*d)*(a*e - b*d)):
            # формируем словарь с коэффициентами и добавляем в список
            i += 1

            tmp_dict['a'] = a
            tmp_dict['b'] = b
            tmp_dict['c'] = rand_num(-1, 1)
            if random.randint(-2, 1) < 0:
                tmp_dict['c'] = -tmp_dict['c']
            tmp_dict['d'] = d
            tmp_dict['e'] = e
            tmp_dict['f'] = rand_num(-1, 1)
            if random.randint(-2, 1) < 0:
                tmp_dict['f'] = -tmp_dict['f']

            # Выбираем случайным образом цвет стартового пикселя
            tmp_dict['red'] = random.randint(1, 255)
            tmp_dict['green'] = random.randint(1, 255)
            tmp_dict['blue'] = random.randint(1, 255)

            afin_preobr_list.append(tmp_dict)

    return afin_preobr_list


# Функция рисует точку в нужном месте и нужным цветом
def draw_point(x, y, r=1, g=1, b=1):
    turtle.penup()
    turtle.setpos(x, y)
    turtle.pendown()
    turtle.pencolor(r, g, b)
    turtle.dot()
    # print 'Точка с координатами [%f, %f]' % turtle.pos()


# Функция отрисовки изображения
def render(count_point=20000, kol_afin_preobr=16, num_iter=1000, x_res=1920, y_res=1080):
    """

    Функция рисует точки с учетом афинных преобразований
    """
    # инициализируем экран чтобы координата 0,0 лажала в нижнем левом углу
    turtle.setworldcoordinates(0, 0, x_res - 1, y_res - 1)
    turtle.colormode(255)
    turtle.speed(10)

    # Создаем список коэффициентов афинных преобразований
    afins_preobr_list = calc_afin_koeff(kol_afin_preobr)

    # Задаем словарь данных для свойств пикселя
    pixel_property = {'r': 0, 'g': 0, 'b': 0, 'counter': 0}

    # Формируем матрицу пикселей для сохранения их свойств
    y_row = [pixel_property for i in range(y_res)]
    pixel_list = [y_row for i in range(x_res)]

    # рисуем точки на экране
    for num in range(count_point):
        new_x = rand_num(XMIN, XMAX)
        new_y = rand_num(YMIN, YMAX)

        for step in range(-20, num_iter):
            i = random.randint(0, kol_afin_preobr - 1)

            x = (afins_preobr_list[i]['a'] * new_x +
                 afins_preobr_list[i]['b'] * new_y + afins_preobr_list[i]['c'])
            y = (afins_preobr_list[i]['d'] * new_x +
                 afins_preobr_list[i]['e'] * new_y + afins_preobr_list[i]['f'])

            # применяем линейное преобразование
            new_x = x
            new_y = y

            if step > 0:
                theta2 = 0
                symmetry = 2

                for sym in range(1, symmetry):

                    theta2 += (2*math.pi)/sym

                    x_rot = new_x * math.cos(theta2) - new_y * math.sin(theta2)
                    y_rot = new_x * math.sin(theta2) + new_y * math.cos(theta2)

                    if (x_rot >= XMIN and x_rot <= XMAX
                            and y_rot >= YMIN and y_rot <= YMAX):

                        x1 = x_res - int(((XMAX - x_rot) / (XMAX - XMIN)) * x_res)
                        y1 = y_res - int(((YMAX - y_rot) / (YMAX - YMIN)) * y_res)

                        # print '[%f, %f]' % (x1, y1)

                        if x1 < x_res and y1 < y_res:

                            # проверяем первый раз попали в точку или нет
                            if pixel_list[x1][y1]['counter'] == 0:
                                pixel_list[x1][y1]['r'] = afins_preobr_list[i]['red']
                                pixel_list[x1][y1]['g'] = afins_preobr_list[i]['green']
                                pixel_list[x1][y1]['b'] = afins_preobr_list[i]['blue']
                            else:
                                pixel_list[x1][y1]['r'] = ((pixel_list[x1][y1]['r'] +
                                                           afins_preobr_list[i]['red']) / 2)
                                pixel_list[x1][y1]['g'] = ((pixel_list[x1][y1]['g'] +
                                                           afins_preobr_list[i]['green']) / 2)
                                pixel_list[x1][y1]['b'] = ((pixel_list[x1][y1]['b'] +
                                                           afins_preobr_list[i]['blue']) / 2)

                            # отрисовываем точку на экране
                            draw_point(x1, y1, pixel_list[x1][y1]['r'],
                                       pixel_list[x1][y1]['g'], pixel_list[x1][y1]['b'])

                            pixel_list[x1][y1]['counter'] += 1


def main():
    lst = calc_afin_koeff(16)
    print lst


if __name__ == '__main__':
    main()
