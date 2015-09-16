# -*- coding: utf-8 -*-

# задаем золотую пирамиду
triangle = [
        [4],
       [2, 1],
      [2, 2, 5],
     [3, 5, 3, 1],
    [2, 2, 2, 4, 2],
   [2, 3, 4, 5, 2, 3]
]


def mini_triangle(triangle, row=0, column=0, total=0):
    """

    Функция возвращает максимум из суммы вершины и каждой из 2-х нижних вершин малого треугольника.
    Вызывается рекурсивно для каждого попадающегося малого треугольника
    """
    # если стоим у основания пирамиды, то просто суммируем число с накопленным по ходу значением
    if row == (len(triangle) - 1):
        return total + triangle[row][column]

    # рекурсивно вызываем функцию к 2-м нижним вершинам малого треугольника
    return max(mini_triangle(triangle, row + 1, column, total + triangle[row][column]),
               mini_triangle(triangle, row + 1, column + 1, total + triangle[row][column]))


if __name__ == '__main__':
    print 'Максимальная сумма чисел = %d' % (mini_triangle(triangle))
