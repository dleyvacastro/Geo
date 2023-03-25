import numpy as np
from matplotlib.animation import FuncAnimation
from IPython import display
import matplotlib.pyplot as plt

# f = (2,5)
# a, b = f
lim = 25
points = [np.random.randint(-lim + 1, lim, 2) for i in range(7)]
f = lambda x, a, b, c: (x ** 2 - 2 * a * x + a ** 2 + b ** 2 - c ** 2) / (2 * b - 2 * c)


def beachLinePlotter(c, points):
    # remove all points bellow c

    points = [p for p in points if p[1] > c]

    x = {i: [] for i in np.linspace(-lim, lim, 100).tolist()}

    for p in points:
        a, b = p
        plt.plot(p[0], p[1], 'ro')
        xtmp = np.linspace(a - 7, a + 7, 100)
        ytmp = f(xtmp, a, b, c)
        # light gray plot
        plt.plot(xtmp, ytmp, 'k--', alpha=0.2)
        for i in x:
            x[i].append(f(i, a, b, c))

    y = [min(x[i]) for i in x]
    x = np.linspace(-lim, lim, 100).tolist()
    plt.plot(x, y)
    plt.plot(x, np.ones(len(x)) * c, 'r')
    plt.grid("on")
    # regular lim axis
    plt.xlim(-lim, lim)
    plt.ylim(-lim, lim)
    plt.show()


beachLinePlotter(10, points)
beachLinePlotter(0, points)
beachLinePlotter(-10, points)
beachLinePlotter(-lim, points)

# x = np.linspace(-10, 10, 1)
# y = f(x)
#
# plt.plot(x, y)
# plt.plot(a, b, 'ro')
# plt.plot(x, np.ones(len(x))*c, 'r')
# plt.grid("on")
# plt.show()
