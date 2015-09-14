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

# X_RES = 888
# Y_RES = 500

# X_RES = 1920
# Y_RES = 1080

COUNT_AFIN_TRANSFORMS = 5


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


def render_pixels(afins_transform_list, x_res=888, y_res=500, transform_mode=2, num_iter=1000, count_point=10000):
    """

    Функция возвращает матрицу точек с учетом цвета и афинных преобразований
    """

    # инициализируем экран чтобы координата 0,0 лажала в нижнем левом углу
    # turtle.setworldcoordinates(0, 0, x_res - 1, y_res - 1)
    # turtle.colormode(255)
    # turtle.speed(10)

    # Задаем словарь данных для свойств одного пикселя
    pixel_property = {'r': 0, 'g': 0, 'b': 0, 'counter': 0, 'normal': 0}

    # Формируем матрицу пикселей для сохранения их свойств
    pixel_list = [[dict(pixel_property) for i in range(y_res)] for j in range(x_res)]

    for num in range(count_point):
        new_x = random.uniform(XMIN, XMAX)
        new_y = random.uniform(YMIN, YMAX)

        for step in range(-20, num_iter):
            i = random.randint(0, COUNT_AFIN_TRANSFORMS - 1)

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
                symmetry = 2

                for sym in range(1, symmetry):

                    theta2 += (2*math.pi)/sym

                    x_rot = new_x * math.cos(theta2) - new_y * math.sin(theta2)
                    y_rot = new_x * math.sin(theta2) + new_y * math.cos(theta2)

                    if x_rot >= XMIN and x_rot <= XMAX and y_rot >= YMIN and y_rot <= YMAX:

                        x1 = x_res - int(((XMAX - x_rot) / (XMAX - XMIN)) * x_res)
                        y1 = y_res - int(((YMAX - y_rot) / (YMAX - YMIN)) * y_res)

                        if x1 < x_res and y1 < y_res:

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


def correction(pixel_matrix):
    """
    Функция выполняет коррекцию яркости каждого пикселя матрицы пикселей
    """
    max_value = 0.0
    gamma = 2.2

    # Пройдемся по матрице. Каждый элемент матрицы - это словарь свойств пикселя
    for col in pixel_matrix:
        for pixel in col:
            if pixel['counter'] != 0:
                pixel['normal'] = math.log10(pixel['counter'])
                if pixel['normal'] > max_value:
                    max_value = pixel['normal']

    for col in pixel_matrix:
        for pixel in col:
            pixel['normal'] /= max_value
            pixel['r'] = (pixel['r'] * math.pow(pixel['normal'], (1.0 / gamma)))
            pixel['g'] = (pixel['g'] * math.pow(pixel['normal'], (1.0 / gamma)))
            pixel['b'] = (pixel['b'] * math.pow(pixel['normal'], (1.0 / gamma)))

    return pixel_matrix


def draw_points(matrix, x_res, y_res):
    """

    Функция рисует точки в соответствии с переданной матрицей свойств пикселей.
    """
    # инициализируем экран чтобы координата 0,0 лажала в нижнем левом углу
    turtle.setworldcoordinates(0, 0, x_res - 1, y_res - 1)
    turtle.colormode(255)
    turtle.speed(10)
    turtle.pensize(1)

    for x in range(len(matrix)):
        for y in range(len(matrix[x])):
            # если цвет точки не есть цветом фона, то рисуем ее
            if matrix[x][y]['r'] > 0 and matrix[x][y]['g'] > 0 and matrix[x][y]['b'] > 0:
                turtle.penup()
                turtle.setpos(x, y)
                turtle.pendown()
                turtle.pencolor(matrix[x][y]['r'], matrix[x][y]['g'],
                                matrix[x][y]['b'])
                turtle.dot(1)
                # print 'Точка с координатами [%f, %f]' % turtle.pos()


def save_coeff_to_file(fname, coeff_dict):
    """
    Функция сохраняет в json-формате параметры афинных преобразований в файл
    """
    try:
        with open(fname, 'w') as f:
            json.dump(coeff_dict, f)
    except:
        return False


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
        --iter - количество итераций
        -w - количество точек по горизонтали
        -h - количество точек по вертикали
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('-l', help='load afin transformation coefficients from file', type=str)
    # parser.add_argument('-s', help='file to save afin transformation coefficients', type=str)
    parser.add_argument('--type', help='type of transformation', choices=range(4))
    parser.add_argument('-i', help='amount of iterations', type=int)
    parser.add_argument('-x', help='number of points on the x-axis', type=int)
    parser.add_argument('-y', help='number of points on the y-axis', type=int)

    args = parser.parse_args()

    # если есть параметр l, то загружаем из файла
    if args.l:
        afins_transform_list = read_coeff_from_file(args.l)

        # если не удалось прочитать файл
        if not afins_transform_list:
            print 'Не удалось загрузить кэффициенты из файла'
            return False
    else:
        # Создаем список расчетных коэффициентов афинных преобразований
        afins_transform_list = calc_afin_coeff(COUNT_AFIN_TRANSFORMS)

    # если есть параметр type, то задаем тип преобразования (по умолчанию 0 - линейный)
    transform_mode = args.type if args.type else 0

    # если есть параметр i, то задаем количество итераций
    num_iter = args.i if args.i else 1000

    # если есть параметр -x, то задаем размер изображения по оси Х
    x_res = args.x if args.x else 888

    # если есть параметр -y, то задаем размер изображения по оси Y
    y_res = args.y if args.y else 500

    # Получаем матрицу свойств пикселей. Результат м.б. False если не удалось вычислить коэффициенты.
    # В render_pixels передаем только параметры командной строки, остальные - по умолчанию.
    pixel_matrix = render_pixels(afins_transform_list, x_res, y_res, transform_mode, num_iter)

    if pixel_matrix:
        correction(pixel_matrix)
        draw_points(pixel_matrix, x_res, y_res)
    else:
        print 'Не получилось подобрать коэффициенты. Попробуйте еще раз.'
        return False

    s = raw_input('Сохранить? Y/N')

    if s.lower() == 'y':
        save_coeff_to_file('coeff.txt', afins_transform_list)


if __name__ == '__main__':
    main()
