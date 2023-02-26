import numpy as np
import matplotlib.pyplot as plt
from utilites_geo import *
from BT import *
import random


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __lt__(self, p) -> bool:
        # comparison rule for points
        return (self.y > p.y) or (self.y == p.y and self.x < p.x)

    def __gt__(self, p) -> bool:
        return not self.__lt__(p)

    def __eq__(self, p) -> bool:
        return self.x == p.x and self.y == p.y

    def __str__(self):
        return f"({self.x}, {self.y})"

    def __repr__(self):
        return f"({self.x}, {self.y})"

    def toTuple(self):
        return (self.x, self.y)


class Segment:
    def __init__(self, start: Point, end: Point, label=None):
        self.label = label
        self.ysl = None
        if start > end:
            start, end = end, start
        self.start = start
        self.end = end

    def add2plot(self, color=''):
        plt.plot([self.start.x, self.end.x], [
            self.start.y, self.end.y], f'{color}-', label=self.label)

    def toCoordsArray(self):
        return [[self.start.x, self.end.x],[self.start.y, self.end.y]]

    def sp_intersection_point(self, y):
        alpha = (y - self.end.y) / (self.start.y - self.end.y)
        x = alpha * self.start.x + (1 - alpha) * self.end.x
        return Point(round(x, 2), round(y, 2))

    def __lt__(self, s):
        if any([self.ysl is None, s.ysl is None, self.ysl != s.ysl]):
            raise ValueError('Not comparing segments with the same y')
        return self.sp_intersection_point(self.ysl) < s.sp_intersection_point(self.ysl)

    def __gt__(self, s):
        return not self.__lt__(s)

    def __repr__(self):
        return f'S({self.start} - {self.end})'

    def __str__(self):
        return f'S({self.start} - {self.end})'


class SweepLine:
    def __init__(self, S):
        self.S = S  # list of segments
        self.T = None  # binary search tree
        self.U = []  # Segments that contains p as a upper endpoint
        self.L = []  # Segments that contains p as a lower endpoint
        self.C = []  # Segments that contains p as a inner point
        self.Q = []  # Event queue
        self.I = []  # Intersection points
        self.y = None  # Sweep line height
        self.TaoSortArr = []  # Array of segments sorted by sweep line height

        self.frames = []

    # Plotter functions
    def plotState(self):
        if len(self.S) > 5:
            print("Too many segments to plot")
            return
        if self.y is None:
            return
        maxxs = max([i.start.x for i in self.S] + [i.end.x for i in self.S])
        plt.plot([0, maxxs], [self.y, self.y], 'k--', label="Sweep line")
        for i in self.S:
            if i.start.y >= self.y >= i.end.y:
                i.add2plot('b')
            else:
                # plot in gray
                i.add2plot('k')
        plt.grid()
        plt.show()

    # Sweep line functions utilities
    def updateQSP(self):
        # Updates all sweep line height in Q segments
        for i in self.Q:
            i[1].ysl = self.y

    def updateTreeArrSP(self):
        # Updates all sweep line height in tree segments
        for i in self.TaoSortArr:
            i.ysl = self.y

    def updateSP(self):
        # Updates all sweep line height in Q and tree segments
        self.updateQSP()
        self.updateTreeArrSP()

    # Algorithm functions
    def findNewEvent(self, sl, sr, p):
        intersection = cross(sl.start.toTuple(), sl.end.toTuple(), sr.start.toTuple(), sr.end.toTuple())

        if not intersection[0]:
            return
        intersection = intersection[1]

        intersection_point = Point(intersection[0], intersection[1])

        if p[0] < intersection_point != p[0] and intersection_point not in [i[0] for i in self.Q]:
            self.Q.append((intersection_point, sl, 'c'))
            self.Q.sort(key=lambda x: x[0])

    def handleEventPoint(self, p):
        self.U = [i[1] for i in self.Q if i[2] == 'u' and i[0] == p[0]]
        self.L = [i[1] for i in self.Q if i[2] == 'l' and i[0] == p[0]]

        if p[2] == 'u':
            self.U.append(p[1])
        elif p[2] == 'l':
            self.L.append(p[1])

        self.TaoSortArr = inOrder(self.T)

        self.C = [i for i in self.TaoSortArr if (i.sp_intersection_point(p[0].y) == p[0] or abs(
            p[0].x - i.sp_intersection_point(p[0].y).x) < 0.1) and i not in self.L and i not in self.U]

        if p[2] == 'c' and p[1] not in self.C:
            self.C.append(p[1])

        if len(self.L + self.U + self.C) > 1:
            self.I.append([p, self.L, self.U, self.C])

        for i in self.L + self.C:
            if i in self.TaoSortArr:
                self.TaoSortArr.remove(i)

        for i in self.U + self.C:
            if i not in self.TaoSortArr:
                self.TaoSortArr.append(i)

        self.y -= 0.001
        self.updateSP()

        if (not self.TaoSortArr and not self.Q) or not self.TaoSortArr:
            return

        root = self.TaoSortArr.pop(0)
        self.T = Node(root)

        for i in self.TaoSortArr:
            insertBST(self.T, Node(i))

        self.TaoSortArr = inOrder(self.T)

        if len(self.TaoSortArr) > 1:
            if not self.U + self.C:
                indx = 0
                xs = [p[0].x]
                for i in self.TaoSortArr:
                    xs.append(i.sp_intersection_point(self.y).x)

                while max(xs) != p[0].x and self.TaoSortArr[indx].sp_intersection_point(self.y).x < p[0].x:
                    indx += 1
                sr = self.TaoSortArr[indx]
                sl = self.TaoSortArr[indx - 1]

                self.findNewEvent(sl, sr, p)
            else:
                U_C = self.U + self.C
                indx = 0
                sp = None
                spp = None
                sl = None
                sr = None

                while 1:
                    if self.TaoSortArr[indx] in U_C:
                        sp = self.TaoSortArr[indx]
                        sl = self.TaoSortArr[indx - 1]
                        break
                    indx += 1

                self.findNewEvent(sl, sp, p)
                indx = -1

                while 1:
                    if self.TaoSortArr[indx] in U_C:
                        spp = self.TaoSortArr[indx]
                        sr = self.TaoSortArr[indx + 1]
                        break
                    indx -= 1

                self.findNewEvent(spp, sr, p)
    def findIntersections(self):
        Q_U = [(i.start, i, 'u') for i in self.S]
        Q_L = [(i.end, i, 'l') for i in self.S]
        self.Q.extend(Q_U + Q_L)
        self.Q.sort(key=lambda x: x[0])
        self.T = Node(self.Q[0][1])
        while self.Q:
            self.plotState()
            self.y = self.Q[0][0].y
            self.updateSP()

            p = self.Q.pop(0)
            self.handleEventPoint(p)

        Ip = []

        for i in self.I:
            Ip.append(i[0][0])

        return Ip


def segmentGenerator(n, limit):
    return [Segment(Point(round(random.uniform(1, limit), 2), round(random.uniform(1, limit), 2)),
                    Point(round(random.uniform(1, limit), 2), round(random.uniform(1, limit), 2))) for i in
            range(n)]


def main():
    S = segmentGenerator(5, 50)
    for i in S:
        i.add2plot()

    plt.show()

    s = SweepLine(S)
    I = s.findIntersections()
    for i in I:
        plt.plot(i.x, i.y, 'ro')

    for i in S:
        i.add2plot()

    plt.show()

def main2():
    a = Segment(Point(0, 0), Point(10, 10), 'A')
    b = Segment(Point(0, 10), Point(10, 0), 'B')

    a.add2plot()
    b.add2plot()

    plt.legend()
    plt.show()


if __name__ == '__main__':
    main()
