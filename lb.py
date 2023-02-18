from random import randint
import BT as bt

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

class Segment:
    def __init__(self, p0 : Point, p1 : Point):
        self.p0 = p0
        self.p1 = p1

    def getUpperPoint(self):
        if self.p0 > self.p1:
            return self.p0
        return self.p1

    def getLowerPoint(self):
        if self.p0 < self.p1:
            return self.p0
        return self.p1

    def isInSegment(self, p : Point) -> bool:
        return self.p0.x <= p.x <= self.p1.x and self.p0.y <= p.y <= self.p1.y

    def __lt__(self, s) -> bool:
        return self.getUpperPoint() < s.getUpperPoint()

    def __gt__(self, s) -> bool:
        return self.getUpperPoint() > s.getUpperPoint()

class SweepLine:
    def __init__(self, S):
        self.S = S
        self.T = bt.Node(None)
        self.intersects = []

    def findIntersections(self):
        Q = [i for i in self.S]
        while not Q:
            p = Q.pop(0)
            self.handleEventPoint(p)


    def handleEventPoint(self, p):
        U = [i for i in self.Q if i.getUpperPoint() == p]
        L = [i for i in self.Q if i.getLowerPoint() == p]
        C = [i for i in self.Q if i.isInSegment(p)]

        if len(list(dict.fromkeys(U+L+C))) > 1:
            self.intersects.append((p, U, L, C))




def comparisson_rule(p0, p1) -> bool:
    x0, y0 = p0
    x1, y1 = p1
    return (y0 > y1) or (y0 == y1 and x0 < x1)


def bubbleSort2(arr):
    n = len(arr)

    # Traverse through all array elements
    for i in range(n):

        # Last i elements are already in place
        for j in range(0, n - i - 1):

            # traverse the array from 0 to n-i-1
            # Swap if the element found is greater
            # than the next element
            if comparisson_rule(arr[j + 1], arr[j]):
                arr[j], arr[j + 1] = arr[j + 1], arr[j]


def lb_intersect_point(y0, p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    alpha = (y0 - y2) / (y1 - y2)
    x0 = alpha * x1 + (1 - alpha) * x2
    return (x0, y0)




def main():
    # #points = [Point(8,10), Point(1,2), Point(3,4), Point(5,6), Point(7,8), Point(9,10)]
    # b = bt.Node(Point(1,2))
    #
    # bt.insertBST(b, bt.Node(Point(3,4)))
    # bt.insertBST(b, bt.Node(Point(5,6)))
    # bt.insertBST(b, bt.Node(Point(7,8)))
    # bt.insertBST(b, bt.Node(Point(9,10)))
    # bt.insertBST(b, bt.Node(Point(8, 10)))
    #
    # #b.display()
    # a = bt.inOrder(b)
    # c = bt.BBT(a)
    # c.display()
    # bt.complete(c, a)
    # c.display()
    # #print(a)
    #
    # #points.sort()

    s = Segment(Point(0,0), Point(2,2))
    print(s.isInSegment(Point(1,1)))

if __name__ == "__main__":
    main()