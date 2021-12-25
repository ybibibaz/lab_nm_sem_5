# -*- coding: utf-8 -*-
import math
import matplotlib.pyplot as plt


A = -0.8
B = 0.8


# исходная функция
def f(x):
    return math.sin(x) * math.exp(-x)


# первая производная
def der_1(x):
    return -f(x) + math.cos(x) * math.exp(-x)


# вторая производная
def der_2(x):
    return -der_1(x) -f(x) - math.cos(x) * math.exp(-x)


def gen_dots(H):
    return [A + H * i for i in range(int((B - A) // H + 1))]


def first_der(values, H):
    ans = []
    if H <= 0.8:
        for i in range(len(values)):
            if i == 0:
                ans.append((4 * values[i + 1] - 3 * values[i] - values[i + 2]) / (2 * H))
            elif i == len(values) - 1:
                ans.append((values[i - 2] - 4 * values[i - 1] + 3 * values[i]) / (2 * H))
            else:
                ans.append((values[i + 1] - values[i - 1]) / (2 * H))
    else:
        ans = [(values[1] - values[0]) / 2, (values[1] - values[0]) / 2]

    return ans


def second_der_2(values, H):
    ans = []
    values1 = [f(A - H)]
    values1.extend(values)
    values1.append(f(B + H))
    for i in range(len(values)):
        ans.append((values1[i] - 2 * values1[i + 1] + values1[i + 2]) / H ** 2)

    return ans


def second_der_4(values, H):
    ans = []
    values1 = [f(A - 2 * H), f (A - H)]
    values1.extend(values)
    values1.append(f(B + H))
    values1.append(f(B + 2 * H))
    for i in range(len(values)):
        ans.append((-values1[i] + 16 * values1[i + 1] - 30 * values1[i + 2] + 16 * values1[i + 3] - values1[i + 4]) / (12 * H ** 2))

    return ans


def main():
    H = 0.1
    dots = gen_dots(H)
    values = list(map(f, dots))
    true_der_1 = list(map(der_1, dots))
    true_der_2 = list(map(der_2, dots))

    _first_der = first_der(values, H)
    plt.figure()
    plt.subplot(221)
    plt.plot(dots, true_der_1, 'r', dots, _first_der, 'b')
    plt.title('1-st der')

    _second_der_2 = second_der_2(values, H)
    plt.subplot(222)
    plt.plot(dots, true_der_2, 'r', dots, _second_der_2, 'b')
    plt.title('2-nd der(2)')

    _second_der_4 = second_der_4(values, H)
    plt.subplot(212)
    plt.plot(dots, true_der_2, 'r', dots, _second_der_4, 'b')
    plt.title('2-nd der(4)')

    _f_d_diff = []
    for i in range(len(_first_der)):
        _f_d_diff.append(abs(_first_der[i] - true_der_1[i]))

    _s_d_diff2 = []
    for i in range(len(_second_der_2)):
        _s_d_diff2.append(abs(_second_der_2[i] - true_der_2[i]))

    _s_d_diff4 = []
    for i in range(len(_first_der)):
        _s_d_diff4.append(abs(_second_der_4[i] - true_der_2[i]))


    plt.figure()
    plt.subplot(221)
    plt.plot(dots, _f_d_diff, 'r')
    plt.title('1-st der diff')
    plt.subplot(222)
    plt.plot(dots, _s_d_diff2, 'r')
    plt.title('2-nd der(2) diff')
    plt.subplot(212)
    plt.plot(dots, _s_d_diff4, 'r')
    plt.title('2-nd der(4) diff')

    diff_list1 = []
    diff_list2 = []
    diff_list3 = []
    H_list = []

    for i in range(80):
        H = 0.02 + i * 0.02
        H_list.append(H)
        dots = gen_dots(H)
        values = list(map(f, dots))
        true_der_1 = list(map(der_1, dots))
        true_der_2 = list(map(der_2, dots))
        _first_der = first_der(values, H)
        _second_der_2 = second_der_2(values, H)
        _second_der_4 = second_der_4(values, H)
        _f_d_diff = []
        for i in range(len(_first_der)):
            _f_d_diff.append(abs(_first_der[i] - true_der_1[i]))

        _s_d_diff2 = []
        for i in range(len(_second_der_2)):
            _s_d_diff2.append(abs(_second_der_2[i] - true_der_2[i]))

        _s_d_diff4 = []
        for i in range(len(_first_der)):
            _s_d_diff4.append(abs(_second_der_4[i] - true_der_2[i]))

        diff_list1.append(max(_f_d_diff))
        diff_list2.append(max(_s_d_diff2))
        diff_list3.append(max(_s_d_diff4))

    print(H_list)
    print(diff_list1)
    print(diff_list2)
    print(diff_list3)
    plt.figure()
    plt.subplot(221)
    plt.plot(list(map(math.log, H_list)), list(map(math.log, diff_list1)), 'r')
    plt.title('1-st der diff log')
    plt.subplot(222)
    plt.plot(list(map(math.log, H_list)), list(map(math.log, diff_list2)), 'r')
    plt.title('2-nd der(2) diff log')
    plt.subplot(212)
    plt.plot(list(map(math.log, H_list)), list(map(math.log, diff_list3)), 'r')
    plt.title('2-nd der(4) diff log')
    plt.figure()
    ananas = []
    for items in dots:
        ananas.append(math.sin(items) * math.exp(-items))
    plt.plot(dots, ananas)
    plt.show()


if __name__ == '__main__':
    main()