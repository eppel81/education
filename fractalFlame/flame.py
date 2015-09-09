# -*- coding: utf-8 -*-

import turtle

import random

import math

import json

import argparse


XMIN = -1.777
XMAX = 1.777
YMIN = -1
YMAX = 1

COEFF_RANGE_MIN = -1
COEFF_RANGE_MAX = 1

X_RES = 1920
Y_RES = 1080


def select_afin_transform(num):
    """
    Функция выбирает нужное афинное преобразование по его номеру.
    Результатом возвращается функция, расчитывающая нужные координаты
    """

    def linear(x, y):
        """
        Фунцкция возвращает параметры для линейного преобразования
        """
        new_x = x
        new_y = y
        return new_x, new_y


    def sinusoidal(x, y):
        """
        Фунцкция возвращает параметры для синусоидального преобразования
        """
        new_x = math.sin(x)
        new_y = math.sin(y)
        return new_x, new_y


    def spherical(x, y):
        """
        Фунцкция возвращает параметры для сферического преобразования
        """
        r = 1.0 / (x*x + y*y)
        new_x = r * x
        new_y = r * y
        return new_x, new_y


    def swirl(x, y):
        """
        Фунцкция возвращает параметры для преобразования Свирла
        """
        r = x*x + y*y
        new_x = x*math.sin(r) - y*math.cos(r)
        new_y = x*math.cos(r) + y*math.sin(r)
        return new_x, new_y

    # связываем ключи словаря с функциями, возвращающими параметры афинн. преобр.
    type_afin_transform = {
        0: linear,
        1: sinusoidal,
        2: spherical,
        3: swirl
    }

    return type_afin_transform[num]

def calc_rand_coeff():
    """

    Функция подбирает случайным образом пару коэффициентов и проверяет
    неравенство, заданное условием подбора коэффициентов. Возвращает кортеж.
    """

    # Выбрали 1000 попыток подбора коэффициентов, чтобы не зациклиться.
    max_steps = 1000

    i = 0
    k1 = 2
    k2 = 2
    while ((k1*k1 + k2*k2) > 1) and i < max_steps:
        k1 = random.random()
        k2 = random.uniform(k1*k1, COEFF_RANGE_MAX)

        # выбираем диапазон от -2 до 1, чтобы было равное количество
        # отриц. и положит. чисел, т.е. равноверноятное появление
        if random.randint(-2, 1) < 0:
            k2 = -k2
        i += 1

    # если за 1000 шагов не нашли значение, то прерываемся
    if i >= max_steps:
        return False
    else:
        return k1, k2


def calc_afin_coeff(count_afin_transforms):
    """

    Функция рассчитывает коээфициенты афинных преобразований и вовращает список или False.
    """
    afin_transform_list = []
    i = 0
    while i < count_afin_transforms:
        tmp_dict = {}

        # расчет a, d коэффициентов. Если False, то возвращаем False
        coeff = calc_rand_coeff()
        if (coeff):
            a = coeff[0]
            d = coeff[1]
        else:
            return False

        # расчет b, e коэффициентов. Если False, то возвращаем False
        coeff  = calc_rand_coeff()
        if coeff:
            b = coeff[0]
            e = coeff[1]
        else:
            return False

        if (a*a + b*b + d*d + e*e) < (1 + (a*e - b*d)*(a*e - b*d)):
            # формируем словарь с коэффициентами и добавляем в список
            i += 1

            tmp_dict['a'] = a
            tmp_dict['b'] = b
            tmp_dict['c'] = random.uniform(-1, 1)
            if random.randint(-2, 1) < 0:
                tmp_dict['c'] = -tmp_dict['c']
            tmp_dict['d'] = d
            tmp_dict['e'] = e
            tmp_dict['f'] = random.uniform(-1, 1)
            if random.randint(-2, 1) < 0:
                tmp_dict['f'] = -tmp_dict['f']

            # Выбираем случайным образом цвет стартового пикселя
            tmp_dict['red'] = random.randint(1, 255)
            tmp_dict['green'] = random.randint(1, 255)
            tmp_dict['blue'] = random.randint(1, 255)

            afin_transform_list.append(tmp_dict)

    return afin_transform_list


# Функция рисует точку в нужном месте и нужным цветом
# def draw_point2(x, y, r=1, g=1, b=1):
#     turtle.penup()
#     turtle.setpos(x, y)
#     turtle.pendown()
#     turtle.pencolor(r, g, b)
#     turtle.dot()


def render_pixels(args, count_afin_transforms=16, count_point=1000, num_iter=1000, transform_mode=3):
    """

    Функция возвращает матрицу точек с учетом цвета и афинных преобразований
    """

    # инициализируем экран чтобы координата 0,0 лажала в нижнем левом углу
    # turtle.setworldcoordinates(0, 0, X_RES - 1, Y_RES - 1)
    # turtle.colormode(255)
    # turtle.speed(10)

    # если есть параметр l, то загружаем из файла
    if args.l:
        afins_transform_list = read_coeff_from_file(args.l)
    else:
        # Создаем список расчетных коэффициентов афинных преобразований
        afins_transform_list = calc_afin_coeff(count_afin_transforms)

    # если есть параметр s, то сохраняем коэффициенты в файл
    if args.s:
        save_coeff_to_file(args.s, afins_transform_list)

    # если есть параметр type, то задаем тип преобразования (по умолчанию 0 - линейный)
    if args.type:
        transform_mode = args.type

    # Задаем словарь данных для свойств одного пикселя
    pixel_property = {'r': 0, 'g': 0, 'b': 0, 'counter': 0}

    # Формируем матрицу пикселей для сохранения их свойств
    y_row = [pixel_property for i in range(Y_RES)]
    pixel_list = [y_row for i in range(X_RES)]

    # просчитываем точки в матрице
    for num in range(count_point):
        new_x = random.uniform(XMIN, XMAX)
        new_y = random.uniform(YMIN, YMAX)

        for step in range(-20, num_iter):
            i = random.randint(0, count_afin_transforms - 1)

            x = (afins_transform_list[i]['a'] * new_x +
                 afins_transform_list[i]['b'] * new_y + afins_transform_list[i]['c'])
            y = (afins_transform_list[i]['d'] * new_x +
                 afins_transform_list[i]['e'] * new_y + afins_transform_list[i]['f'])

            # Здесь вызываем ф-ю, возвращающую функцию нужного преобразования
            tmp = select_afin_transform(transform_mode)(x, y)
            new_x = tmp[0]
            new_y = tmp[1]

            if step > 0:
                theta2 = 0
                symmetry = 3

                for sym in range(1, symmetry):

                    theta2 += (2*math.pi)/sym

                    x_rot = new_x * math.cos(theta2) - new_y * math.sin(theta2)
                    y_rot = new_x * math.sin(theta2) + new_y * math.cos(theta2)

                    if x_rot >= XMIN and x_rot <= XMAX and y_rot >= YMIN and y_rot <= YMAX:

                        x1 = X_RES - int(((XMAX - x_rot) / (XMAX - XMIN)) * X_RES)
                        y1 = Y_RES - int(((YMAX - y_rot) / (YMAX - YMIN)) * Y_RES)

                        if x1 < X_RES and y1 < Y_RES:

                            # проверяем первый раз попали в точку или нет
                            if pixel_list[x1][y1]['counter'] == 0:
                                pixel_list[x1][y1]['r'] = afins_transform_list[i]['red']
                                pixel_list[x1][y1]['g'] = afins_transform_list[i]['green']
                                pixel_list[x1][y1]['b'] = afins_transform_list[i]['blue']
                            else:
                                pixel_list[x1][y1]['r'] = ((pixel_list[x1][y1]['r'] +
                                                           afins_transform_list[i]['red']) / 2)
                                pixel_list[x1][y1]['g'] = ((pixel_list[x1][y1]['g'] +
                                                           afins_transform_list[i]['green']) / 2)
                                pixel_list[x1][y1]['b'] = ((pixel_list[x1][y1]['b'] +
                                                           afins_transform_list[i]['blue']) / 2)

                            pixel_list[x1][y1]['counter'] += 1
                            # draw_point2(x1, y1, pixel_list[x1][y1]['r'], pixel_list[x1][y1]['g'],
                            #             pixel_list[x1][y1]['b'])
    return pixel_list


def draw_points(matrix):
    """

    Функция рисует точки в соответствии с переданной матрицей свойств пикселей.
    """
    # инициализируем экран чтобы координата 0,0 лажала в нижнем левом углу
    turtle.setworldcoordinates(0, 0, X_RES - 1, Y_RES - 1)
    turtle.colormode(255)
    turtle.speed(10)
    turtle.pensize(1)

    for x in range(len(matrix)):
        for y in range(len(matrix[x])):
            turtle.penup()
            turtle.setpos(x, y)
            turtle.pendown()
            turtle.pencolor(matrix[x][y]['r'], matrix[x][y]['g'],
                            matrix[x][y]['b'])
            turtle.dot()
            # print 'Точка с координатами [%f, %f]' % turtle.pos()


def save_coeff_to_file(fname, coeff_dict):
    """
    Функция сохраняет в json-формате параметры афинных преобразований в файл
    """
    f = open(fname, 'w')
    try:
        json.dump(coeff_dict, f)
    except Exception:
        return False
    finally:
        f.close()


def read_coeff_from_file(fname):
    """
    Функция читает из файла параметры афинных преобразований
    """
    try:
        return json.load(file(fname))
    except Exception:
        return False


def main():
    """

    Точка входа в приложение. В качестве опциональных параметров задаются:
        -s 'имя файла' - для сохранения коэффициентов афинных преобразований;
        -l 'имя файла' - для загрузки коэффициентов из файла
        --type - тип преобразования (0 - линейное, 1 - синусоидальное, 2 - сферическое
                                     3 - преобразование Свирла)
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', help='file to save afin transformation coefficients', type=str)
    parser.add_argument('-l', help='load afin transformation coefficients from file', type=str)
    parser.add_argument('--type', help='type of transformation', type=int)
    args = parser.parse_args()

    # Получаем матрицу свойств пикселей. Результат м.б. False если не удалось вычислить коэффициенты.
    # В render_pixels передаем только параметры командной строки, остальные - по умолчанию.
    pixel_matrix = render_pixels(args)

    if pixel_matrix:
        draw_points(pixel_matrix)
        pass
    else:
        print 'Не получилось подобрать коэффициенты. Попробуйте еще раз.'


if __name__ == '__main__':
    main()
