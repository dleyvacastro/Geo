import numpy as np
import matplotlib.pyplot as plt
from utilites_geo import *
from BT import *
from random import randint, uniform
import pprint
class Point:
    def __init__(self, x: float, y: float):
        if not isinstance(x, (int, float)):
            raise TypeError('x must be a number')
        self.x = x
        self.y = y

    def __lt__(self, p) -> bool:
        return (self.y > p.y) or (self.y == p.y and self.x < p.x)

    def __gt__(self, p) -> bool:
        return not self.__lt__(p)

    def __eq__(self, p) -> bool:
        return self.x == p.x and self.y == p.y

    def __str__(self):
        return f"P({self.x}, {self.y})"

    def __repr__(self):
        return f"P({self.x}, {self.y})"

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

    def toCoords(self):
        return [[self.start.x, self.end.x], [self.start.y, self.end.y]]

    def add2plot(self, color='', plter=plt):
        plter.plot([self.start.x, self.end.x], [
            self.start.y, self.end.y], f'{color}-', label=self.label)

    def sp_intersection_point(self, y):
        if self.start.y == self.end.y:
            return self.end
        alpha = (y - self.end.y) / (self.start.y - self.end.y)
        x = alpha * self.start.x + (1 - alpha) * self.end.x
        return Point(round(x, 5), round(y, 5))

    def __lt__(self, s):
        if any([self.ysl is None, s.ysl is None, self.ysl != s.ysl]):
            raise ValueError('Not comparing segments with the same y')
        return self.sp_intersection_point(self.ysl) < s.sp_intersection_point(self.ysl)

    def __gt__(self, s):
        return not self.__lt__(s)

    def __eq__(self, s):
        return self.start == s.start and self.end == s.end

    def __iter__(self):
        return iter([self.start, self.end])

    def __repr__(self):
        return f'S({self.start} - {self.end})'

    def __str__(self):
        return f'S({self.start} - {self.end})'


class SweepLine:
    def __init__(self, S):
        self.S = S # list of segments
        self.T = None # binary search tree
        self.U = [] # Segments that contains p as an upper endpoint
        self.L = [] # Segments that contains p as a lower endpoint
        self.C = [] # Segments that contains p as an inner point
        self.Q = [] # Event queue
        self.I = [] # Intersection points
        self.y = None # Sweep line height
        self.TaoSortArr = [] # Array of segments sorted by sweep line height

        self.warned = False

    # Plotter Functions
    def plotState(self, plot=True):
        if not plot:
            return
        if len(self.S) > 5:
            if not self.warned:
                print("Too many segments to plot")
            self.warned = True
            return
        if self.y is None:
            return
        maxxs = max([i.start.x for i in self.S] + [i.end.x for i in self.S])
        minxs = min([i.start.x for i in self.S] + [i.end.x for i in self.S])
        plt.plot([minxs, maxxs], [self.y, self.y], 'k--', label="Sweep line")
        for i in self.S:
            if i.start.y >= self.y >= i.end.y:
                i.add2plot('b')
            else:
                # plot in gray
                i.add2plot('k')
        plt.grid()
        plt.show()

    # sweep line functions utilities
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
        self.y -= 0.01
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

        self.updateSP()

        if (not self.TaoSortArr and not self.Q) or not self.TaoSortArr:
            return

        root = self.TaoSortArr.pop(0)
        self.T = Node(root)

        for i in self.TaoSortArr:
            insertBST(self.T, Node(i))

        self.TaoSortArr = inOrder(self.T)

        if len(self.TaoSortArr) > 1:
            if len(self.U + self.C) == 0:
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
                sp = sp = spp = sl = sr = None
                while 1:
                    if self.TaoSortArr[indx] in U_C:
                        s_prime = self.TaoSortArr[indx]
                        if indx == 0:
                            break
                        sl = self.TaoSortArr[indx - 1]
                        break
                    indx += 1
                if indx != 0:
                    self.findNewEvent(sl, s_prime, p)
                indx = -1

                while 1:
                    if self.TaoSortArr[indx] in U_C:
                        s_prime_prime = self.TaoSortArr[indx]
                        if indx == -1:
                            break
                        sr = self.TaoSortArr[indx + 1]
                        break
                    indx -= 1
                if indx != -1:
                    self.findNewEvent(s_prime_prime, sr, p)

        pass

    def findIntersections(self, plot=True):
        Q_U = [(i.start, i, 'u') for i in self.S]
        Q_L = [(i.end, i, 'l') for i in self.S]
        self.Q.extend(Q_U + Q_L)
        self.Q.sort(key=lambda x: x[0])
        self.T = Node(self.Q[0][1])

        while self.Q:
            self.plotState(plot)
            self.y = self.Q[0][0].y
            self.updateSP()

            p = self.Q.pop(0)
            self.handleEventPoint(p)

        return self.I


def segmentGenerator(n, limit, type=1, rounded=2):
    if type:
        return [
            Segment(
                *[Point(*[round(uniform(-limit,limit), rounded) for _ in range(2)]) for _ in range(2)]
            )
            for _ in range(n)
        ]
    return [
        Segment(
            *[Point(*[round(randint(-limit, limit), rounded) for _ in range(2)]) for _ in range(2)]
        )
        for _ in range(n)
    ]

def main():
    S = [
        Segment(Point(1,0), Point(1,10)),
        Segment(Point(0,1), Point(10,1)),
        Segment(Point(9,0), Point(9,10)),
        Segment(Point(0,9), Point(10,9))
    ]

    for i in S:
        i.add2plot()

    plt.show()

    s = SweepLine(S)
    I = s.findIntersections(plot=0)
    intersectionPoints = [i[0][0] for i in I]
    for i in S:
        i.add2plot('b')
    for i in intersectionPoints:
        plt.plot(i.x, i.y, 'ro')

    plt.title("Intersecciones")
    plt.grid(1)
    plt.show()
    print(f"Intersecciones encontradas: {len(I)}")
    for i in I:
        pprint.pprint(i[0][0])


if __name__ == '__main__':
    main()