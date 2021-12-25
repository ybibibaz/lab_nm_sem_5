import math
import matplotlib.pyplot as plt


U0 = 1
U10 = 0
A = 0
B = 1


def true_u(x):

    return (1 + x) ** (1 / 2) * math.sin(x) + math.exp(-x)


def euler_f(x, w, u):

    return -1 / (2 * ( x + 1)) * w + (1 + 2 * x) / (2 * (x + 1)) * u + (3 * math.cos(x) - (3 + 4 * x) * math.sin(x)) / (2 * math.sqrt(1 + x))


#метод Эйлера(O(h))
def euler(h):
    w = [U10]
    u = [U0]
    for i in range(1, int(1 // h) + 2):
        hi = h * i
        u.append(u[i - 1] + h * w[i - 1])
        w.append(w[i - 1] + h * euler_f(hi, w[i - 1], u[i - 1]))

    return u


#метод Рунге-Кутты(O(h**4))
def runge(h):
    w = [U10]
    u = [U0]
    for i in range(1, int(1 // h) + 2):
        hi = h * (i - 1)
        k1 = euler_f(hi, w[i - 1], u[i - 1])
        q1 = w[i - 1]
        k2 = euler_f(hi + h / 2, w[i - 1] + h * k1 / 2, u[i - 1] + h * q1 / 2)
        q2 = w[i - 1] + h * k1 / 2
        k3 = euler_f(hi + h / 2, w[i - 1] + h * k2 / 2, u[i - 1] + h * q2 / 2)
        q3 = w[i - 1] + h * k2 / 2
        k4 = euler_f(hi + h, w[i - 1] + h * k3, u[i - 1] + h * q3)
        q4 = w[i - 1] + h * k3
        w.append(w[i - 1] + (k1 + 2 * (k2 + k3) + k4) * h / 6)
        u.append(u[i - 1] + (q1 + 2 * (q2 + q3) + q4) * h / 6)

    return u


#метод Адамса(O(h**3))
def adams(h):
    w = [U10]
    u = [U0]
    for i in range(1, 3):
        hi = h * (i - 1)
        k1 = euler_f(hi, w[i - 1], u[i - 1])
        q1 = w[i - 1]
        k2 = euler_f(hi + h / 2, w[i - 1] + h * k1 / 2, u[i - 1] + h * q1 / 2)
        q2 = w[i - 1] + h * k1 / 2
        k3 = euler_f(hi + h / 2, w[i - 1] + h * k2 / 2, u[i - 1] + h * q2 / 2)
        q3 = w[i - 1] + h * k2 / 2
        k4 = euler_f(hi + h, w[i - 1] + h * k3, u[i - 1] + h * q3)
        q4 = w[i - 1] + h * k3
        w.append(w[i - 1] + (k1 + 2 * (k2 + k3) + k4) * h / 6)
        u.append(u[i - 1] + (q1 + 2 * (q2 + q3) + q4) * h / 6)
    for i in range(3, int(1 // h) + 2):
        hi = h * i
        u.append(u[i - 1] + h * (23 / 12 * w[i - 1] - 16 / 12 * w[i - 2] + 5 / 12 * w[i - 3]))
        w.append(w[i - 1] + h * (23 / 12 * euler_f(hi - h , w[i - 1], u[i - 1]) - 16 / 12 * euler_f(hi - h * 2, w[i - 2], u[i - 2]) + 5 / 12 * euler_f(hi - h * 3, w[i - 3], u[i - 3])))

    return u


def subplot(pos, x, y, x1, y1, title):
    plt.subplot(pos)
    plt.plot(x, y, 'r')
    plt.plot(x1, y1, 'b')
    plt.title(title)
    plt.grid(True)
    ax = plt.gca()
    ax.axhline(y=0, color='k')
    ax.axvline(x=0, color='k')


def subplot1(pos, x, y, title):
    plt.subplot(pos)
    plt.plot(x, y, 'r')
    plt.title(title)
    plt.grid(True)
    ax = plt.gca()
    ax.axhline(y=0, color='k')
    ax.axvline(x=0, color='k')


def main_fix_step(h=0.05):
    dots = [h * i for i in range(int((B - A) // h) + 2)]
    values = list(map(true_u, dots))
    eulers = euler(h)
    adamss = adams(h)
    runges = runge(h)

    eulers1 = euler(2 * h)
    adamss1 = adams(2 * h)
    runges1 = runge(2 * h)
    euler_err_list = []
    adams_err_list = []
    runge_err_list = []
    euler_err_list1 = []
    adams_err_list1 = []
    runge_err_list1 = []
    for i in range(len(eulers1)):
        euler_err_list.append(abs(eulers[i * 2] - eulers1[i]))
        adams_err_list.append(abs(adamss[i * 2] - adamss1[i]) / 7)
        runge_err_list.append(abs(runges[i * 2] - runges1[i]) / 15)
    for i in range(len(values)):
        euler_err_list1.append(abs(eulers[i] - values[i]))
        adams_err_list1.append(abs(adamss[i] - values[i]))
        runge_err_list1.append(abs(runges[i] - values[i]))
    dots1 = [2 * h * i for i in range(int((B - A) // (2 * h) + 2))]
    #values1 = list(map(true_u, dots1))
    plt.figure()
    subplot1(334, dots1, euler_err_list, 'Метод Эйлера, поправка Рунге')
    subplot1(335, dots1, adams_err_list, 'Метод Адамса, поправка Рунге')
    subplot1(336, dots1, runge_err_list, 'Метод Рунге-Кутты, поправка Рунге')

    subplot(331, dots, values, dots, eulers, 'Метод Эйлера')
    subplot(332, dots, values, dots, adamss, 'Метод Адамса')
    subplot(333, dots, values, dots, runges, 'Метод Рунге-Кутты')

    subplot1(337, dots, euler_err_list1, 'Метод Эйлера, ошибка')
    subplot1(338, dots, adams_err_list1, 'Метод Адамса, ошибка')
    subplot1(339, dots, runge_err_list1, 'Метод Рунге-Кутты, ошибка')

    plt.show()


def main():
    step_list = []
    euler_list = []
    adams_list = []
    runge_list = []
    euler_list_rung = []
    adams_list_rung = []
    runge_list_rung = []
    for n in range(20, 200, 2):
        h = (B - A) / n
        step_list.append(h)
        eulers = euler(h)
        adamss = adams(h)
        runges = runge(h)

        eulers1 = euler(2 * h)
        adamss1 = adams(2 * h)
        runges1 = runge(2 * h)
        true_value = [true_u(h * i) for i in range(len(eulers))]
        length = min(len(eulers) // 2, len(eulers1))
        euler_runge_range = [eulers[2 * i] - eulers1[i] for i in range(length)]
        adams_runge_range = [(adamss[2 * i] - adamss1[i]) / 7 for i in range(length)]
        runge_runge_range = [(runges[2 * i] - runges1[i]) / 15 for i in range(length)]
        euler_list.append(max([abs(true_value[i] - eulers[i]) for i in range(len(eulers))]))
        adams_list.append(max([abs(true_value[i] - adamss[i]) for i in range(len(eulers))]))
        runge_list.append(max([abs(true_value[i] - runges[i]) for i in range(len(eulers))]))
        euler_after_runge = [eulers[2 * i] + euler_runge_range[i] for i in range(length)]
        adams_after_runge = [adamss[2 * i] + adams_runge_range[i] for i in range(length)]
        runge_after_runge = [runges[2 * i] + runge_runge_range[i] for i in range(length)]
        euler_list_rung.append(max([abs(true_value[2 * i] - euler_after_runge[i]) for i in range(length)]))
        adams_list_rung.append(max([abs(true_value[2 * i] - adams_after_runge[i]) for i in range(length)]))
        runge_list_rung.append(max([abs(true_value[2 * i] - runge_after_runge[i]) for i in range(length)]))


    plt.figure()

    subplot(131, list(map(math.log, step_list)), list(map(math.log, euler_list)), list(map(math.log, step_list)), list(map(math.log, euler_list_rung)), 'Метод Эйлера (логарифм)')
    plt.legend(['before_runge', 'after_runge'])
    plt.ylim((-11, -2))
    plt.xlim((-6, -2))
    subplot(132, list(map(math.log, step_list)), list(map(math.log, adams_list)), list(map(math.log, step_list)), list(map(math.log, adams_list_rung)), 'Метод Адамса (логарифм)')
    plt.legend(['before_runge', 'after_runge'])
    plt.ylim((-25, -10))
    plt.xlim((-6, -2))
    subplot(133, list(map(math.log, step_list)), list(map(math.log, runge_list)), list(map(math.log, step_list)), list(map(math.log, runge_list_rung)), 'Метод Рунге-Кутты (логарифм)')
    plt.legend(['before_runge', 'after_runge'])
    plt.ylim((-35, -15))
    plt.xlim((-6, -2))

    plt.show()


if __name__ == '__main__':
    main_fix_step()
    #зависимость от шага
    main()
