import math
import matplotlib.pyplot as plt


# исходная функция
def f(x):
    return math.sin(math.exp(x / 2) / 35)


a = 0
b = 10
h = 0.25
n_chebyshev = 80
args = [h * i for i in range(int(b // h))]
values = list(map(f, args))


# массив узлов Чебышева
def cheb_args(n):
    reversed_ans = [(a + b) / 2 + (b - a) / 2 * math.cos(math.pi * (2 * k + 1) / (2 * n)) for k in range(n)]

    return reversed_ans[::-1]


def term(x, k, argss=args):
    ans = 1
    for i in range(len(argss)):
        if i != k:
            ans *= (x - argss[i]) / (argss[k] - argss[i])

    return ans


def polynomial(x, argss=args, valuess=values):
    ans = 0
    for i in range(len(argss)):
        ans += valuess[i] * term(x, i, argss)

    return ans


# a
new_args = list(map(lambda x: x + h / 2, args))
new_values = list(map(polynomial, new_args))

# print(args)
# print(values)
# print(new_args)
# print(new_values)

# b
new_args1 = cheb_args(n_chebyshev)
new_values1 = list(map(polynomial, new_args1))

# print(new_args1)
# print(new_values1)
plt.figure()
plt.subplot(221)
plt.plot(args, values, 'r', new_args, new_values, 'b')
plt.title('Равномерный шаг')
plt.subplot(222)
plt.plot(args, values, 'r',  new_args1, new_values1, 'b')
plt.title('Узлы Чебышева')
plt.subplot(223)
plt.plot(new_args, [list(map(f, new_args))[i] - new_values[i] for i in range(len(new_args))], 'r')
plt.title('Погрешность равномерного шага')
plt.subplot(224)
plt.plot(new_args1, [list(map(f, new_args1))[i] - new_values1[i] for i in range(len(new_args1))], 'r')
plt.title('Погрешность узлов Чебышева')
plt.show()

# оптимальное кол-во точек для равномерного шага
opt_error = math.inf
opt_count = 0
for i in range(2, 101):
    step = (b - a) / i
    opt_args = [a + step * j for j in range(i)]
    opt_values = list(map(f, opt_args))
    new_opt_args = list(map(lambda x: x + step / 2, opt_args))
    new_opt_values = []
    for k in range(len(new_opt_args)):
        new_opt_values.append(polynomial(new_opt_args[k], argss=opt_args, valuess=opt_values))
    perf_values = list(map(f, new_opt_args))
    error = sum(list(map(lambda x, y: abs(x - y) ** 2, new_opt_values, perf_values))) / i
    print(error)
    if error < opt_error:
        opt_error = error
        opt_count = i

# оптимальное количество узлов
print(opt_count)
