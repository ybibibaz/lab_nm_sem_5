import math
import matplotlib.pyplot as plt


A = 0
B = 10


def f(x):

    return math.log(x**2 + 3 * x + 1) - math.cos(2 * x + 1)


def dih_n(e):

    return math.floor(math.log(abs(B - A) / e, 2)) + 1


def gen_dots():
    ans = []
    for i in range(1000):
        ans.append(A + (B - A) / 1000 * i)

    return ans


def subplot(pos, x, y, title):
    plt.subplot(pos)
    plt.plot(x, y)
    plt.title(title)
    plt.grid(True)
    ax = plt.gca()
    ax.axhline(y=0, color='k')
    ax.axvline(x=0, color='k')


def dih(e):
    n_counter = 0
    start = A
    end = B
    while abs(end - start) > e:
        n_counter += 1
        c = (end + start) / 2
        if f(c) == 0:
            print('Найден точный корень {}, количество итераций = {}'.format(c, n_counter))

            return c
        elif f(start) * f(c) < 0:
            end = c
        else:
            start = c

    print('Численное количество итераций дихотомии = {}'.format(n_counter))

    return end


def dih_block(e):
    print('-------------------------------------------------')
    print('Значение корня с точностью 10^({}) = {}'.format(-e, dih(10**(-e))))
    print('Алгебраическое количество итераций = {}'.format(dih_n(10**(-e))))
    print('-------------------------------------------------')


def dir(x):

    return (x * 2 + 3) / (x ** 2 + x * 3 + 1) + 2 * math.sin(x * 2 + 1)


def newton(e):
    xk = (A + B) / 2
    xk1 = xk - f(xk) / dir(xk)
    n_counter = 1
    while abs(xk1 - xk) > e:
        n_counter += 1
        xk = xk1
        xk1 = xk1 - f(xk1) / dir(xk1)

    print('Численное количество итераций метода Ньютона = {}'.format(n_counter))

    return xk1


def newton_block(e):
    print('-------------------------------------------------')
    print('Значение корня с точностью 10^({}) = {}'.format(-e, newton(10 ** (-e))))
    print('-------------------------------------------------')


def chord(e):
    xk = B
    xk1 = A
    n_counter = 1
    while abs(xk1 - xk) > e:
        n_counter += 1
        xk1, xk = xk1 - f(xk1) * (xk1 - xk) / (f(xk1) - f(xk)), xk1

    print('Численное количество итераций метода хорд = {}'.format(n_counter))

    return xk1


def chord_block(e):
    print('-------------------------------------------------')
    print('Значение корня с точностью 10^({}) = {}'.format(-e, chord(10 ** (-e))))
    print('-------------------------------------------------')


def chord_mod(e):
    xk = B
    xk1 = xk - f(xk) * (xk - A) / (f(xk) - f(A))
    n_counter = 1
    while abs(xk1 - xk) > e:
        n_counter += 1
        xk1, xk = xk1 - f(xk1) * (xk1 - A) / (f(xk1) - f(A)), xk1

    print('Численное количество итераций модифицированного метода хорд = {}'.format(n_counter))

    return xk1


def chord_mod_block(e):
    print('-------------------------------------------------')
    print('Значение корня с точностью 10^({}) = {}'.format(-e, chord_mod(10 ** (-e))))
    print('-------------------------------------------------')


def dih_speed(root):
    start = A
    end = B
    while end != root:
        R = math.log(abs(root - end)) / math.log(abs(root - start))
        c = (end + start) / 2
        if f(start) * f(c) < 0:
            end = c
        else:
            start = c

    return R


def newton_speed(root):
    xk = (A + B) / 2
    xk1 = xk - f(xk) / dir(xk)
    while xk1 != root:
        R = math.log(abs(root - xk1)) / math.log(abs(root - xk))
        xk = xk1
        xk1 = xk1 - f(xk1) / dir(xk1)

    return R


def chord_speed(root):
    xk = B
    xk1 = A
    while xk1 != root:
        R = math.log(abs(root - xk1)) / math.log(abs(root - xk))
        xk1, xk = xk1 - f(xk1) * (xk1 - xk) / (f(xk1) - f(xk)), xk1

    return R


def chord_mod_speed(root):
    xk = B
    xk1 = xk - f(xk) * (xk - A) / (f(xk) - f(A))
    while xk1 != root:
        R = math.log(abs(root - xk1)) / math.log(abs(root - xk))
        xk1, xk = xk1 - f(xk1) * (xk1 - A) / (f(xk1) - f(A)), xk1

    return R


def subplot1(pos, x, y, x1, y1, title):
    plt.subplot(pos)
    plt.plot(x, y, 'r')
    plt.plot(x1, y1, 'b')
    plt.title(title)
    plt.grid(True)
    ax = plt.gca()
    ax.axhline(y=0, color='k')
    ax.axvline(x=0, color='k')


def dop(e):
    xk = (A + B) / 2
    conv_list = [xk]
    xk1 = xk - f(xk) / dir(xk)
    conv_list.append(xk1)
    while abs(xk1 - xk) > e:
        xk = xk1
        xk1 = xk1 - f(xk1) / dir(xk1)
        conv_list.append(xk1)

    n = list(range(len(conv_list)))
    plt.figure()
    subplot1(111, n, conv_list, n, [conv_list[-1] for _ in range(len(n))], 'Сходимость метода Ньютона')


    return xk1


def main():
    plt.figure()
    subplot(111, gen_dots(), list(map(f, gen_dots())), 'График')

    #блок дихотомии
    dih_block(3)
    dih_block(6)
    dih_block(9)

    #блок Ньютона
    newton_block(3)
    newton_block(6)
    newton_block(9)

    #блок хорд
    chord_block(3)
    chord_block(6)
    chord_block(9)

    #блок модифицированного мтеода хорд
    chord_mod_block(3)
    chord_mod_block(6)
    chord_mod_block(9)

    print('-------------------------------------------------')
    print('Cкорость сходимости дихотомии: {}'.format(dih_speed(dih(10 ** (-15)))))
    print('-------------------------------------------------')
    print('Cкорость сходимости метода Ньютона: {}'.format(newton_speed(newton(10 ** (-15)))))
    print('-------------------------------------------------')
    print('Cкорость сходимости метода хорд: {}'.format(chord_speed(chord(10 ** (-15)))))
    print('-------------------------------------------------')
    print('Cкорость сходимости модифицированного метода хорд: {}'.format(chord_mod_speed(chord_mod(10 ** (-15)))))
    print('-------------------------------------------------')

    dop(10 ** (-9))

    plt.show()


if __name__ == '__main__':
    main()
