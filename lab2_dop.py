# -*- coding: utf-8 -*-
import math
import matplotlib.pyplot as plt


A = -0.8
B = 0.8


# исходная функция
def f(x):

    return math.sin(x) * math.exp(-x)


def der_3(x):

    return 2 * (math.sin(x) + math.cos(x)) * math.exp(-x)


def gen_dots(H):

    return [A + H * i for i in range(int((B - A) // H + 1))]


def third_der_2(values, H):
    ans = []
    values1 = [f(A - H * 2), f(A - H)]
    values1.extend(values)
    values1.append(f(B + H))
    values1.append(f(B + 2 * H))
    for i in range(len(values)):
        ans.append((-values1[i] + 2 * values1[i + 1] - 2 * values1[i + 3] + values1[i + 4]) / (2 * H ** 3))

    return ans


def main():
    H = 0.01
    dots = gen_dots(H)
    values = list(map(f, dots))
    true_der_3 = list(map(der_3, dots))

    #task1(3-rd der plot)
    _third_der = third_der_2(values, H)
    plt.figure()
    plt.subplot(221)
    plt.plot(dots, true_der_3, 'r', dots, _third_der, 'b')
    plt.title('3-rd der')
    plt.grid(True)

    _t_d_diff = []
    for i in range(len(_third_der)):
        _t_d_diff.append(abs(_third_der[i] - true_der_3[i]))

    #task2(3-rd der diff)
    plt.subplot(222)
    plt.plot(dots, _t_d_diff, 'r')
    plt.title('3-rd der diff')
    plt.grid(True)

    #task3(log diff)
    H_list = []
    diff_list = []
    for i in range(16):
        H = 0.1 + i * 0.1
        H_list.append(H)
        dots = gen_dots(H)
        values = list(map(f, dots))
        true_der_3 = list(map(der_3, dots))
        _third_der = third_der_2(values, H)
        _t_d_diff = []
        for j in range(len(_third_der)):
            _t_d_diff.append(abs(_third_der[j] - true_der_3[j]))

        diff_list.append(max(_t_d_diff))
        #print(H, max(_t_d_diff))
        #print(math.log(H), math.log(max(_t_d_diff)))

    plt.subplot(212)
    plt.plot(list(map(math.log, H_list)), list(map(math.log, diff_list)), 'r')
    plt.title('log diff')
    plt.grid(True)


    plt.show()


if __name__ == '__main__':
    main()
