from utilites_geo import *
import numpy as np
import random
from matplotlib import pyplot as plt
import math
def slope(p0,p1):
    x0, y0 = p0
    x1, y1 = p1
    try:
        return (y1-y0)/(x1-x0)
    except:
        return float("inf")

def distance(p0, p1):
    x0, y0 = p0
    x1, y1 = p1
    return math.sqrt((x1-x0)**2 + (y1-y0)**2)

def getMin(points : list) -> tuple:
    xs = [i[0] for i in points]
    ys = [i[1] for i in points]

    temp = min(xs)
    xminindex = [i for i, j in enumerate(xs) if j == temp]

    if len(xminindex) != 1:
        ymin = min([ys[i] for i in xminindex])
        tmin = points[ys.index(ymin)]
    else:
        tmin = points[xminindex[0]]
    return tmin

def clearPoints(points: list, p0):
    # create a list of the points without p0 sorted by slope
    points.remove(p0)
    # get the poins with the same slopes
    a = {}
    for i in points:

        if slope(p0, i) not in a.keys():
            a[slope(p0, i)] = [i]
        else:
            a[slope(p0, i)].append(i)

    for i in a:
        a[i].sort(key=lambda x: distance(p0, x))

    final = [a[i][-1] for i in a]
    final.sort(key = lambda x : slope(p0, x))
    return final

def graham(points):
    S = []
    p0 = getMin(points)
    S.append(p0)
    heap = clearPoints(points, p0)
    S.append(heap[0])
    heap.pop(0)
    S.append(heap[0])
    heap.pop(0)
    # print(S)
    for i in heap:
        S.append(i)
        while direction(S[-3], S[-2], S[-1]):
            S.pop(-2)
    S.append(p0)
    return S

def randomSet(n):
    return list(set([(random.randint(0, 10), random.randint(0, 10)) for i in range(n)]))

def main():
    # points =[(0,0),(1,1),(3,3),(0,2), (1,4), (2,3), (2,1)]
    # points = [(0,0), (1,1), (3,3), (1,2), (2,1)]
    points = randomSet(10)
    p0 = getMin(points)
    convex_hull = graham(points)
    x = [i[0] for i in points]
    y = [i[1] for i in points]
    x1 = [i[0] for i in convex_hull]
    y1 = [i[1] for i in convex_hull]
    plt.plot(x, y, 'ro')
    plt.plot(x1, y1, 'b-')
    plt.show()

if __name__ == "__main__":
    main()