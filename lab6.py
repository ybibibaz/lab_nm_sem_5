import math
import matplotlib.pyplot as plt


params = {'A1': 1, 'B1': 0, 'C1': 1, 'A2': 1, 'B2': -2, 'C2': 0.1704}


def real_solution(x):

    return (1 + x) ** (1 / 2) * math.sin(x) + math.exp(-x)


def gen_dots(h):
    ans = []
    i = 0
    while h * i <= 1:
        ans.append(h * i)
        i += 1

    return ans


def p(x):

    return 1 / (2 * (1 + x))


def q(x):

    return -(1 + 2 * x) / (2 * (1 + x))


def f(x):

    return (3 * math.cos(x) - (3 + 4 * x) * math.sin(x)) / (2 * math.sqrt(1 + x))


def progonka_forward(a, b, c, f_):
    a_forward = [-c[0] / b[0]]
    b_forward = [f_[0] / b[0]]
    for i in range(1, len(a)):
        a_forward.append(-c[i] / (b[i] + a[i] * a_forward[i - 1]))
        b_forward.append((f_[i] - a[i] * b_forward[i - 1]) / (b[i] + a[i] * a_forward[i - 1]))

    return a_forward, b_forward


def progonka_backward(a, b):
    y = [b[0]]
    for i in range(1, len(b)):
        y.append(b[i] + a[i] * y[i - 1])

    return y


def progonka(a, b, c, f_):
    a_forward, b_forward = progonka_forward(a, b, c, f_)
    a_forward.reverse()
    b_forward.reverse()
    y = progonka_backward(a_forward, b_forward)
    y.reverse()

    return y


def prec_1(h):
    dots = gen_dots(h)
    a = [0]
    b = [params['A1'] - params['B1'] / h]
    c = [params['B1'] / h]
    f_ = [params['C1']]
    for items in dots[1:len(dots) - 1]:
        a.append(1 / h ** 2 - p(items) / (2 * h))
        b.append(-2 / h ** 2 + q(items))
        c.append(1 / h ** 2 + p(items) / (2 * h))
        f_.append(f(items))
    a.append(-params['B2'] / h)
    b.append(params['A2'] + params['B2'] / h)
    c.append(0)
    f_.append(params['C2'])
    y = progonka(a, b, c, f_)

    return y


def prec_2(h):
    dots = gen_dots(h)
    a0 = 0
    b0 = params['A1'] - params['B1'] / h
    c0 = params['B1'] / h
    f_0 = params['C1']
    an = -params['B2'] / h
    bn = params['A2'] + params['B2'] / h
    cn = 0
    f_n = params['C2']
    a = []
    b = []
    c = []
    f_ = []
    if params['B1'] != 0:
        b0 = -2 + 2 * h * params['A1'] / params['B1'] - p(dots[0]) * h ** 2 * params['A1'] / params['B1'] + q(dots[0]) * h ** 2
        c0 = 2
        f_0 = f(dots[0]) * h ** 2 + 2 * params['C1'] * h / params['B1'] - p(dots[0]) * h ** 2 * params['C1'] / params['B1']

    if params['B2'] != 0:
        an = 2
        bn = -2 + (-2) * h * params['A2'] / params['B2'] - p(dots[-1]) * h ** 2 * params['A2'] / params['B2'] + q(dots[-1]) * h ** 2
        f_n = f(dots[-1]) * h ** 2 - (2 * h * params['C2'] / params['B2'] + p(dots[-1]) * h ** 2 * params['C2'] / params['B2'])
    a.append(a0)
    b.append(b0)
    c.append(c0)
    f_.append(f_0)
    for items in dots[1:len(dots) - 1]:
        a.append(1 / h ** 2 - p(items) / (2 * h))
        b.append(-2 / h ** 2 + q(items))
        c.append(1 / h ** 2 + p(items) / (2 * h))
        f_.append(f(items))
    a.append(an)
    b.append(bn)
    c.append(cn)
    f_.append(f_n)
    y = progonka(a, b, c, f_)

    return y


def graph_for_task_1(x, y1, y2, real):
    plt.figure()
    plt.subplot(311)
    plt.plot(x, y1, 'r')
    plt.plot(x, y2, 'b')
    plt.plot(x, real, 'g')
    plt.legend(['h', 'h^2', 'real'])
    plt.grid(True)
    plt.title('Графики функции и численных решений')
    plt.subplot(312)
    plt.plot(x, list(abs(real[i] - y1[i]) for i in range(len(real))), 'r')
    plt.grid(True)
    plt.title('График ошибки решения первого порядка точности')
    plt.subplot(313)
    plt.plot(x, list(abs(real[i] - y2[i]) for i in range(len(real))), 'r')
    plt.grid(True)
    plt.title('График ошибки решения второго порядка точности')


def log_graph(error1, error2, steps):
    plt.figure()
    error1 = list(map(math.log, error1))
    error2 = list(map(math.log, error2))
    steps = list(map(math.log, steps))
    plt.subplot(111)
    plt.plot(steps, error1, 'r', steps, error2, 'b')
    plt.text(steps[0], error1[0], 'tg = {0:.4}'.format((error1[-1] - error1[0]) / (steps[-1] - steps[0])))
    plt.text(steps[0], error2[0],'tg = {0:.5}'.format((error2[-1] - error2[0]) / (steps[-1] - steps[0])))
    plt.title('Зависимость логарифма ошибки от логарифма шага')
    plt.legend(['h', 'h^2'])
    plt.grid(True)


def max_error(y, real):
    ans = 0
    for i in range(len(y)):
        if abs(y[i] - real[i]) > ans:
            ans = abs(y[i] - real[i])

    return ans


def runge(h):
    y_h = prec_2(h)
    y_2h = prec_2(h * 2)
    length = len(y_2h)
    runge_diff = [(y_h[i * 2] - y_2h[i]) / 3 for i in range(length)]
    after_runge = [y_h[2 * i] + runge_diff[i] for i in range(length)]

    return after_runge


def main():
    #task1
    h = 0.05
    dots = gen_dots(h)
    y1 = prec_1(h)
    y2 = prec_2(h)
    real = list(map(real_solution, dots))
    graph_for_task_1(dots, y1, y2, real)
    #task2
    error_list_1 = []
    error_list_2 = []
    step_list = []
    for n in range(20, 60):
        h = 1 / n
        dots = gen_dots(h)
        y1 = prec_1(h)
        y2 = prec_2(h)
        real = list(map(real_solution, dots))
        error_list_1.append(max_error(y1, real))
        error_list_2.append(max_error(y2, real))
        step_list.append(h)
    log_graph(error_list_1, error_list_2, step_list)


def task_3():
    before_runge_error = []
    after_runge_error = []
    step_list = []
    for n in range(2, 10, 2):
        h = 1 / n
        dots = gen_dots(h)
        y_h = prec_2(h)
        y_2h = prec_2(h * 2)
        real = list(map(real_solution, dots))
        before_runge_error.append(max([abs(real[i] - y_h[i]) for i in range(len(real))]))
        after_runge = runge(h)
        after_runge_error.append(max([abs(real[i * 2] - after_runge[i]) for i in range(len(after_runge))]))
        step_list.append(h)
    plt.figure()
    plt.subplot(121)
    step_list = list(map(math.log, step_list))
    after_list = list(map(math.log, after_runge_error))
    before_list = list(map(math.log, before_runge_error))
    diff = before_list[-1] - after_list[-1]
    for i in range(len(after_list)):
        after_list[i] += diff
    plt.plot(step_list, after_list, 'r')
    plt.plot(step_list, before_list, 'b')
    plt.title('Второй и третий порядок')
    plt.legend(['after_runge', 'before_runge'])
    plt.grid(True)


    h = 0.01
    dots = gen_dots(h)
    y_h = prec_2(h)
    real = list(map(real_solution, dots))
    after_runge = runge(h)
    plt.subplot(122)
    plt.plot(dots, real, 'r', dots[::2], after_runge, dots, y_h, 'g')
    plt.title('Решения второго и третьего порядка(шаг 0.01)')
    plt.legend(['real', 'after_runge', 'before_runge'])
    plt.grid(True)


    plt.show()


if __name__ == '__main__':
    main()
    task_3()
