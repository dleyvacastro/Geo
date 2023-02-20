from graham import *
from utilites_geo import crossProduct
from matplotlib import pyplot as plt
import copy
import random


def direction(p0, p1, p2):
    # p0, p1, p2 are points
    # return: -1 if counter-clockwise, 1 if clockwise, 0 if colinear
    cp = crossProduct(p0=p0, p1=p1, p2=p2)
    if cp > 0:
        return -1  # Izquierda
    elif cp < 0:
        return 1  # Derecha
    elif cp == 0:
        return 0  # Colineal

def findUpperTangent(hull1, hull2, h1r, h2l):
    # hull1 and hull2 are the convex hulls of two sets of points
    # h1r is the rightmost point of hull1
    # h2l is the leftmost point of hull2
    # return: the upper tangent of the two convex hulls
    h1r = hull1.index(h1r)
    h2l = hull2.index(h2l)

    while 1:
        while direction(hull2[h2l], hull1[h1r], hull1[(h1r + 1) % len(hull1)]) >= 0:
            h1r = (h1r + 1) % len(hull1)
        if direction(hull1[h1r], hull2[h2l], hull2[(len(hull2) + h2l - 1) % len(hull2)]) <= 0:
            while direction(hull1[h1r], hull2[h2l], hull2[(len(hull2) + h2l - 1) % len(hull2)]) <= 0:
                h2l = (len(hull2) + h2l - 1) % len(hull2)
        else:
            break

    return h1r, h2l


def findLowerTangent(hull1, hull2, h1r, h2l):
    # hull1 and hull2 are the convex hulls of two sets of points
    # h1r is the rightmost point of hull1
    # h2l is the leftmost point of hull2
    # return: the lower tangent of the two convex hulls
    h1r = hull1.index(h1r)
    h2l = hull2.index(h2l)

    while 1:
        while direction(hull1[h1r], hull2[h2l], hull2[(h2l + 1) % len(hull2)]) >= 0:
            h2l = (h2l + 1) % len(hull2)
        if direction(hull2[h2l], hull1[h1r], hull1[(len(hull1) + h1r - 1) % len(hull1)]) <= 0:
            while direction(hull2[h2l], hull1[h1r], hull1[(len(hull1) + h1r - 1) % len(hull1)]) <= 0:
                h1r = (len(hull1) + h1r - 1) % len(hull1)
        else:
            break

    return h1r, h2l


def merger(hull1, hull2):
    # hull1 and hull2 are the convex hulls of two sets of points
    # return: the convex hull of the union of the two sets of points
    if hull1[-1] == hull1[0]:
        hull1.pop()

    if hull2[-1] == hull2[0]:
        hull2.pop()

    h1r = max(hull1, key=lambda x: x[0])  # Rightmost point of hull1
    h2l = min(hull2, key=lambda x: x[0])  # Leftmost point of hull2

    # tans
    utia, utib = findUpperTangent(hull1, hull2, h1r, h2l)
    ltia, ltib = findLowerTangent(hull1, hull2, h1r, h2l)

    hull = []

    # Append points from upper tangent point on set 1 to lower tangent point on set 1
    start = utia
    while 1:
        hull.append(hull1[start])
        if start == ltia:
            break

        start = (start + 1) % len(hull1)

    # Append points from lower tangent point on set 2 to upper tangent point on set 2
    start = ltib
    while 1:
        hull.append(hull2[start])
        if start == utib:
            break

        start = (start + 1) % len(hull2)

    return hull


def plotHull(hull, color='b'):
    x = [i[0] for i in hull]
    y = [i[1] for i in hull]
    fig = plt.plot(x, y, f'{color}-')
    return fig

def divideAndConquer(points):
    # points is a list of points
    # return: the convex hull of the set of points
    points.sort(key=lambda x: x[0])
    points1 = points[:len(points) // 2]
    points2 = points[len(points) // 2:]

    hull1 = graham(points1)
    hull2 = graham(points2)

    hull = merger(copy.deepcopy(hull1), copy.deepcopy(hull2))
    hull.append(hull[0])

    fig = plt.figure(figsize=(10, 5))
    fig.suptitle('Divide and Conquer')
    subfigs = fig.subplots(1, 2)
    subfigs[0].plot([i[0] for i in points1], [i[1] for i in points1], 'ro')
    subfigs[0].plot([i[0] for i in points2], [i[1] for i in points2], 'ro')
    subfigs[0].plot([i[0] for i in hull1], [i[1] for i in hull1], 'b-')
    subfigs[0].plot([i[0] for i in hull2], [i[1] for i in hull2], 'b-')
    subfigs[0].title.set_text('Splited Convex Hulls')

    subfigs[1].plot([i[0] for i in points], [i[1] for i in points], 'ro')
    subfigs[1].plot([i[0] for i in hull], [i[1] for i in hull], 'b-')
    subfigs[1].title.set_text('Merged Convex Hull')

    plt.show()
    return hull


def main():
    points = [(4.4761, 1.994), (4.9466, 1.2667), (0.1991, 3.0293), (1.2734, 4.9885), (1.9589, 3.6342), (3.7172, 3.6357),
              (4.0876, 0.2972), (4.304, 2.2281), (3.2383, 3.0908), (3.1682, 3.7495), (0.7345, 4.7487), (3.968, 3.5959),
              (1.2508, 0.1982), (0.1991, 2.256), (0.1991, 1.562), (2.134, 1.562), (3.334, 1.562)]

    points.sort(key=lambda x: x[0])
    points1 = points[:len(points) // 2]
    points2 = points[len(points) // 2:]

    g1 = graham(points1)
    g2 = graham(points2)

    plotHull(g1)
    plotHull(g2)
    plt.show()

    hull = merger(g1, g2)
    # hull.append(hull[0])
    plotHull(hull)
    # plot the points
    x = [i[0] for i in points]
    y = [i[1] for i in points]
    plt.plot(x, y, 'ro')
    plt.show()

def main2():
    points = [(4.4761, 1.994), (4.9466, 1.2667), (0.1991, 3.0293), (1.2734, 4.9885), (1.9589, 3.6342), (3.7172, 3.6357),
              (4.0876, 0.2972), (4.304, 2.2281), (3.2383, 3.0908), (3.1682, 3.7495), (0.7345, 4.7487), (3.968, 3.5959),
              (1.2508, 0.1982), (0.1991, 2.256), (0.1991, 1.562), (2.134, 1.562), (3.334, 1.562)]
    # points = [(0, 0), (1, 1), (1, 0), (2, 0), (2, 2), (3, 0)]
    hull = divideAndConquer(points)
    hull.append(hull[0])
    plt.close()




if __name__ == "__main__":
    main2()
