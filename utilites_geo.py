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

def cross(p0,p1,p2,p3):
    x0, y0 = p0
    x1, y1 = p1
    x2, y2 = p2
    x3, y3 = p3

    cp1 = crossProduct(p2,p3,p0)
    cp2 = crossProduct(p2,p3,p1)
    cp3 = crossProduct(p0,p1,p2)
    cp4 = crossProduct(p0,p1,p3)
    crossed = False

    conditions = [
        cp1*cp2 < 0 and cp3*cp4 <0,
        cp1 == 0 and min(x2,x3) <= x0 <= max(x2,x3) and min(y2,y3) <= y0 <= max(y2,y3),
        cp2 == 0 and min(x2,x3) <= x1 <= max(x2,x3) and min(y2,y3) <= y1 <= max(y2,y3),
        cp3 == 0 and min(x0,x1) <= x2 <= max(x0,x1) and min(y0,y1) <= y2 <= max(y0,y1),
        cp4 == 0 and min(x0,x1) <= x3 <= max(x0,x1) and min(y0,y1) <= y3 <= max(y0,y1)
    ]

    if any(conditions):
        crossed = True

    # get the intersection point using matrix
    A = np.matrix([
        [x2-x3, x1-x0],
        [y2-y3, y1-y0]
    ])
    print(A)

    # get the inverse of the matrix
    Ainv = np.linalg.inv(A)

    r = Ainv*np.matrix([[x1-x3],[y1-y3]])

    pcx = r[1][0] * p0[0] + (1 - r[1][0]) * p1[0]
    pcy = r[1][0] * p0[1] + (1 - r[1][0]) * p1[1]

    return float(pcx), float(pcy)


def main():
    p0 = (0, 1)
    p1 = (2, 1)
    p2 = (1, 2)
    p3 = (1, 0)
    # rotation(p0, p1, p2)
    # direction(p0,p1,p2)
    #plot the points as a cordenates
    plt.plot([p0[0], p1[0]], [p0[1], p1[1]], 'ro-')
    plt.plot([p2[0], p3[0]], [p2[1], p3[1]], 'bo-')
    plt.show()
    a = cross(p0,p1,p2,p3)
    print(a)

if __name__ == "__main__":
    main()