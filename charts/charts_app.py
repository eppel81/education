# -*- coding: utf-8 -*-

import re

import collections

import turtle

import random

# функция для подсчета рейтинга встречающихся слов в строке
def string_parser(str_for_parse):
    """
    Функция возвращает список кортежей (слово : сколько раз встречается)

    """
    words = re.findall(r'\w+', str_for_parse.lower())
    cnt = collections.Counter(words)

    parsed_words = cnt.items()
    # отсортируем список кортежей по 2-му элементу в кортеже
    parsed_words.sort(key=lambda item: item[1], reverse=True)
    return parsed_words


def text_drawer(text, x, y, **colors):
    """

    Функция пишет текст легенды в нужных координатах и заданным цветом.
    """
    turtle.penup()
    turtle.goto(x, y)
    turtle.pendown()
    turtle.pencolor(colors['r'], colors['g'], colors['b'])
    turtle.dot(20)
    turtle.penup()
    turtle.goto(x + 25, y-10)
    turtle.write(text, True, font=('Arial', 12, 'normal'))


def circle_chart_drawer(words_list):
    """

    Функция отрисоввывает круговую жиаграмму
    """
    radius = 200

    # считаем сколько всего слов - нужно для расчета углов
    amount = sum(map(lambda item: item[1], words_list))

    turtle.colormode(255)
    turtle.speed(10)

    i = 0

    # сохраняем текущие координаты начала дуги
    curr_pos = (0, -radius)
    for word in words_list:
        r = random.randint(0, 255)
        g = random.randint(0, 255)
        b = random.randint(0, 255)

        # устанавливаем цвет, выбранный случайным образом
        turtle.fillcolor(r, g, b)

        turtle.penup()
        turtle.goto(curr_pos)
        turtle.pendown()
        turtle.begin_fill()

        # угол расчитываем исходя из общего количества слов (amount)
        angle = (360/amount)*word[1]

        turtle.circle(radius, angle)
        curr_pos = turtle.pos()

        # центр диаграммы в [0, 0]
        turtle.goto(0, 0)
        turtle.end_fill()
        # color_list.append(turtle.fillcolor())

        # сразу и легенду отрисовываем по этому слову. Параметры rgb передаются как словарь (**dict)
        text_drawer(word[0] + ' - ' + str(word[1]) + ' time(-s)', radius + 50, radius - i*30, r=r, g=g, b=b)

        # i нужна для междустрочного интервала в легенде
        i += 1


def main(text, type_diagr=1):
    """

    Функция выводит круговую диаграмму по встречаемости слов в строке, переданной ей параметром.
    """
    # находим список кортежей (слово, частота)
    words_count_list = string_parser(text)

    # рисуем диаграмму ( 1 - круговая, 2 - лучевая
    if type_diagr == 1:
        circle_chart_drawer(words_count_list)

    raw_input('Press any key')


if __name__ == '__main__':
    tmp = 'hello, world! hello world nice to meet you, world'
    main(tmp)