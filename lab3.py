import math
import matplotlib.pyplot as plt


A = -1
B = 1


def gen_steps():
    ans = []
    param = 100
    for i in range(1, (B - A) * param + 1):
        if (B - A) * param % i == 0:
            ans.append(i / param)

    return ans

def gen_dots(step):
    item = A
    dots = []
    while item <= B:
        dots.append(item)
        item = round(step + item, 5)

    return dots


#function
def f(x):

    return 1 / (2 * x ** 2 + 1)
    #return math.exp(x**2)


#integral
def int():

    return math.sqrt(2) * math.atan(math.sqrt(2))


#rectangle(O(h**1))
def rectangle(values, dots, step):
    ans = 0
    for i in range(len(values) - 2):
        ans += values[i + 1] * step

    return ans


#trapeze(O(h**2))
def trapeze(values, step):
    ans = 0
    for i in range(len(values) - 1):
        ans += (values[i + 1] + values[i]) * step / 2

    return ans


#simpson(O(h**4))
def simpson(values, dots, step):
    ans = 0
    '''if len(values) // 2 != 0:
        for i in range((len(values) - 1)// 2):
            ans += (values[i * 2] + values[i * 2 + 2] + 4 * values[i * 2 + 1]) * step / 3

        return ans'''
    for i in range(len(values) - 1):
        ans += (values[i] + values[i + 1] + 4 * f(dots[i] + step / 2)) * step / 6

    return ans


#Gauss(O(h**6))
def gauss(dots):
    c1 = 5 / 9
    c2 = 8 / 9
    c3 = 5 / 9
    x1 = math.sqrt(0.6)
    x2 = 0
    x3 = -math.sqrt(0.6)
    ans = 0
    for i in range(len(dots) - 1):
        norm1 = (dots[i + 1] - dots[i]) / 2 #масштаб (отношение длины отрезка к длине [-1, 1])
        norm2 = (dots[i + 1] + dots[i]) / 2 #смещение (середина отрезка)
        ans += norm1 * (c1 * f(norm2 + norm1 * x1) + c2 * f(norm2 + norm1 * x2) + c3 * f(norm2 + norm1 * x3))
    return ans


def main(step_list):
    rectangle_list = []
    trapeze_list = []
    simpson_list = []
    gauss_list = []
    rectangle_list_value = []
    trapeze_list_value = []
    simpson_list_value = []
    gauss_list_value = []
    for step in step_list:
        dots = gen_dots(step)
        values = list(map(f, dots))
        true_int = int()
        rectangle_int = rectangle(values, dots, step)
        trapeze_int = trapeze(values, step)
        simpson_int = simpson(values, dots, step)
        gauss_int = gauss(dots)
        rectangle_list_value.append(rectangle_int)
        trapeze_list_value.append(trapeze_int)
        simpson_list_value.append(simpson_int)
        gauss_list_value.append(gauss_int)
        rectangle_list.append(abs(true_int - rectangle_int))
        trapeze_list.append(abs(true_int - trapeze_int))
        simpson_list.append(abs(true_int - simpson_int))
        gauss_list.append(max(abs(true_int - gauss_int), 1e-17))

    plt.figure()
    plt.subplot(331)
    plt.plot(step_list, [int() for i in range(len(step_list))], 'r', step_list, rectangle_list_value, 'b')
    plt.title('rectangle_int')
    plt.grid(True)
    plt.subplot(332)
    plt.plot(step_list, [int() for i in range(len(step_list))], 'r', step_list, trapeze_list_value, 'b')
    plt.title('trapeze_int')
    plt.grid(True)
    plt.subplot(333)
    plt.plot(step_list, [int() for i in range(len(step_list))], 'r', step_list, simpson_list_value, 'b')
    plt.title('simpson_int')
    plt.grid(True)
    plt.subplot(334)
    plt.plot(step_list, rectangle_list, 'b')
    plt.title('rectangle_int_error')
    plt.grid(True)
    plt.subplot(335)
    plt.plot(step_list, trapeze_list, 'b')
    plt.title('trapeze_int_error')
    plt.grid(True)
    plt.subplot(336)
    plt.plot(step_list, simpson_list, 'b')
    plt.title('simpson_int_error')
    plt.grid(True)
    plt.subplot(337)
    plt.plot(list(map(math.log, step_list)), list(map(math.log, rectangle_list)), 'b')
    plt.title('rectangle_log_error')
    plt.grid(True)
    plt.subplot(338)
    plt.plot(list(map(math.log, step_list)), list(map(math.log, trapeze_list)), 'b')
    plt.title('trapeze_log_error')
    plt.grid(True)
    plt.subplot(339)
    plt.plot(list(map(math.log, step_list)), list(map(math.log, simpson_list)), 'b')
    plt.title('simpson_log_error')
    plt.grid(True)
    plt.figure()
    plt.subplot(131)
    plt.plot(step_list, [int() for i in range(len(step_list))], 'r', step_list, gauss_list_value, 'b')
    plt.title('gauss_int')
    plt.grid(True)
    plt.subplot(132)
    plt.plot(step_list, gauss_list, 'b')
    plt.title('gauss_int_error')
    plt.grid(True)
    plt.subplot(133)
    print(step_list)
    print(gauss_list)
    plt.plot(list(map(math.log, step_list)), list(map(math.log, gauss_list)), 'b')
    plt.title('gauss_log_error')
    plt.grid(True)

    #блок с принтами

    '''
    print('errors for steps {}'.format(step_list))
    print('rectangle error: {}'.format(rectangle_list))
    print('trapeze error: {}'.format(trapeze_list))
    print('simpson error: {}'.format(simpson_list))
    print('gauss error: {}'.format(gauss_list))
    '''


    plt.show()


if __name__ == '__main__':
    step_list = gen_steps()
    step_list.pop()
    step_list.pop()
    step_list.pop()
    step_list.pop()
    step_list.pop()
    main(step_list)
    #main([0.03])
