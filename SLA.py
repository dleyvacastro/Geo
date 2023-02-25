import numpy as np
import matplotlib.pyplot as plt
from utilites_geo import *
from BT import *


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __lt__(self, p) -> bool:
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
        #        selfysl = SweepLine.y
        if start > end:
            start, end = end, start
        self.start = start
        self.end = end

    def add2plot(self, color=''):
        plt.plot([self.start.x, self.end.x], [
            self.start.y, self.end.y], f'{color}-', label=self.label)

    #    def isInSegment(self, p) -> bool:
    #        cross_res = cross(self.start, self.end, p.start, p.end)
    #        return  cross_res[0] and cross_res[1] not in [p.getUpperPoint(), p.getLowerPoint()]

    def sp_intersection_point(self, y):
        alpha = (y - self.end.y) / (self.start.y - self.end.y)
        x = alpha * self.start.x + (1 - alpha) * self.end.x
        return Point(round(x, 2), round(y, 2))

    def __lt__(self, s):
        if self.ysl is None:
            raise "non ysl 2"
        elif s.ysl is None:
            raise "no s ysl"
        elif self.ysl != s.ysl:
            raise "different ysl"
        return self.sp_intersection_point(self.ysl) < s.sp_intersection_point(self.ysl)

    def __gt__(self, s):
        return not self.__lt__(s)

    def __eq__(self, s):
        return self.start == s.start and self.end == s.end

    def __iter__(self):
        return iter([self.start, self.end])

    def __repr__(self):
        return f'{self.start} -> {self.end}'

    def __str__(self):
        return f'{self.start} -> {self.end}'


class SweepLine:
    def __init__(self, S):
        self.S = S
        self.T = None
        self.U = []
        self.L = []
        self.C = []
        self.Q = []
        self.intersects = []
        self.y = 0
        self.treeArr = []

    def findNewEvent(self, sl, sr, p):

        intersection = cross(sl.start.toTuple(), sl.end.toTuple(), sr.start.toTuple(), sr.end.toTuple())

        if not intersection[0]:
            return
        intersection = intersection[1]

        intersection_point = Point(intersection[0], intersection[1])

        if p[0] < intersection_point != p[0] and intersection_point not in [i[0] for i in self.Q]:
            self.Q.append((intersection_point, sl, 'c'))
            self.Q.sort(key=lambda x: x[0])

    def moveSweepLine(self):
        for i in self.Q:
            i[1].ysl = self.y

        for i in self.treeArr:
            i.ysl = self.y

    def handleEventPoint(self, p, count):

        self.U = [i[1] for i in self.Q if i[2] == 'u' and i[0] == p[0]]
        self.L = [i[1] for i in self.Q if i[2] == 'l' and i[0] == p[0]]

        if p[2] == 'u':
            self.U.append(p[1])
        elif p[2] == 'l':
            self.L.append(p[1])

        self.treeArr = inOrder(self.T)

        self.C = [i for i in self.treeArr if (i.sp_intersection_point(p[0].y) == p[0] or abs(
            p[0].x - i.sp_intersection_point(p[0].y).x) < 0.1) and i not in self.L and i not in self.U]

        if p[2] == 'c' and p[1] not in self.C:
            self.C.append(p[1])

        if len(self.L + self.U + self.C) > 1:
            self.intersects.append([p, self.L, self.U, self.C])

        for i in self.L + self.C:
            if i in self.treeArr:
                self.treeArr.remove(i)

        for i in self.U + self.C:
            if i not in self.treeArr:
                self.treeArr.append(i)

        self.y -= 0.1
        self.moveSweepLine()

        if (not self.treeArr and not self.Q) or not self.treeArr:
            return

        root = self.treeArr.pop(0)
        self.T = Node(root)

        for i in self.treeArr:
            insertBST(self.T, Node(i))

        self.treeArr = inOrder(self.T)

        if len(self.treeArr) > 1:
            if not self.U + self.C:

                indx = 0

                xs = [p[0].x]

                for i in self.treeArr:
                    xs.append(i.sp_intersection_point(self.y).x)

                while max(xs) != p[0].x and self.treeArr[indx].sp_intersection_point(self.y).x < p[0].x:
                    indx += 1
                sr = self.treeArr[indx]
                sl = self.treeArr[indx - 1]

                self.findNewEvent(sl, sr, p)
            else:
                U_C = self.U + self.C
                indx = 0
                s_prime = None
                s_prime_prime = None
                sl = None
                sr = None

                while 1:
                    if self.treeArr[indx] in U_C:
                        s_prime = self.treeArr[indx]
                        sl = self.treeArr[indx - 1]
                        break
                    indx += 1

                self.findNewEvent(sl, s_prime, p)
                indx = -1

                while 1:
                    if self.treeArr[indx] in U_C:
                        s_prime_prime = self.treeArr[indx]
                        sr = self.treeArr[indx + 1]
                        break
                    indx -= 1

                self.findNewEvent(s_prime_prime, sr, p)

        pass

    def findIntersections(self):
        # (event, event_segment, event_type)
        # All segments upper points (point, segment, 'upper')
        Q_U = [(i.start, i, 'u') for i in self.S]
        # All segments lower points (point, segment, 'lower')
        Q_L = [(i.end, i, 'l') for i in self.S]
        self.Q.extend(Q_U + Q_L)  # All segments
        # Initialize the tree with the first p
        self.Q.sort(key=lambda x: x[0])

        #        self.y = self.Q[0][0].y
        #        self.moveSweepLine()

        self.T = Node(self.Q[0][1])

        # Iterate over all points in Q
        count = 0
        while self.Q:
            self.y = self.Q[0][0].y
            self.moveSweepLine()

            p = self.Q.pop(0)
            # self.sweepLineState(p)
            self.handleEventPoint(p, count)

            count += 1

        intersected_points = []

        for i in self.intersects:
            intersected_points.append(i[0][0])

        return intersected_points


def segmentGenerator(n, limit):
    return [Segment(Point(round(np.random.uniform(1, limit), 2), round(np.random.uniform(1, limit), 2)),
                    Point(round(np.random.uniform(1, limit), 2), round(np.random.uniform(1, limit), 2))) for i in
            range(n)]


def main():
    S = segmentGenerator(20, 50)

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


if __name__ == '__main__':
    main()
