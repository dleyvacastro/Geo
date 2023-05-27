import numpy as np
from matplotlib import pyplot as plt


def crossProduct(p0, p1, p2):
    x0, y0 = p0
    x1, y1 = p1
    x2, y2 = p2
    return (x1-x0)*(y2-y0) - (x2-x0)*(y1-y0)

def rotation(p0, p1,p2):
    cp = crossProduct(p0=p0,p1=p1,p2=p2)
    print(f"d: {cp}")
    if cp >0:
        print("Horario")
    elif cp < 0:
        print("Antiohorario")
    elif cp == 0:
        print("paralelo")


def direction(p0, p1, p2):
    cp = crossProduct(p0 = p0, p1=p1, p2=p2)
    if cp >0:
        return 0
    elif cp < 0:
        return 1
    elif cp == 0:
        return 1


def cross(p0, p1, p2, p3):
    # Function that checks if two segments cross each other
    # p0, p1, p2, p3 are the points of the segments
    # p0 and p1 are the points of the first segment
    # p2 and p3 are the points of the second segment
    # return: (True, intersection point) if the segments cross each other in a single point
    # return: (True, interval) if the segments cross each other in an interval
    # return: (False, ()) if the segments do not cross each other

    if p0 > p3:
        p0, p2 = p2, p0
        p1, p3 = p3, p1

    x0, y0 = p0
    x1, y1 = p1
    x2, y2 = p2
    x3, y3 = p3

    cp1 = crossProduct(p2, p3, p0)
    cp2 = crossProduct(p2, p3, p1)
    cp3 = crossProduct(p0, p1, p2)
    cp4 = crossProduct(p0, p1, p3)
    crossed = False

    # Conditions to check if the segments cross each other
    conditions = [
        cp1 * cp2 < 0 and cp3 * cp4 < 0,
        cp1 == 0 and min(x2, x3) <= x0 <= max(x2, x3) and min(y2, y3) <= y0 <= max(y2, y3),
        cp2 == 0 and min(x2, x3) <= x1 <= max(x2, x3) and min(y2, y3) <= y1 <= max(y2, y3),
        cp3 == 0 and min(x0, x1) <= x2 <= max(x0, x1) and min(y0, y1) <= y2 <= max(y0, y1),
        cp4 == 0 and min(x0, x1) <= x3 <= max(x0, x1) and min(y0, y1) <= y3 <= max(y0, y1)
    ]

    # Conditions to check if the segments cross each other in an interval
    cossedInterval = [
        cp1 * cp2 == 0, cp3 * cp4 == 0,
        min(x0, x1) <= max(x2, x3),
        min(x2, x3) <= max(x0, x1),
        min(y0, y1) <= max(y2, y3),
        min(y2, y3) <= max(y0, y1)
    ]

    if any(conditions):
        crossed = True
        if all(cossedInterval):
            if (max(x2, x3) <= max(x0, x1) or (max(y2, y3) <= max(y0, y1))) and all([cp1 * cp2 == 0, cp3 * cp4 == 0]):
                if min(p2, p3) == max(p0, p1):
                    return crossed, max(p0, p1)
                return crossed, (p2, p3)

            if min(p1, p2) == max(p1, p2):
                return crossed, p1

            return crossed, (min(p1, p2), max(p1, p2))

        # get the intersection point using matrix
        A = np.matrix([
            [x2 - x3, x1 - x0],
            [y2 - y3, y1 - y0]
        ])

        # get the inverse of the matrix
        Ainv = np.linalg.inv(A)

        r = Ainv * np.matrix([[x1 - x3], [y1 - y3]])

        pcx = r[1][0] * p0[0] + (1 - r[1][0]) * p1[0]
        pcy = r[1][0] * p0[1] + (1 - r[1][0]) * p1[1]

        return crossed, (float(pcx), float(pcy))
    else:
        return crossed, ()

def plotter(cross):
    if not cross[0]:
        plt.title('Points do not cross each other')
    else:
        if type(cross[1][0]) == tuple:
            plt.title('Points cross each other in an interval')
            plt.plot([cross[1][0][0], cross[1][1][0]], [cross[1][0][1], cross[1][1][1]], 'ro-')
        else:
            plt.title('Points cross each other in a single point')
            plt.plot(cross[1][0], cross[1][1], 'ro')

    # legends
    plt.legend(['Segment 1', 'Segment 2', 'Intersection'])
    plt.xlabel('x')
    plt.ylabel('y')
    plt.show()

def main():
    p0 = (1,0)
    p1 = (1,2)
    p2 = (0,1)
    p3 = (2,1)

    # rotation(p0, p1, p2)
    # direction(p0,p1,p2)
    #plot the points as a cordenates
    plt.plot([p0[0], p1[0]], [p0[1], p1[1]], 'ro-')
    plt.plot([p2[0], p3[0]], [p2[1], p3[1]], 'bo-')
    plt.show()
    a = cross(p0,p1,p2,p3)
    print(a)

def main2():
    s1 = [(1,2),(3,4)]
    s2 = [(3,4),(5,6)]
    s3 = [(2,3),(5,6)]
    s4 = [(4,5),(5,6)]

    # plt.plot([s1[0][0], s1[1][0]], [s1[0][1], s1[1][1]], 'ro-')
    # plt.plot([s2[0][0], s2[1][0]], [s2[0][1], s2[1][1]], 'bo-')
    # plt.plot([s3[0][0], s3[1][0]], [s3[0][1], s3[1][1]], 'go-')
    # #plt.plot([s4[0][0], s4[1][0]], [s4[0][1], s4[1][1]], 'yo-')
    # plt.show()

    print(cross(s1[0],s1[1],s2[0],s2[1]))
    print(cross(s1[0],s1[1],s3[0],s3[1]))
    print(cross(s1[0],s1[1],s4[0],s4[1]))

    plotter(cross(s1[0],s1[1],s2[0],s2[1]))



if __name__ == "__main__":
    main2()