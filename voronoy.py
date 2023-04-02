import numpy as np
from matplotlib.animation import FuncAnimation
from IPython import display
import matplotlib.pyplot as plt
import gif
import json


def pointManager(lim, n, rand):
    if rand:
        points = [np.random.randint(-lim + 1, lim, 2).tolist() for i in range(n)]
        # save into a json file, with indent
        with open("points.json", "w") as f:
            json.dump(points, f, indent=4)
    else:
        with open("points.json", "r") as f:
            points = json.load(f)
    return points


# f = (2,5)
# a, b = f
lim = 10
n = 10
points = pointManager(lim, n, rand=0)

f = lambda x, a, b, c: (x ** 2 - 2 * a * x + a ** 2 + b ** 2 - c ** 2) / (2 * b - 2 * c)


class Parabola:
    def __init__(self, p, c, lim):
        self.p = p
        self.a = p[0]
        self.b = p[1]
        self.c = c
        self.lim = lim
        self.x = np.linspace(-self.lim, self.lim, 100)
        self.y = f(self.x, self.a, self.b, self.c)
        self.f = lambda x: (x ** 2 - 2 * self.a * x + self.a ** 2 + self.b ** 2 - self.c ** 2) / (
                    2 * self.b - 2 * self.c)

    def plot(self, color='b'):
        plt.plot(self.x, self.y, color, alpha=0.5)

class Beachline:
    def __init__(self):
        self.beachline = [() for i in range(len(np.linspace(-lim, lim, 100)))]

    def detectIntersections(self):
        index = []
        intersections = []
        for i in range(len(self.beachline)-1):
            if self.beachline[i][1] != self.beachline[i + 1][1]:
                index.append(i)
                intersections.append((self.beachline[i][0]+self.beachline[i + 1][0])/2)

        return index, intersections






class Voronoi:
    def __init__(self, points, lim):
        self.currBeachLine2 = None
        self.points = points
        self.lim = lim
        self.linspace = np.linspace(-lim, lim, 100)
        self.nonActive = []
        self.currBeachLine = np.inf * np.ones(len(self.linspace))


    @gif.frame
    def beachLineP(self, c):
        print(len(self.currBeachLine))
        self.currBeachLine2 = Beachline()
        plt.grid("on")
        # regular lim axis
        plt.xlim(-lim - 1, lim + 1)
        plt.ylim(-lim, lim)

        # plot bizectriz
        plt.plot(self.linspace, np.ones(len(self.linspace)) * c, 'r')
        active = [p for p in self.points if p[1] > c and p not in self.nonActive]
        plt.plot([i[0] for i in active], [i[1] for i in active], 'or')
        plt.plot([i[0] for i in self.points if i not in active], [i[1] for i in self.points if i not in active], 'ok')
        if len(active) == 0:
            return

        for i in active:
            
            par = Parabola(i, c, lim)
            isactive = False  # suppose it is not active
            par.plot('k--')
            for j in range(len(par.y)):
                if par.y[j] < self.currBeachLine[j]:
                    self.currBeachLine[j] = par.y[j]
                    self.currBeachLine2.beachline[j] = (par.y[j], i)

                    isactive = True  # if it has a point in the beach line, it is active
            if not isactive:
                self.nonActive.append(i)

        index, intersections = self.currBeachLine2.detectIntersections()
        xi = []
        tmp = self.linspace.tolist()
        for i in index:
            xi.append(tmp[i])

        plt.plot(xi, intersections, 'go')

        plt.plot(self.linspace, self.currBeachLine, 'b')

    def beachLine(self, c):
        # remove all points bellow c
        print(len(self.currBeachLine))
        plt.plot([i[0] for i in self.points], [i[1] for i in self.points], 'ok')
        points = [p for p in self.points if p[1] > c and p not in self.nonActive]
        if len(points) == 0:
            return

        x = {i: [] for i in np.linspace(-lim, lim, 1000).tolist()}

        for p in points:
            a, b = p
            plt.plot(p[0], p[1], 'ro')
            xtmp = np.linspace(a - 7, a + 7, 1000)
            ytmp = f(xtmp, a, b, c)
            if f(a, a, b, c) > max(self.currBeachLine):
                self.nonActive.append(p)
            # light gray plot
            plt.plot(xtmp, ytmp, 'k--', alpha=0.2)
            for i in x:
                x[i].append(f(i, a, b, c))

        y = [min(x[i]) for i in x]
        x = np.linspace(-lim, lim, 1000).tolist()
        self.currBeachLine = y
        plt.plot(x, y)
        plt.plot(x, np.ones(len(x)) * c, 'r')
        plt.grid("on")
        # regular lim axis
        plt.xlim(-lim, lim)
        plt.ylim(-lim, lim)

    def animate(self):
        frames = []
        for i in np.linspace(-lim, lim, 100):
            # if i*-1 < -5.5:
            #     continue
            frame = self.beachLineP(i * -1)
            frames.append(frame)

        gif.save(frames, "beachLine.gif", duration=100)


# beachLineP(0, points)
vor = Voronoi(points, lim)
vor.animate()
